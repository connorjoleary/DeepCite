#!/bin/bash
echo starting help_test
sleep 20
# generic test
curl -d '{"claim":"Michael Jackson could not read or write music. He was also an incredible beatboxer.", "link":"https://www.nme.com/blogs/nme-blogs/the-incredible-way-michael-jackson-wrote-music-16799/amp"}' -H "Content-Type: application/json" -X POST http://127.0.0.1:5000/api/v1/deep_cite
sleep 5
# generic test
curl -d '{"claim":"white mushrooms, cremini mushrooms, and portobello mushrooms are all the same mushroom but at different stages of growth.", "link":"https://en.wikipedia.org/wiki/Agaricus_bisporus"}' -H "Content-Type: application/json" -X POST http://127.0.0.1:5000/api/v1/deep_cite
sleep 5
# trash link - expect malformed error
curl -d '{"claim":"thesdaf", "link":"trash"}' -H "Content-Type: application/json" -X POST http://127.0.0.1:5000/api/v1/deep_cite
sleep 5
# sanitizaton - expect malformed error
curl -d '{"claim":"file://D:/user/", "link":"input://trash.com/"}' -H "Content-Type: application/json" -X POST http://127.0.0.1:5000/api/v1/deep_cite
sleep 5
# malformed link - expect malformed error
curl -d '{"claim":"claim", "link":"google.com"}' -H "Content-Type: application/json" -X POST http://127.0.0.1:5000/api/v1/deep_cite
sleep 5
# fake link - issue
curl -d '{"claim":"claim", "link":"https://www.w.ca"}' -H "Content-Type: application/json" -X POST http://127.0.0.1:5000/api/v1/deep_cite
sleep 5
# error404
curl -d '{"claim":"claim", "link":"https://www.google.com/hello_world"}' -H "Content-Type: application/json" -X POST http://127.0.0.1:5000/api/v1/deep_cite
sleep 5
# claim is not in website
curl -d '{"claim":"The chicken man exists", "link":"https://en.wikipedia.org/wiki/Hubert_Schmundt"}' -H "Content-Type: application/json" -X POST http://127.0.0.1:5000/api/v1/deep_cite
sleep 5
ps -ef | grep app.py | grep -v grep | awk '{print $2}' | xargs kill -2