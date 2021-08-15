from lambda_config import config
import base64
import json
import os
import sqlalchemy
from sqlalchemy.sql import select, and_, insert
from google.cloud import secretmanager
import pg8000

class DatabaseCalls():

    def get_secret(self):
        print('grabbing secret')
        
        client = secretmanager.SecretManagerServiceClient()
        secret_name = "deepcite_db"
        project_id = "deepcite-306405"

        request = {"name": f"projects/{project_id}/secrets/{secret_name}/versions/latest"}
        response = client.access_secret_version(request)
        secret_string = response.payload.data.decode("UTF-8")

        return {'password':secret_string, 'username': 'postgres', 'host': '35.226.116.208', 'dbInstanceIdentifier': 'postgres', 'port': 5432}

    def __init__(self):
        secret = self.get_secret()
        self.conn = None
        metadata = sqlalchemy.MetaData()

        db_config = {
            "pool_size": 1,
            "max_overflow": 2,
            "pool_timeout": 30,  # 30 seconds
            "pool_recycle": 540,  # 30 minutes
        }

        pool = sqlalchemy.create_engine(
            # Equivalent URL:
            # postgresql+pg8000://<db_user>:<db_pass>@<db_host>:<db_port>/<db_name>
            sqlalchemy.engine.url.URL(
                drivername="postgresql+pg8000",
                username=secret['username'],  # e.g. "my-database-user"
                password=secret['password'],  # e.g. "my-database-password"
                host=secret['host'],  # e.g. "127.0.0.1"
                port=secret['port'],  # e.g. 5432
                database=secret['dbInstanceIdentifier']  # e.g. "my-database-name"
            ),
            **db_config
        )

        self.conn = pool.connect()

        self.deepcite_call_table = sqlalchemy.Table('deepcite_call', metadata, autoload=True, autoload_with=pool)
        self.deepcite_retrieval_table = sqlalchemy.Table('deepcite_retrieval', metadata, autoload=True, autoload_with=pool)
        self.source_label_table = sqlalchemy.Table('source_label', metadata, autoload=True, autoload_with=pool)


    def record_call(self, existing_id, base_id, user_id, stage, status_code, response, time_elapsed, versions):
        try:
            with self.conn.connect() as cur:
                if existing_id is None: # This is a new entry
                    query = insert(self.deepcite_call_table).values(
                        id = base_id,
                        user_id = user_id,
                        stage = stage,
                        status_code = status_code,
                        response = json.dumps(response),
                        response_time_elapsed = time_elapsed,
                        current_versions = json.dumps(versions)
                    )
                    cur.execute(query)
                else:
                    query = insert(self.deepcite_retrieval_table).values(
                        id = base_id,
                        user_id = user_id,
                        deepcite_call_id = existing_id,
                        stage = stage,
                        status_code = status_code,
                        response_time_elapsed = time_elapsed,
                        current_versions = json.dumps(versions)
                    )
                    cur.execute(query)
        except Exception as e:
            print("ERROR: Unexpected error: Could not commit to database instance.")
            print(e)

    def check_repeat(self, claim, link, versions):
        responses = []
        cols = self.deepcite_call_table.c
        try:
            with self.conn.connect() as cur:
                query = select([cols.id, cols.response]).where(
                    and_(
                        cols.current_versions == versions, 
                        cols.response[('results', 0, 'link')].astext.ilike(link),
                        cols.response[('results', 0, 'source')].astext.ilike(claim)
                    )
                ).limit(1)
                responses = cur.execute(query)
                responses = [res for res in responses]
        except pg8000.exceptions.ProgrammingError as e:
            print("Exception has occurred: ProgrammingError: Could not select from database")
            print(e)

        return responses

    def record_source(self, base_id, source_id, user_id, stage, versions):
        try:
            with self.conn.connect() as cur:
                query = insert(self.source_label_table).values(
                        base_id = base_id,
                        source_id = source_id,
                        user_id = user_id,
                        stage = stage,
                        current_versions = json.dumps(versions)
                    )
                cur.execute(query)

        except Exception as e:
            print("ERROR: Unexpected error: Could not commit to database instance.")
            print(e)

# # For testing
# if __name__ == "__main__":
#     import uuid
#     versions = {a: str(b) for a,b in config['versions'].items()}
#     res = DatabaseCalls().record_call(None, str(uuid.uuid4()), 'not_real', 'dev', 200, {}, 1, versions)
#     # (
#     #     'According to the convention of Geneva an ejected pilot in the air is not a combatant and therefore attacking him is a war crime.',
#     #     'https://www.reddit.com/r/todayilearned/comments/p4j7da/til_according_to_the_convention_of_geneva_an/',
#     #     versions)
#     print(res)