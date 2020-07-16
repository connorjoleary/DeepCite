from app import lambda_handler
import json

from flask import Flask, jsonify, request
app = Flask(__name__)

@app.route('/test/deepcite', methods=['POST'])
def test_lambda():
    print('running')
    content = request.get_json()

    response = lambda_handler(content,0)

    return {'Payload': response['body']}


if __name__ == '__main__':
   app.run()