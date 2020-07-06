from app import lambda_handler

body = "{\"id\": \"fdaeasfsd\", \"resonse_size\": \"small\", \"claim\":\"the death of Sherlock Holmes almost destroyed the magazine thries. When Arthur Conan Doyle killed him off in 1893, 20,000 people cancelled their subscriptions. The magazine barely survived. Its staff referred to Holmes’ death as “the dreadful event”.\", \"link\":\"http://www.bbc.com/culture/story/20160106-how-sherlock-holmes-changed-the-world\"}"
print(lambda_handler({"isBase64Encoded": False, "body": body, "requestContext": {"http": {"method": "POST", "sourceIp": "dfsds"}, "stage": "dev", }},0))
