from flask import Flask, jsonify
from flask import request
import json
from tree import Tree
from controller import Claim, html_link, new_indention
import exceptions as errors
import pprint
app = Flask(__name__)


exceptions = [errors.MalformedLink, errors.URLError, errors.EmptyWebsite, errors.ClaimNotInLink, errors.InvalidInput]

@app.route('/ping', methods=['GET'])
def ping():
    health = True #TODO make this better

    status = 200 if health else 404
    return flask.Response(response='\n', status=status, mimetype='application/json')

@app.route('/invocations', methods=['POST'])
def deep_cite():
    content = request.get_json()
# def deep_cite(content):

    try:
        claim = sanitize_claim(content['claim'])
        link = sanitize_link(content['link'])
    except Exception as e:
        print(e)
        return jsonify({'error': 'Error 505: HTTP Verison Not Supported, hacker' })

    full_pre_json = {'error': 'none'}

    try:
        tree = Tree(link, claim)
        full_pre_json = {'results': tree.get_best_path()}
    # handles exceptions that arise
    except Exception as e:
        print(e)
        if check_instance(e):
            full_pre_json['error'] = str(e)
        else:
            link = html_link('https://github.com/connorjoleary/DeepCite/issues')
            full_pre_json['error'] = str('Error 500: Internal Server Error ' + str(e) + "."  + \
                        new_indention("Please add your error to " + link + " with the corresponding claim and link."))
    
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(full_pre_json)
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
    # url = "https://en.wikipedia.org/wiki/Detroit_Masonic_Temple"
    # claim = "TIL that the largest Masonic Temple in the world, the Detroit Masonic Temple, was saved from foreclosure in 2013 by Jack White of the White Stripes. White paid off $142,000 owed in back taxes by the Temple due to the fact that it had given his mother a job as an usher when she was in need."
    # deep_cite({'link': url, 'claim': claim})
    app.run(host='0.0.0.0')