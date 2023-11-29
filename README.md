# streaming_ml

## curl command to invoke lambda
Replace `reinvent` with any other topic or categroy
```
curl -X POST https://mecji43lle.execute-api.us-east-1.amazonaws.com/producer \
     -H "Content-Type: application/json" \
     -d '{"search_query": "reinvent"}'
```
