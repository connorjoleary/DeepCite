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
        claim = sanitize_claim(content['claim'])
        link = sanitize_link(content['link'])
    except Exception as e:
        return jsonify({'error': 'Error 505: claim or link cannot be sanitized' })

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

    return jsonify(full_pre_json)

def check_instance(e):
    for error in exceptions:
        if isinstance(e, error):
            return True
    return False

# sanitization and stripping of claim
def sanitize_claim(claim):
    sanitized = claim
    badstrings = [';','$','&&','../','<','>','%3C','%3E','\'','--','1,2','\x00','`','(',')','file://','input://', '\n', '\t']
    
    for bad in badstrings:
        if bad in sanitized:
            sanitized = sanitized.replace(bad, '')

    return sanitized.strip()

# sanitization of link
def sanitize_link(link):
    sanitized = link
    badstrings = [';','&&','../','<','>','--','1,2','`','(',')','input://', 'file://']
    
    for bad in badstrings:
        if bad in sanitized:
            sanitized = sanitized.replace(bad, '')

    return sanitized.strip()

if __name__ == "__main__":
    # with app.app_context():
    #     deep_cite(**{"claim":"rapper Too Short managed to sell 50,000 copies of his album \"Born to Mack\" from the trunk of his car.", "link":"https://www.reddit.com/r/todayilearned/comments/or9u42/til_rapper_too_short_managed_to_sell_50000_copies/"})
    app.run(host=config['server']['host'], port=config['server']['port'])
