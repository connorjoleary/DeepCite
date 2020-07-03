from app import lambda_handler
import json

from flask import Flask, jsonify, request
app = Flask(__name__)

@app.route('/test/deepcite', methods=['POST'])
def test_lambda():
    print('running')
    content = request.get_json()

    try:
        claim = content['claim']
        link = content['link']
        id = content.get('id')
        response_size = content.get('response_size', 'small')
    except Exception as e:
        return jsonify({'error': 'Error 505: HTTP Verison Not Supported' })

    body = json.dumps({"claim": claim, "link": link, "id": id, "response_size": response_size})
    response = lambda_handler({"test": True, "isBase64Encoded": False, "body": body, "requestContext": {"http": {"method": "POST", "sourceIp": "0.0.0.0"}, "stage": "dev", }},0)

    return json.dumps(response['body'])


if __name__ == '__main__':
   app.run()