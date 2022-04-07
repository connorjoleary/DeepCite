from bs4 import BeautifulSoup
import exceptions as error
import requests
from tokenizer import Tokenizer
from wiki_scraper import wiki
import sys
import io
import re
import os
import queue as q
from config import config
import uuid
import json
from urllib.parse import urlparse

CWD_FOLDER = os.path.dirname(os.path.abspath(__file__))

def new_indention(text):
    style =  'style = \"color:#8b0000; font-style: italic; font-weight: bold;\">'
    return "<div><p " + style + text + "</p></div>" 

def html_link(link):
    return "<a href= \"" + link + "\">" + link + "</a>"


class Claim:
    maxheight = config['model']['max_height']
    def __init__(self, href, text: str, tokenizer: Tokenizer, score = 1, height = 0, parent = None):
        super(Claim, self).__init__()
        self.id = str(uuid.uuid4())
        # text : the text of the claim
        # child: a list of claims
        # score: matching score computed by nlp algorithm
        # parent: a instance of Claim class.
        # visited: a list to store all the hrefs for cycle detection.
        if href == '' or text == '':
            if parent == None:
                raise error.InvalidInput('Input is invalid.')
        self.href = href
        self.text = text
        self.tokenizer = tokenizer
        self.parent = parent
        self.child = []
        self.score = score
        self.height = height
        self.visited = []
        parse_result = self.parse_child()

        # If there was some issue with the website
        if parse_result:
            self.child.append(Claim('', parse_result, self.tokenizer, score=-1, height=(self.height +1), parent=self))
        self.jumps = []
        
        # Add field cand and score to the parent so that children can work correctly
        # self.branch = order
        # default value of score is 0

    def check_repeats(self):
        """ Checks for cycles and adds visited urls to list
        """
        if self.parent != None:
            self.visited = self.parent.visited

        # Cycle Detection
        if self.href in self.visited and self.parent != None:
            # Terminate the scraper and parse the parent node to the leaf list
            return False

        return True


    # returns the p tags found in link
    def get_page_text(self, response):

        # static html
        soup = BeautifulSoup(response.text, 'html.parser')
        static = soup.findAll('p')

        return static


    # calls tokenizer and gets potential sources to claim
    def set_cand(self, ref2text):
        cand = self.tokenizer.predict(self.text, list(ref2text.keys()))
        texts = []
        scores = []
        for text in cand:
            texts.append(text[0])
            scores.append(text[1])
        self.cand = texts
        return scores

    # tree be making babies
    def create_children(self, ref2text, scores):
        # iterates through texts to check if there is a link associtated with text
        for i, words in enumerate(self.cand):
            if words in ref2text:
                if ref2text[words] != "":  # if there is a link
                    self.child.append(Claim(ref2text[words], words, self.tokenizer, scores[i], (self.height +1), self)) # does ref2text allow for multiple links
                else:
                    self.child.append(Claim("", words, self.tokenizer, scores[i], (self.height +1), self))

            # tokenizer returned a sentence
            else:
                ref_key = ""
                # looks for paragraph that the sentence is in 
                for key in ref2text.keys():
                    if words in key:
                        ref_key = key
                        break

                # sentence was not found - creates a leaf node - should not be reached but okay
                if ref_key == "":
                    self.child.append(Claim("", words, self.tokenizer, scores[i], (self.height +1), self))
                    continue
                # has a link - creates new jump
                if ref2text[ref_key] != "" and self.height < Claim.maxheight:
                    self.child.append(Claim(ref2text[ref_key], words, self.tokenizer, scores[i], (self.height +1), self))
                # creates leaf node
                elif self.height < Claim.maxheight:
                    self.child.append(Claim("", words, self.tokenizer, scores[i], (self.height +1), self))



    def parse_child(self):
        """ Checks the validity of the link (cyles, malformed) and creates the children 
        """
        ref2text = {}
        if self.href == "":
            return
        elif self.height >= Claim.maxheight:
            return

        # Check if root node
        if self.parent:
            parent_host = urlparse(self.parent.href).hostname
        else:
            parent_host = ''

        # is wikipedia link then correct href
        if self.parent != None and parent_host.endswith(".wikipedia.org"):
            citation = wiki(self.href, self.parent.href)
            if citation == None:
                self.href = self.parent.href + self.href
                self.score = self.parent.score
                return 'Unable to handle wiki link'
            else:
                self.href = citation

        # Check common errors
        if not self.check_repeats():
            self.score = self.parent.score
            return 'URL is repeated'
        try:
            host = urlparse(self.href).hostname
        except ValueError:
            if self.parent == None:
                raise error.MalformedLink('URL cannot be parsed')
            return 'URL is malformed'

        # gets url
        user_agent = {'User-agent': 'Mozilla/5.0'}
        try:
            response = requests.get(self.href, headers=user_agent, timeout=config['model']['request_timeout'])
        # url is trash
        except Exception as e:
            print(f"Request timed out after {config['model']['request_timeout']} seconds for {self.href}")
            # faulty input
            if self.parent == None:
                raise error.URLError('Unable to reach URL: ' + html_link(self.href))
            # create leaf
            return 'Unable to reach the url'
        
        if response.status_code != 200:
            if self.parent == None:
                raise error.EmptyWebsite(f'Website returned statue_code: {response.status_code}')
            return f'URL status code: {response.status_code}'

        # marked site as visited
        self.visited.append(self.href)

        text_raw = self.get_page_text(response)
        
        # Exception that the child of one claim has no valid sentences, then add its parent to the leaf list.
        if len(text_raw) == 0:
            # Terminate the scraper and parse the parent node to the leaf list
            # unable to obtain infomation from website
            if self.parent == None and not host.endswith(".reddit.com"):
                raise error.EmptyWebsite('Website does not have any readable text')
            return 'Website doesn\'t have any readable text'

        for unit in text_raw:
            if len(unit.findAll('a')) > 0:
                for ref in unit.findAll('a'):
                    try:
                        if ref['href'] != self.href:
                            ref2text[unit.text] = ref['href'] # doesn't this just take the last link in a piece of text?
                    except KeyError:
                        continue
            else:
                ref2text[unit.text] = ""

        # If the claim is on reddit, the title and link of the posts are not in p tags. To get around this we read its json
        if host.endswith(".reddit.com"):
            try:
                response = requests.get(self.href+'.json', headers=user_agent)
                page_info = json.loads(response.text)
            except Exception as e:
                page_info = {}
            if type(page_info) == list:
                page_info = page_info[0]

            if page_info.get('kind') == 'Listing':
                posts = page_info['data']['children']
                for post in posts:
                    if post.get('kind') == 't3':
                        post = post.get('data', {})
                        if 'url' in post and 'title' in post:
                            if post['url']!= self.href:
                                ref2text[post['title']] = post['url']

        # get tokenizer values
        scores = self.set_cand(ref2text)

        # Raise error if there are no matches on the root page
        if scores[0] <= config['model']['similarity_cutoff']:
            if self.parent == None:
                raise error.ClaimNotInLink('Unable to find \"' + self.text + '\" in ' + html_link(self.href))
            else:
                return 'No similar texts were found'

        # creates leaf node or children
        self.create_children(ref2text, scores)
