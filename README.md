# DeepCite
CS506 Project
<p> Google Chrome extension that finds the source of a claim using BeautifulSoup, spaCy, and gensim libraries. Please look at documentation for implemenation details. :trollface:</p>

## Table of Contents

* [Setup](#setup)
* [Installation](#installation)
* [Testing](#testing)
* [Authors](#authors)


## Setup

1. Install Google Chrome
2. In Chrome, navigate to `chrome://extensions/`
3. Enable developer mode
4. "Load unpacked" 
5. Select DeepCite/extension folder
6. Click DeepCite icon in upper-right corner of Chrome to use
7. To emulate backend returning results, follow instructions in the readme within DeepCite/test-server


## Installation for Server
Installations and downloads required before server can funciton properly

### Downloads
  * Google News vector space https://code.google.com/archive/p/word2vec/ -- in DeepCite/backend/word_vectors
  * Chrome driver https://sites.google.com/a/chromium.org/chromedriver/home -- in DeepCite/backend, check compatibility 

<small>n Note: 'en_core_web_sm' installation is testing purposes. It has lower accurary compared to the word google vectors </small>


## Testing

### Frontend Testing
* Download and install node.js from <a href="https://nodejs.org/en/"> their website </a>
* For the following commands navigate to DeepCite/extension folder
  * Use command `npm install mocha` to install testing framework
  * Use command `npm test` to run tests


* DeepCite/test-folder contains a basic web server meant for testing frontend functionality before we connect the frontend and backend together.
  * Follow the readme in that folder for its instructions

### System Testing
* To run a local server testing bash shell script:
* python -m spacy download en_core_web_sm
* run `pip install coverage`
* In DeepCite/backend, run run_tests.sh 

<small>Note: connection issues make occur when webscrapping, wait a minute then run again</small>

## Future Features
* Video transcription
* More Robust Webscrapping

## Curl request for testing
Run `gunicorn -c gunicorn_config.py wsgi` in Deepcite/backend

* Local testing:
`curl -d '{"claim":"the death of Sherlock Holmes almost destroyed the magazine that had originally published the stories. When Arthur Conan Doyle killed him off in 1893, 20,000 people cancelled their subscriptions. The magazine barely survived. Its staff referred to Holmes’ death as “the dreadful event”.", "link":"http://www.bbc.com/culture/story/20160106-how-sherlock-holmes-changed-the-world"}' -H "Content-Type: application/json" -X POST http://127.0.0.1:5000/api/v1/deep_cite`
* Server Testing:
`curl -d '{"claim":"the death of Sherlock Holmes almost destroyed the magazine that had originally published the stories. When Arthur Conan Doyle killed him off in 1893, 20,000 people cancelled their subscriptions. The magazine barely survived. Its staff referred to Holmes’ death as “the dreadful event”.", "link":"http://www.bbc.com/culture/story/20160106-how-sherlock-holmes-changed-the-world"}' -H "Content-Type: application/json" -X POST http://3.19.142.118:8000/api/v1/deep_cite`

## Bugs
* Server is down due to money
* Server cannot handle two requests at the same time
* App.py has a memory leak and needs to be restarted every so often
* Server runs out of hard drive space for temp files in Chromium and needs to be rebooted every so often

## Authors
Connor O'Leary, Shourya Goel, Jiayi Hu, Vinay Janardhanam, Dillion O'Leary, Noah SickLick, and Catherine Yan
