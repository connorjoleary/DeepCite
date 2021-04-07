from lambda_config import config
import base64
import json
import os
import sqlalchemy

class DatabaseCalls():

    def get_secret(self):
        print('grabbing secret')

        secret_string = os.environ.get("DB_PASS")

        return {'password':secret_string, 'username': 'postgres', 'host': '35.226.116.208', 'dbInstanceIdentifier': 'postgres', 'port': 5432}

    def __init__(self):
        secret = self.get_secret()
        self.conn = None

        db_config = {
            # [START cloud_sql_postgres_sqlalchemy_limit]
            # Pool size is the maximum number of permanent connections to keep.
            "pool_size": 1,
            # Temporarily exceeds the set pool_size if no connections are available.
            "max_overflow": 2,
            # The total number of concurrent connections for your application will be
            # a total of pool_size and max_overflow.
            # [END cloud_sql_postgres_sqlalchemy_limit]

            # [START cloud_sql_postgres_sqlalchemy_backoff]
            # SQLAlchemy automatically uses delays between failed connection attempts,
            # but provides no arguments for configuration.
            # [END cloud_sql_postgres_sqlalchemy_backoff]

            # [START cloud_sql_postgres_sqlalchemy_timeout]
            # 'pool_timeout' is the maximum number of seconds to wait when retrieving a
            # new connection from the pool. After the specified amount of time, an
            # exception will be thrown.
            "pool_timeout": 30,  # 30 seconds
            # [END cloud_sql_postgres_sqlalchemy_timeout]

            # [START cloud_sql_postgres_sqlalchemy_lifetime]
            # 'pool_recycle' is the maximum number of seconds a connection can persist.
            # Connections that live longer than the specified amount of time will be
            # reestablished
            "pool_recycle": 540,  # 30 minutes
            # [END cloud_sql_postgres_sqlalchemy_lifetime]
        }

        db_socket_dir = os.environ.get("DB_SOCKET_DIR", "/cloudsql")
        cloud_sql_connection_name = 'deepcite-306405:us-central1:deepcite'#os.environ["CLOUD_SQL_CONNECTION_NAME"]

        pool = sqlalchemy.create_engine(

            # Equivalent URL:
            # postgres+pg8000://<db_user>:<db_pass>@/<db_name>
            #                         ?unix_sock=<socket_path>/<cloud_sql_instance_name>/.s.PGSQL.5432
            sqlalchemy.engine.url.URL(
                drivername="postgresql+pg8000",
                username=secret['username'],  # e.g. "my-database-user"
                password=secret['password'],  # e.g. "my-database-password"
                database=secret['dbInstanceIdentifier'],  # e.g. "my-database-name"
                query={
                    "unix_sock": "{}/{}/.s.PGSQL.5432".format(
                        db_socket_dir,  # e.g. "/cloudsql"
                        cloud_sql_connection_name)  # i.e "<PROJECT-NAME>:<INSTANCE-REGION>:<INSTANCE-NAME>"
                }
            ),
            **db_config
        )

        self.conn = pool.connect()

    def grab_deepcite_entry(self, id):
        try:
            with self.conn.connect() as cur:

                responses = cur.execute(f"SELECT response FROM deepcite_call where id = '{id}'").fetchall() #potentially this could just be a search by source claim and link and run for everything
                responses = [res[0] for res in responses]
        except Exception as e:
            print("ERROR: Unexpected error: Could not select from database instance.")
            print(e)
            responses = []
        print("Deepcite entry responses:", responses)
        return responses

    def record_call(self, new_submission, base_id, user_id, stage, status_code, response, time_elapsed, versions):
        try:
            with self.conn.connect() as cur:
                if new_submission:
                    cur.execute("INSERT INTO deepcite_call (id,user_id,stage,status_code,response,response_time_elapsed,current_versions) VALUES (%s, %s, %s, %s, %s, %s, %s)", (base_id, user_id, stage, status_code, json.dumps(response), time_elapsed, json.dumps(versions)))
                else:
                    cur.execute("INSERT INTO deepcite_retrieval (id,user_id,stage,status_code,response_time_elapsed,current_versions) VALUES (%s, %s, %s, %s, %s, %s)", (base_id, user_id, stage, status_code, time_elapsed, json.dumps(versions)))
        except Exception as e:
            print("ERROR: Unexpected error: Could not commit to database instance.")
            print(e)

    def record_source(self, base_id, source_id, user_id, stage, versions):
        try:
            with self.conn.connect() as cur:
                cur.execute("INSERT INTO source_label (base_id, source_id, user_id, stage, current_versions) VALUES (%s, %s, %s, %s, %s)", (base_id, source_id, user_id, stage, json.dumps(versions)))

        except Exception as e:
            print("ERROR: Unexpected error: Could not commit to database instance.")
            print(e)