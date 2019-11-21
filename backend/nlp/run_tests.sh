#!/bin/bash
echo Hello, World!
coverage run app.py &
echo sent to background
sleep 300
curl -d '{"claim":"the death of Sherlock Holmes almost destroyed the magazine that had originally published the stories. When Arthur Conan Doyle killed him off in 1893, 20,000 people cancelled their subscriptions. The magazine barely survived. Its staff referred to Holmes’ death as the dreadful event.", "link":"http://www.bbc.com/culture/story/20160106-how-sherlock-holmes-changed-the-world"}' -H "Content-Type: application/json" -X POST http://127.0.0.1:5000/api/v1/deep_cite
curl -d '{"claim":"thesdaf", "link":"trash"}' -H "Content-Type: application/json" -X POST http://127.0.0.1:5000/api/v1/deep_cite
coverage report