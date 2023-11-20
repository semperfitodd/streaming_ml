import boto3
import tweepy
import json
import os


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
        response = client.search_recent_tweets(query=query, max_results=max_results, tweet_fields=["created_at", "author_id"])
        tweets = []
        if response.data:
            for tweet in response.data:
                tweets.append(tweet.text)
        return tweets
    except tweepy.TweepyException as e:
        error_message = f"Error during search: {e}"
        if hasattr(e, 'response'):
            error_message += f"\nResponse status code: {e.response.status_code}\nResponse text: {e.response.text}"
        raise Exception(error_message)


def lambda_handler(event, context):
    secret_name = os.environ.get('SECRET_NAME')
    search_query = os.environ.get('SEARCH_KEYWORDS')
    credentials = get_secret(secret_name)

    bearer_token = credentials['bearer_token']
    client = tweepy.Client(bearer_token=bearer_token)

    tweets = search_tweets_v2(client, search_query, 10)
    return {
        'statusCode': 200,
        'body': json.dumps(tweets)
    }
