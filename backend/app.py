from flask import Flask, jsonify
from flask import request
import json
from tree import Tree
from controller import Claim

app = Flask(__name__)

# configure database∫
# probably should use extern variables for this infomation
# documentation https://flask-mysqldb.readthedocs.io/en/latest/
# app.config['MYSQL_HOST'] = ''
# app.config['MYSQL_USER'] = ''
# app.config['MYSQL_PASSWORD'] = ''
# app.config['MYSQL_DB'] = ''

# instanization of mysql object
# mysql = MySQL(app)

# @app.route('/')
# # sample section where infomation if placed into database
# def home():

#     return 'Flask'

@app.route('/api/v1/deep_cite', methods=['GET', 'POST'])
def deep_cite():
    content = request.get_json()

    claim = sanitize_claim(content['claim'])
    #link = content['link']
    link = sanitize_link(content['link'])
    ret_json = None
    full_pre_json = {'error': 'none'}

    try:
        tree = Tree(link, claim)
        print(tree.get_best_path())
        full_pre_json = {'results': tree.get_best_path()}
    except Exception as e:
        full_pre_json['error'] = str(e)
    
    return jsonify(full_pre_json)


def sanitize_claim(claim):
    sanitized = claim
    badstrings = [';','$','&&','../','<','>','%3C','%3E','\'','--','1,2','\x00','`','(',')','file://','input://', '\n', '\t']
    
    for bad in badstrings:
        if bad in sanitized:
            sanitized = sanitized.replace(bad, '')

    return sanitized.strip()

def sanitize_link(link):
    sanitized = link
    badstrings = [';','&&','../','<','>','--','1,2','`','(',')','input://']
    
    for bad in badstrings:
        if bad in sanitized:
            sanitized = sanitized.replace(bad, '')

    return sanitized.strip()

# @app.route('/users')
# # sample code how infomation is retrieved from database
# def users():
#     cursor = mysql.connection.cursor()
#     # returns the number of rows in user model in database
#     resultValue = cur.execute("SELECT * FROM users")
#     if resultValue > 0: # e.g. there is something inside of the database
#         # returns all of rows which has been fetched by the cursor
#         userDetails = cursor.fetchall()
#         for user in userDetails:
#             print(user[0]) # username
#             print(user[0]) # user email

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
