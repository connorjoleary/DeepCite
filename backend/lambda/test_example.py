from main import lambda_handler
import uuid
import json

body = {"ip": "127.0.0.1", "stage": "test", "id": str(uuid.uuid4()), "resonse_size": "small", "claim":"the death of Sherlock Holmes almost destroyed the magazine thries. When Arthur Conan Doyle killed him off in 1893, 20,000 people cancelled their subscriptions. The magazine barely survived. Its staff referred to Holmes’ death as “the dreadful event”.", "link":"http://www.bbc.com/culture/story/20160106-how-sherlock-holmes-changed-the-world"}
print(lambda_handler(body, None))#{"isBase64Encoded": False, "body": body, "requestContext": {"http": {"method": "POST", "sourceIp": "dfsds"}, "stage": "dev", }},0))
# {"ip": "127.0.0.1", "stage": "test", "id": "", "resonse_size": "small", "claim":"the death of Sherlock Holmes almost destroyed the magazine thries. When Arthur Conan Doyle killed him off in 1893, 20,000 people cancelled their subscriptions. The magazine barely survived. Its staff referred to Holmes’ death as “the dreadful event”.", "link":"http://www.bbc.com/culture/story/20160106-how-sherlock-holmes-changed-the-world"}