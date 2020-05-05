import json
from tree import Tree
from controller import Claim, html_link, new_indention
import exceptions as errors


exceptions = [errors.MalformedLink, errors.URLError, errors.EmptyWebsite, errors.ClaimNotInLink, errors.InvalidInput]

def deep_cite(event, context):
    content = event

    try:
        claim = sanitize_claim(content['claim'])
        link = sanitize_link(content['link'])
    except Exception as e:
        print(e)
        print('Error 505: HTTP Verison Not Supported, hacker')
        return {'error': 'Error 505: HTTP Verison Not Supported, hacker' }

    full_pre_json = {'error': 'none'}

    try:
        tree = Tree(link, claim)
        full_pre_json = {'results': tree.get_best_path()}
    # handles exceptions that arise
    except Exception as e:
        if check_instance(e):
            full_pre_json['error'] = str(e)
        else:
            link = html_link('https://github.com/root1337/DeepCite/issues')
            full_pre_json['error'] = str('Error 500: Internal Server Error ' + str(e) + "."  + \
                        new_indention("Please add your error to " + link + " with the corresponding claim and link."))
    print(full_pre_json)
    return full_pre_json

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
    url = "https://www.nature.com/articles/1704715"
    claim = "After transplantation, it has been of central interest whether the newly developed hematopoietic system is of recipient or donor origin."
    deep_cite({'link': url, 'claim': claim}, '')
