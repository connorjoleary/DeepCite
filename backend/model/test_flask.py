from main import deep_cite
import json

from flask import Flask, jsonify, request
app = Flask(__name__)

@app.route('/api/v1/deepcite', methods=['POST'])
def test_model():
    print('running')
    content = request.get_json()

    response = deep_cite(content,0)

    return {'Payload': response['body']}


if __name__ == '__main__':
   app.run()