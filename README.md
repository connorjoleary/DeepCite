# DeepCite
CS506 Project
<p> Google Chrome extension that finds the source of a claim using BeautifulSoup, spaCy, and gensim libraries. Please look at documentation for implemenation details. :trollface:</p>

## Table of Contents
* [Installation](#installation)
* [Testing](#testing)
* [Tasks](#tasks)
* [Authors](#authors)

## Installation
Installations and downloads required before running the application
### Downloads
<details>
  <summary> Developer Downloads </summary>
  <ul>
  <li>* MySQL documentation: https://dev.mysql.com/doc/mysql-getting-started/en/ </li>
   <li>* Recommended Database/Downloads:</li>
   <ul><li>* free remote mysql(100MB cap): https://remotemysql.com/</li>
   <li>* Community Server: https://dev.mysql.com/downloads/mysql/</li> 
   <li>* Visual Studio database: https://dev.mysql.com/downloads/windows/visualstudio/ </li>
   <li>* MySQL WorkBench: https://dev.mysql.com/downloads/workbench/ </li>
   <li>* General mySQL installer: https://dev.mysql.com/downloads/installer/</li> 
   </ul>
 </ul>
  
  <small> Currently looking at Google News vector space https://code.google.com/archive/p/word2vec/ </small>
  <small> other word2vec options: https://github.com/3Top/word2vec-api#where-to-get-a-pretrained-models </small>
  
</details>
* (optional test data) Reddit World News Database: https://www.kaggle.com/rootuser/worldnews-on-reddit


### Installs

#### For backend:
* `pip install beautifulsoup4`
* `pip install requests`
* `pip install spacy`
* `pip install --upgrade gensim`
* ~`pip install Flask`~
* ~`pip install Flask-MySQLdb`~

<small>Note: 'en_core_web_sm' installation is subject to change for higher accuracy</small>

#### For frontend:
1. Install Google Chrome
2. In Chrome, navigate to `chrome://extensions/`
3. Enable developer mode
4. "Load unpacked" 
5. Select DeepCite/extension folder
6. Click DeepCite icon in upper-right corner of Chrome to use
7. To emulate backend returning results, follow instructions in the readme within DeepCite/test-server

## Testing
### Frontend Testing
* Download and install node.js from <a href="https://nodejs.org/en/"> their website </a>
* For the following commands navigate to DeepCite/extension folder
  * Use command `npm install mocha` to install testing framework
  * Use command `npm test` to run tests


* DeepCite/test-folder contains a basic web server meant for testing frontend functionality before we connect the frontend and backend together.
  * Follow the readme in that folder for its instructions

### Backend Testing
  * main testing for nlp: run main.py in backend/nlp/
    *  **make sure testing-set/claims.txt and testing-set/links.txt are present**
    * results are printed, ignore spaCy's model's warning
    * results are stored in dataset/word2vec/redditWorldNews.txt and dataset/word2vector/redditWorldNews.model
    
  * main testing for web scraper: run tree.py in backend/tokenize/nlp/
    *  **make sure testing-set/claims.txt and testing-set/links.txt are present**
    * results are a list of node which is an interface to visualize the citation tree in frontend.

  * for testing server
    * download GoogleNews-vectors-negative300.bin.gz from https://code.google.com/archive/p/word2vec/ and place it in the word_vectors dirctory in the testing_set folder
    go into backend/nlp and run python app.py

<small>Note: connection issues make occur when webscrapping, wait a minute then run again</small>

## Tasks
- [x] Add extension
- [x] Enter Data
- [ ] View Results
- [x] Web Scraper
- [x] Word Tokenizer
- [ ] Setting up database

## Additional Features
Video transcription

##Curl request for testing
Local testing:
`curl -d '{"claim":"the death of Sherlock Holmes almost destroyed the magazine that had originally published the stories. When Arthur Conan Doyle killed him off in 1893, 20,000 people cancelled their subscriptions. The magazine barely survived. Its staff referred to Holmes’ death as “the dreadful event”.", "link":"http://www.bbc.com/culture/story/20160106-how-sherlock-holmes-changed-the-world"}' -H "Content-Type: application/json" -X POST http://127.0.0.1:5000/api/v1/deep_cite`
Server Testing:
`curl -d '{"claim":"the death of Sherlock Holmes almost destroyed the magazine that had originally published the stories. When Arthur Conan Doyle killed him off in 1893, 20,000 people cancelled their subscriptions. The magazine barely survived. Its staff referred to Holmes’ death as “the dreadful event”.", "link":"http://www.bbc.com/culture/story/20160106-how-sherlock-holmes-changed-the-world"}' -H "Content-Type: application/json" -X POST http://3.17.173.207:5000/api/v1/deep_cite`

## Authors
Shourya Goel, Jiayi Hu, Vinay Janardhanam, Dillion O'Leary, Noah SickLick, and Catherine Yan
