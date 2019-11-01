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
* `python -m spacy download en_core_web_sm` 
* `pip install --upgrade gensim`
* `pip install Flask`
* `pip install Flask-MySQLdb`

<small>Note: 'en_core_web_sm' installation is subject to change for higher accuracy</small>

#### For frontend:
1. Install Google Chrome
2. In Chrome, navigate to `chrome://extensions/`
3. Enable developer mode
4. "Load unpacked" 
5. Select DeepCite/extension folder
6. Click DeepCite icon in upper-right corner of Chrome to use

## Testing
### Frontend Testing
* Download and install node.js from <a href="https://nodejs.org/en/"> their website </a>
* For the following commands navigate to DeepCite/extension folder
  * Use command `npm install mocha` to install testing framework
  * Use command `npm test` to run tests

### Backend Testing
  * main testing: run main.py in backend/tokenizer_files/
    *  **make sure testing-set/claims.txt and testing-set/links.txt are present**
    * results are printed
  * vector creation: run vector.py with Reddit World News database
    * **make sure dataset/redditWorldNews.csv is present**
    * results are stored in dataset/word2vec/redditWorldNews.txt and dataset/word2vector/redditWorldNews.model

<small>Note: connection issues make occur when webscrapping, wait a minute then run again</small>

## Tasks
### Iteration 1
- [x] Add extension
- [x] Enter Data
- [ ] View Results
- [x] Web Scraper
- [x] Word Tokenizer
- [ ] Setting up database

## Authors
Shourya Goel, Jiahe Hu, Vinay Janardhanam, Dillion O'Leary, Noah SickLick, and Catherine Yan
