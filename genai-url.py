import json
from urllib.parse import parse_qs

# Replace 'YOUR_OPENAI_API_KEY' with your actual OpenAI API key
openai_api_key = ""

def run_chatbot(user_query):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {openai_api_key}',
    }

    payload = {
        'model': 'gpt-3.5-turbo',
        'messages': [
            {'role': 'system', 'content': 'You are a chatbot and you are going to give an answer to my query.'},   
            {'role': 'user', 'content': user_query}
        ],
        'max_tokens': 150,
    }

    try:
        # The API endpoint remains '/ask' even if the query parameter is in the URL
        response = requests.post('https://api.openai.com/v1/chat/completions', json=payload, headers=headers)      
        response.raise_for_status()

        choices = response.json().get('choices', [])

        if choices:
            answer = choices[0].get('message', {}).get('content', '').strip()
            return answer
        else:
            return 'Invalid response from OpenAI API'

    except requests.exceptions.RequestException as e:
        print(e)
        return 'Internal server error'

def lambda_handler(event, context):
    try:
        # Extract user_query from query parameters in the URL
        user_query = parse_qs(event['queryStringParameters']['user_query'])[0]

        # Run the chatbot with the received query
        answer = run_chatbot(user_query)

        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'answer': answer}),
        }

    except KeyError:
        return {
            'statusCode': 400,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': 'Bad Request: Missing user_query in the query parameters'}),
        }
