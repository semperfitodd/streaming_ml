import json
import tweepy
import boto3
import os

def lambda_handler(event, context):
    # Authenticate with the Twitter API using the execution role's permissions
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    # Initialize the Kinesis client
    kinesis_client = boto3.client('kinesis', region_name='us-east-2')
    kinesis_stream_name = os.environ['KINESIS_STREAM_NAME']

    # Get search keywords from the environment variable
    search_keywords = os.environ['SEARCH_KEYWORDS'].split(',')

    # Initialize the tweet counter
    tweet_count = 0

    # Search for recent tweets for each keyword
    for keyword in search_keywords:
        tweets = api.search(q=keyword.strip(), lang='en', count=10)

        # Send each tweet to the Kinesis stream
        for tweet in tweets:
            try:
                # Create a record for the Kinesis stream
                kinesis_record = {
                    'Data': json.dumps(tweet._json),
                    'PartitionKey': tweet.id_str
                }
                # Put the record into the Kinesis stream
                response = kinesis_client.put_record(StreamName=kinesis_stream_name, Data=json.dumps(kinesis_record),
                                                     PartitionKey='partitionkey')
                # Increment tweet counter
                tweet_count += 1
            except Exception as e:
                print(f"Failed to send tweet with id {tweet.id_str} to Kinesis. Error: {e}")

    # Return the total number of tweets processed
    return {
        'statusCode': 200,
        'body': f"{tweet_count} tweets processed."
    }
