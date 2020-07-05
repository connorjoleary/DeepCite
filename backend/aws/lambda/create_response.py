import json
from lambda_config import config

def trim_response(error, results):
    if len(results) == 0:
        raise('No results returned, should include at least source')
    
    shortened_results = [{'link': result['link'], 'source': result['source'], 'score': result['score']} for result in results]
    source = shortened_results[0]
    shortened_results = shortened_results[1:]
    sorted_results = sorted(shortened_results, key=lambda k: k['score'], reverse=True)

    return json.dumps([source]+sorted_results[:config['response']['num_best_returned']])

def respond(response_size, res=None):
    if isinstance(res, Exception):
        return {
            'statusCode': '400',
            'body': res.args[0]
        }
    elif response_size == 'large':
        return {
            'statusCode': 200,
            'body': json.dumps(res.body)
        }
    elif response_size == 'small':
        return {
            'statusCode': 200,
            'body': trim_response(**res)
        }

    return {
        'statusCode': '400',
        'body': 'response_size is not recognized'
    }
