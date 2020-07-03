import json


def error_results_response_format(error, results):
    return {'error': error, 'results': results}

def trim_response(error, results):
    if len(results) == 0:
        raise('No results returned, should include at least source')
    
    shortened_results = [{'link': result['link'], 'source': result['source'], 'score': result['score']} for result in results]
    source = shortened_results[0]
    shortened_results = shortened_results[1:]
    sorted_results = sorted(shortened_results, key=lambda k: k['score'], reverse=True)

    return error_results_response_format(None, [source]+sorted_results[:3])

def respond(response_size, res=None):
    if isinstance(res, Exception):
        return {
            'statusCode': '400',
            'body': error_results_response_format(res.args[0], None)
        }
    elif response_size == 'large':
        return {
            'statusCode': 200,
            'body': res.body
        }
    elif response_size == 'small':
        return {
            'statusCode': 200,
            'body': trim_response(**res)
        }

    return {
        'statusCode': '400',
        'body': error_results_response_format('response_size is not recognized', None)
    }
