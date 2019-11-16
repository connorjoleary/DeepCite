from flask import Flask
from flask_mysqldb import MySQL

# requires a hosting site for database

app = Flask(__name__)

# configure database
# probably should use extern variables for this infomation
# documentation https://flask-mysqldb.readthedocs.io/en/latest/
app.config['MYSQL_HOST'] = ''
app.config['MYSQL_USER'] = ''
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = ''

# instanization of mysql object
mysql = MySQL(app)

@app.route('/', methods=['GET', 'POST'])
# sample section where infomation if placed into database
def home():
    #TODO: call webscraper
    # create cursor object
    # allows us to execute querries
    cursor = mysql.connection.cursor()
    # insert info into the user model
    cursor.execute("INSERT INTO user(name,email) VALUES(%s,%s)", (name,email))
    # saves the changes
    mysql.conntection.commit()
    cursor.close()
    return 'Flask'

@app.route('/users')
# sample code how infomation is retrieved from database
def users():
    cursor = mysql.connection.cursor()
    # returns the number of rows in user model in database
    resultValue = cur.execute("SELECT * FROM users")
    if resultValue > 0: # e.g. there is something inside of the database
        # returns all of rows which has been fetched by the cursor
        userDetails = cursor.fetchall()
        for user in userDetails:
            print(user[0]) # username
            print(user[0]) # user email

if __name__ == "__main__":
    app.run()