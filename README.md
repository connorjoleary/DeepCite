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
  <small> Currently looking at Wikimedia https://dumps.wikimedia.org/ </small>
  
</details>
* (optional test data) Reddit World News Database: https://www.kaggle.com/rootuser/worldnews-on-reddit


### Installs
* `pip install beautifulsoup4`
* `pip install requests`
* `pip install spacy`
* `python -m spacy download en_core_web_sm` 
* `pip install --upgrade gensim`
* `pip install Flask`
* `pip install Flask-MySQLdb`

<small>Note: 'en_core_web_sm' installation is subject to change for higher accuracy</small>

## Testing
### Frontend Testing
To get the testing framework set up, run `npm install mocha`
Then run `npm test`

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
