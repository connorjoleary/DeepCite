from main import lambda_handler
import json

from flask import Flask, jsonify, request
app = Flask(__name__)

@app.route('/test/deepcite', methods=['POST'])
def test_lambda():
    print('running')
    response = lambda_handler(request)
    print(response)

    return json.dumps(response)


if __name__ == '__main__':
   app.run()