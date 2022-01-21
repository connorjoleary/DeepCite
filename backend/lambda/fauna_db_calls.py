from lambda_config import config
import base64
import json
import os
from google.cloud import secretmanager

from faunadb import query as q
from faunadb.objects import Ref
from faunadb.client import FaunaClient

class DatabaseCalls():

    def get_client(self):
        print('grabbing secret')

        client = secretmanager.SecretManagerServiceClient()
        secret_name = "fauna_deepcite_db"
        project_id = "deepcite-306405"

        request = {"name": f"projects/{project_id}/secrets/{secret_name}/versions/latest"}
        response = client.access_secret_version(request)
        secret_string = response.payload.data.decode("UTF-8")

        return FaunaClient(secret=secret_string, domain='db.us.fauna.com')

    def __init__(self, local_password):
        self.client = self.get_client()
        


    def record_call(self, existing_id, base_id, user_id, stage, status_code, response, time_elapsed, versions):
        try:
            if existing_id is None: # This is a new entry
                self.client.query(
                    q.create(
                        q.collection("deepcite_call"),
                        {
                            "data": {
                                'id': base_id,
                                'user_id': user_id,
                                'stage': stage,
                                'status_code': status_code,
                                'response': response,
                                'current_versions': versions,
                                'response_time_elapsed': time_elapsed
                            }
                        }
                    )
                )
            else:
                self.client.query(
                    q.create(
                        q.collection("deepcite_retrieval"),
                        {
                            "data": {
                                'id': base_id,
                                'user_id': user_id,
                                'deepcite_call_id': existing_id,
                                'stage': stage,
                                'status_code': status_code,
                                'current_versions': versions,
                                'response_time_elapsed': time_elapsed
                            }
                        }
                    )
                )
        except Exception as e:
            error = dict(
                severity="ERROR",
                message='Could not commit to database instance.',
                component="db-insert",
            )

            print(json.dumps(error))
            print(e)


    def check_repeat(self, claim: str, link: str, versions: dict) -> list:
        """ Checks if this claim and link at this version is already stored in the db.
        If it is, then we can assume the same result should be returned.

        :return: A list of matches (should only be 0-1) in the format [(<id>, <results>)]
        """
        # TODO: put in better place
        def versions_to_string(versions):
            """ Converts versions into a string in a specific order.
            """
            return versions['api']+versions['model']+versions['lambda']+versions['extension']

        responses = []
        try:
            results = self.client.query(
                q.map_(lambda x: q.get(x),
                    q.paginate(q.match(q.index("deepcite_by_source_claim_and_versions"), claim+link+versions_to_string(versions)))
                )
            )
            responses = [(result['data']['id'],result['data']['results']) for result in results['data']]
        except Exception as e:
            error = dict(
                severity="ERROR",
                message='Could not select from database instance.',
                component="db-select",
            )

            print(json.dumps(error))
            print(e)

        return responses

    def record_source(self, base_id, source_id, user_id, stage: str, versions: dict):
        """ Record the source of a deepcite call in the db.
        Triggered from users pressing the source buttons on the tree page.
        """

        try:
            self.client.query(
                q.create(
                    q.collection("deepcite_source"),
                    {
                        "data": {
                            'base_id': base_id,
                            'source_id': source_id,
                            'user_id': user_id,
                            'stage': stage,
                            'current_versions': versions
                        }
                    }
                )
            )

        except Exception as e:
            error = dict(
                severity="ERROR",
                message='Could not commit to database instance.',
                # Log viewer accesses 'component' as jsonPayload.component'.
                component="db-insert",
            )

            print(json.dumps(error))
            print(e)

# # For testing
# if __name__ == "__main__":
#     import uuid
#     versions = {a: str(b) for a,b in config['versions'].items()}
#     # res = DatabaseCalls().check_repeat(claim, link, versions)
#     res = DatabaseCalls().record_call(None, str(uuid.uuid4()), 'not_real', 'dev', 200, {}, 1, versions)
#     # (
#     #     'According to the convention of Geneva an ejected pilot in the air is not a combatant and therefore attacking him is a war crime.',
#     #     'https://www.reddit.com/r/todayilearned/comments/p4j7da/til_according_to_the_convention_of_geneva_an/',
#     #     versions)
#     print(res)