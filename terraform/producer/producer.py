from itertools import tee
import boto3
import tweepy
import json
import os
from datetime import datetime, timedelta
import logging
from decimal import Decimal

logger = logging.getLogger()
logger.setLevel((logging.INFO))

def get_secret(secret_name):
    # Create a Secrets Manager client
    client = boto3.client(service_name='secretsmanager')

    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    except Exception as e:
        raise e

    if 'SecretString' in get_secret_value_response:
        secret = get_secret_value_response['SecretString']
        return json.loads(secret)
    else:
        raise Exception("Secret not found or not in string format.")


def search_tweets_v2(client, query, max_results):
    try:
        # Include additional fields in the request
        tweet_fields = ['author_id', 'created_at', 'public_metrics']
        user_fields = ['username', 'name']

        response = client.search_recent_tweets(query=query, 
                                               max_results=max_results, 
                                               tweet_fields=tweet_fields,
                                               user_fields=user_fields,
                                               expansions=['author_id'])

        tweets = []
        if response.data:
            for tweet in response.data:
                # Find the user details who authored the tweet
                author_info = next(user for user in response.includes['users'] if user.id == tweet.author_id)
                
                # Extract information from the tweet and the author
                tweet_info = {
                    'topic': query,
                    'id': tweet.id,
                    'text': tweet.text,
                    'author_id': tweet.author_id,
                    'author_username': author_info.username,
                    'author_name': author_info.name,
                    'created_at': tweet.created_at.isoformat(),
                    'likes': tweet.public_metrics['like_count'],
                    'retweets': tweet.public_metrics['retweet_count'],
                    'replies': tweet.public_metrics['reply_count']
                }
                tweets.append(tweet_info)

        return tweets

    except tweepy.TweepyException as e:
        error_message = f"Error during search: {e}"
        if hasattr(e, 'response'):
            error_message += f"\nResponse status code: {e.response.status_code}\nResponse text: {e.response.text}"
        raise Exception(error_message)

def write_tweets_to_dynamo(tweets, query):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ.get('DYNAMO_TABLE'))
    
    logger.info(f'WRITE TO DYNAMO: {tweets}')
    ttl = int((datetime.now() + timedelta(days=7)).timestamp())

    # "sentiment": "NEUTRAL", "sentimentScore": {"Positive": 0.3553813397884369, "Negative": 0.0012201708741486073, "Neutral": 0.6433397531509399, "Mixed": 5.874782436876558e-05}
    for tweet in tweets:
        item = {
            'topic': tweet['topic'],
            'created_at': tweet['created_at'],
            'tweet_id': tweet['id'],
            'expire': ttl,
            'text': tweet['text'],
            'author_id': tweet['author_id'],
            'author_username': tweet['author_username'],
            'author_name': tweet['author_name'],
            'likes': tweet['likes'],
            'retweets': tweet['retweets'],
            'replies': tweet['replies'],
            'sentiment': tweet['sentiment'],
            'sentimentScore': {
                'positive': Decimal(tweet['sentimentScore']['Positive']),
                'negative': Decimal(tweet['sentimentScore']['Negative']),
                'neutral': Decimal(tweet['sentimentScore']['Neutral']),
                'mixed': Decimal(tweet['sentimentScore']['Mixed'])
            }
        }
        
        try:
            table.put_item(Item=item)
        except Exception as e:
            print(f"Error writing to DynamoDB: {str(e)}")
            return {
                'statusCode': 500,
                'body': json.dumps(f"Error writing to DynamoDB: {str(e)}")
            }
        
def get_search_query(event):
    try: 
        body = json.loads(event.get('body', '{}'))
    except json.JSONDecodeError:
        logger.error(("Error parsing JSON from event body"))
        return {
            'statusCode': 400,
            'body': json.dumps("Invalid JSON in request body")
        }
        
    search_query = body.get('search_query')

    if not search_query:
        return {
            'statusCode': 400,
            'body': json.dumps("No search query provided")
        }

    return search_query

def comprehend_tweets(tweets):
    comprehend = boto3.client('comprehend')

    for tweet in tweets:
        text = tweet['text']

        try:
            sentiment_response = comprehend.detect_sentiment(Text=text, LanguageCode='en')
            tweet['sentiment'] = sentiment_response['Sentiment']
            tweet['sentimentScore'] = sentiment_response['SentimentScore']
        except Exception as e:
            logger.error(f"Error in sentiment analysis: {str(e)}")
    return tweets

def lambda_handler(event, context):
    logger.info(f"Recieved event: {event}")

    secret_name = os.environ.get('SECRET_NAME')
    credentials = get_secret(secret_name)
    search_query = get_search_query(event)    

    bearer_token = credentials['bearer_token']
    client = tweepy.Client(bearer_token=bearer_token)

    tweets = search_tweets_v2(client, search_query, 10)
    logger.info(f"Tweets: {tweets}")
    
    comprehended_tweets = comprehend_tweets(tweets)
    logger.info(f"Comprehended Tweets: {comprehended_tweets}")

    write_tweets_to_dynamo(comprehended_tweets, search_query)

    return {
        'statusCode': 200,
        'body': json.dumps(comprehended_tweets)
    }
