import requests
import spacy

import os

from flask import Flask


app = Flask(__name__)


@app.route("/")
def hello_world():
        r = requests.get('https://api.github.com/events')
        print(r.text[:25])
        nlp = spacy.load("en_core_web_lg")

        # Process whole documents
        text = ("When Sebastian Thrun started working on self-driving cars at "
                "Google in 2007, few people outside of the company took him "
                "seriously. “I can tell you very senior CEOs of major American "
                "car companies would shake my hand and turn away because I wasn’t "
                "worth talking to,” said Thrun, in an interview with Recode earlier "
                "this week.")
        doc = nlp(text)
        print(doc)
        name = os.environ.get("NAME", "World")
        return "Hello {}!".format(name)


if __name__ == "__main__":
        app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))


