import json

def trim_response(error, results):
    if len(results) == 0:
        raise('No results returned, should include at least source')
    
    shortened_results = [{'link': result['link'], 'source': result['source'], 'score': result['score']} for result in results]
    source = shortened_results[0]
    shortened_results = shortened_results[1:]
    sorted_results = sorted(shortened_results, key=lambda k: k['score'], reverse=True)

    return json.dumps([source]+sorted_results[:3])



{"error":"none","results":[{"link":"","score":1,"source":"the death of Sherlock Holmes almost destroyed the magazine that had originally published the stories. When Arthur Conan Doyle killed him off in 1893, 20,000 people cancelled their subscriptions. The magazine barely survived. Its staff referred to Holmes\u2019 death as \u201cthe dreadful event\u201d."},{"link":"http://www.bbc.com/culture/story/20160106-how-sherlock-holmes-changed-the-world","score":0.8714702393054453,"source":"Conan Doyle may have thought, at the time of finishing Holmes off in print, that that was that. If he did think this, he did not understand fans \u2013 particularly fans of Holmes \u2013 very well. The public reaction to the death was unlike anything previously seen for fictional events. More than 20,000 Strand readers cancelled their subscriptions, outraged by Holmes\u2019 premature demise. The magazine barely survived. Its staff referred to Holmes\u2019 death as \u201cthe dreadful event\u201d."}]}

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
