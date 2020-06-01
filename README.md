# DeepCite
CS506 Project
<p> Google Chrome extension that finds the source of a claim using BeautifulSoup, spaCy, and gensim libraries. Please look at documentation for implemenation details. :trollface:</p>

## Table of Contents

* [Setup](#setup)
* [Installation](#installation)
* [Testing](#testing)
* [Authors](#authors)


## Setup

#### Chrome

1. Install Google Chrome
2. In Chrome, navigate to `chrome://extensions/`
3. Enable developer mode
4. Then click `Load unpacked` 
5. Select DeepCite/extension folder

#### Firefox

1. Install Firefox
2. Navigate to `about:debugging`
3. Then select `This FireFox`
4. Next click on the button `Load Temporary Add-on...`
5. Select `DeepCite/extension/manifest.json`

Once installed you can use DeepCite by clicking on the on the icon in the top right of the browser. There you can enter a link or claim and click `Cite` to run DeepCite. You can also populate the claim input by highlighting text, then right clicking and selecting _"Populate claim"_. Similiarly you can populate the link input with _"Populate link"_. 

## Installation for Server
Installations and downloads required before server can funciton properly

### Downloads
  * Google News vector space.
  	* Google's word2vec can be found here https://code.google.com/archive/p/word2vec/ but you can no longer install the source code from here.
  	* If you want to just download the Pre-trained models [recommended] then you can download it from this [google drive link](https://drive.google.com/file/d/0B7XkCwpI5KDYNlNUTTlSS21pQmM/edit) then extract it.
  	* You can also find this link from the [archive page](https://code.google.com/archive/p/word2vec/) mentioned above.
  	* Once you have your model you'll need to first create the directory `./DeepCite/backend/word_vectors` then you can copy or move the model into that folder.
  	* Note: the backend expects a specific file name so you may need to rename the file. The end result should look like this `./DeepCite/backend/word_vectors/GoogleNews-vectors-negative300.bin`
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
`curl -d '{"claim":"the death of Sherlock Holmes almost destroyed the magazine that had originally published the stories. When Arthur Conan Doyle killed him off in 1893, 20,000 people cancelled their subscriptions. The magazine barely survived. Its staff referred to Holmes’ death as “the dreadful event”.", "link":"http://www.bbc.com/culture/story/20160106-how-sherlock-holmes-changed-the-world"}' -H "Content-Type: application/json" -X POST http://3.19.142.118:5000/api/v1/deep_cite`

## Bugs
* Server is down due to money
* Server cannot handle two requests at the same time
* App.py has a memory leak and needs to be restarted every so often
* Server runs out of hard drive space for temp files in Chromium and needs to be rebooted every so often

## Authors
Connor O'Leary, Shourya Goel, Jiayi Hu, Vinay Janardhanam, Dillion O'Leary, Noah SickLick, and Catherine Yan
