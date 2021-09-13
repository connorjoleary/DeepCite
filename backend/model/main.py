from flask import Flask, jsonify
from flask import request
from config import config
import json
from tree import Tree
from claim import html_link, new_indention
import exceptions as errors
import uuid
import traceback
app = Flask(__name__)

exceptions = [errors.MalformedLink, errors.URLError, errors.EmptyWebsite, errors.ClaimNotInLink, errors.InvalidInput]

@app.route('/api/v1/deep_cite', methods=['POST'])
def deep_cite():
    content = request.get_json()
    try:
        claim = content['claim']
        link = content['link']
    except Exception as e:
        return jsonify({'error': 'Error 505: claim or link cannot be gathered' })

# def deep_cite(claim, link):
    full_pre_json = {'error': 'none', 'results': [{'citeID': str(uuid.uuid4()), 'parentCiteID': 0, 'link': link, 'score': 1, 'source': claim}]}

    try:
        tree = Tree(link, claim)
        full_pre_json['results'] = tree.response_object

    # handles exceptions that arise
    except Exception as e:
        if check_instance(e):
            full_pre_json['error'] = str(e)
        else:
            traceback.print_exc()
            link = html_link('https://github.com/connorjoleary/DeepCite/issues')
            full_pre_json['error'] = str('Error 500: Internal Server Error ' + str(e) + "."  + \
                        new_indention("Please add your error to " + link + " with the corresponding claim and link."))

    response = jsonify(full_pre_json)
    response.headers["Content-Type"] = "application/json; charset=utf-8"

    return response

def check_instance(e):
    for error in exceptions:
        if isinstance(e, error):
            return True
    return False

# if __name__ == "__main__":
#     with app.app_context():
#         print(deep_cite(**{"claim":"when not neutered, male cats develop large cheeks or jowls, triggered by testosterone. It's thought these jowls signal their virility and protect their neck during fights.", "link":"https://www.red"}))
#     # app.run(host=config['server']['host'], port=config['server']['port'])
