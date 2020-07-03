from app import lambda_handler

from flask import Flask
app = Flask(__name__)

@app.route('/prod/deepcite', methods=['POST'])
def hello_world():
   lambda_handler(event=, None)

if __name__ == '__main__':
   app.run()