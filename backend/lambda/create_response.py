import json
from lambda_config import config


def error_results_response_format(error, results):
    return {'error': error, 'results': results}

def respond(res=None):
    if isinstance(res, Exception):
        return error_results_response_format(res.args[0], None)

    return res
