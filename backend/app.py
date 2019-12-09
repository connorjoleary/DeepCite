from flask import Flask, jsonify
from flask import request
import json
from tree import Tree
from controller import Claim
import exceptions as errors
app = Flask(__name__)


exceptions = [errors.MalformedLink, errors.URLError, errors.EmptyWebsite, errors.ClaimNotInLink, errors.InvalidInput]

@app.route('/api/v1/deep_cite', methods=['GET', 'POST'])
def deep_cite():
    content = request.get_json()

    claim = sanitize_claim(content['claim'])
    link = sanitize_link(content['link'])

    full_pre_json = {'error': 'none'}

    try:
        tree = Tree(link, claim)
        full_pre_json = {'results': tree.get_best_path()}
    # handles exceptions that arise
    except Exception as e:
        if check_instance(e):
            full_pre_json['error'] = str(e)
        else:
            full_pre_json['error'] = str('Internal Server Error 500 ' + str(e))
    
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
    app.run(host='0.0.0.0')
