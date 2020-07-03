import boto3
from botocore.exceptions import ClientError

class database_calls():
    session = boto3.session.Session()

    def get_secret():
        print('grabbing secret')
        try:
            get_secret_value_response = secret_client.get_secret_value(
                SecretId=config['secret']['name']
            )
        except ClientError as e:
            print('error retrieving secret')
            print(e)
        else:
            # Decrypts secret using the associated KMS CMK.
            # Depending on whether the secret is a string or binary, one of these fields will be populated.
            if 'SecretString' in get_secret_value_response:
                secret = get_secret_value_response['SecretString']
            else:
                secret = base64.b64decode(get_secret_value_response['SecretBinary'])
        return secret

    def __init__():
        # Create a Secrets Manager client
        secret_client = session.client(
            service_name='secretsmanager',
            region_name=config['secret']['region']
        )
        secret = get_secret()
        self.conn = None
        try:
            secret = json.loads(secret)
            self.conn = psycopg2.connect(host=secret['host'], user=secret['username'], password=secret['password'], database=secret['dbInstanceIdentifier'], port=secret['port'])
        except psycopg2.OperationalError as e:
            print("ERROR: Unexpected error: Could not connect to database instance.")
            print(e)
        else:
            print("SUCCESS: Connection to RDS instance succeeded")

    def grab_deepcite_entry(self, id):
        try:
            cur = conn.cursor()
            cur.execute("SELECT response FROM deepcite_call where id = %s", (id)) #potentially this could just be a search by source claim and link and run for everything
            responses = conn.fetchall()
        except psycopg2.OperationalError as e:
            print("ERROR: Unexpected error: Could commit to database instance.")
            print(e)
            responses = []
        return responses

    def record_call(self, base_id, id, user_id, stage, response, time_elapsed, versions):
        try:
            cur = conn.cursor()
            if new_submission:
                cur.execute("INSERT INTO deepcite_retrieval (id,user_id,stage,status_code,response_time_elapsed,current_versions) VALUES (%s, %s, %s, %s, %s, %s)", (base_id, id, user_id, stage, response['statusCode'], time_elapsed, json.dumps(versions)))
            else:
                cur.execute("INSERT INTO deepcite_call (id,user_id,stage,status_code,response,response_time_elapsed,current_versions) VALUES (%s, %s, %s, %s, %s, %s, %s)", (base_id, id, user_id, stage, response['statusCode'], response['body'], time_elapsed, json.dumps(versions)))
            conn.commit()
        except psycopg2.OperationalError as e:
            print("ERROR: Unexpected error: Could commit to database instance.")
            print(e)