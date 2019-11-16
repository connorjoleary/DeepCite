from flask import Flask
from flask import request
# from nlp import Claim, Tree
# from nlp.claim import Claim
import nlp.tokenizer as tokenizer
import nlp.claim
# from flask_mysqldb import MySQL

# requires a hosting site for database

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
help(nlp)
root = Claim("link", "claim", 0, None)
tree = Tree(root)
@app.route('/')
# sample section where infomation if placed into database
def home():

    return 'Flask'

@app.route('/api/v1/deep_cite', methods=['GET', 'POST'])
def deep_cite():
    content = request.get_json()
    print(request.get_json())
    print ("claim!!: " + 
        content['claim'])
    content['link']
    claim = content['claim']
    link = content['link']

    root = nlp.claim.Claim(link, claim, 0, None)
    tree = nlp.tree.Tree(root)

    print(tree.tofront())


    ret_list
    # print content
    return 'API request'

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
    app.run()