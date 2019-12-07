from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import tokenizer
from wiki_scraper import wiki
import sys
import io
import re
import os

CWD_FOLDER = os.path.dirname(os.path.abspath(__file__))

class Node:
    def __init__(self, url, text, isroot, score):
        self.text = text
        self.url = url
        self.score = score
        self.isroot = isroot


    def to_claim_link_dict(self):
        if self.text == None or self.url == None:
            return
        cl_dict = {}
        cl_dict['source'] = self.text
        cl_dict['link'] = self.url
        cl_dict['score'] = self.score
        return cl_dict

class Claim:
    maxheight = 8
    def __init__(self, href, text, score=1, height=0, parent=None):
         # TODO: iteration 2 problem
        super(Claim, self).__init__()
        # hrefs : several reference links, which is a list of str
        # text : the text of the claim
        # child: a list of claims
        # score: matching score computed by nlp algorithm. Will be edited by user response.
        # parent: a instance of Claim class.
        # visited: a list to store all the hrefs for cycle detection.
        self.href = href
        self.text = text
        self.parent = parent
        self.child = []
        self.score = score
        self.height = height
        self.visited = []
        self.parse_child()
        self.realscore = 0
        self.jumps = []
        
        # Add field cand and score to the parent so that children can work correctly
        # self.branch = order
        # default value of score is 0
    
    # def __str__(self):
    #     return "text: " + self.text + "href: " + self.hre


    # sets values based on previous jups, handles exceptions
    def excep_handle(self):
        if self.parent != None:
            self.visited = self.parent.visited
            self.realscore = self.parent.score

        
        # fix broken link
        if self.href[:5] != "https" and self.parent != None and self.href[:1] == "/":
            preref = "https://" + self.parent.href.split('/')[2]
            self.href = "".join([preref, self.href])
        
        
        # Cycle Detection
        if self.href in self.visited and self.parent != None:
            # Terminate the scraper and parse the parent node to the leaf list
            return False
        
        return True
     
     
     # returns the p tags found in link
     # accounts for dynamically loaded html
    def get_p_tags(self, response):
        
        # dynamic html
        op = webdriver.ChromeOptions()
        op.add_argument('headless')
        driver = webdriver.Chrome(options=op)
        driver.get(self.href)  
        js_soup = BeautifulSoup(driver.page_source, "html.parser")
        dynamic = js_soup.findAll('p')


        # static html
        soup = BeautifulSoup(response.text, 'html.parser')
        static = soup.findAll('p')

        if len(static) < len(dynamic):
            return dynamic
        return static


    # calls tokenizer and gets potential sources to claim
    def set_cand(self, ref2text):
        cand = tokenizer.predict(self.text, list(ref2text.keys()), 3)
        texts = [] 
        scores = []
        for text in cand:
            texts.append(text[1])
            scores.append(text[2])
        self.cand = texts
        return scores

    # tree be making babies
    def create_children(self, ref2text, scores):

        # iterates through texts to check if there is a link associtated with text
        for i, words in enumerate(self.cand):
            try:
                if ref2text[words] != "" and self.height < Claim.maxheight:
                    self.child.append(Claim(ref2text[words], words, scores[i], (self.height +1), self))
                elif self.height < Claim.maxheight:
                    self.child.append(Claim("", words, scores[i], (self.height +1), self))

            # tokenizer returned a sentence            
            except KeyError:
                ref_key = ""
                # looks for paragraph that the sentence is in 
                for key in ref2text.keys():
                    if key in words:
                        ref_key = key
                        break

                # sentence was not found - creates a leaf node - should not be reached but okay
                if ref_key == "":
                    self.child.append(Claim("", words, scores[i], (self.height +1), self))
                    continue
                # has a link - creates new jump
                if ref2text[ref_key] != "" and self.height < Claim.maxheight:
                    self.child.append(Claim(ref2text[ref_key], words, self.score[i], (self.height +1), self))
                # max height reached - creates leaf node
                elif self.height < Claim.maxheight:
                    self.child.append(Claim("", words, scores[i], (self.height +1), self))



    def parse_child(self):
        # Do nothing if there is a cycle
        ref2text = {}
        if self.href == "":
            return

        # is wikipedia link
        if self.parent != None and  "https://en.wikipedia.org" in self.parent.href:
            citation = wiki(self.href, self.parent.href)
            if citation == None:
                self.href = self.parent.href + self.href
                print("\n" + self.href + "\n")
                self.score = self.parent.score
                return
            else:
                print("\n" + self.href + "\n")
                self.href = citation
        # not wikipedia link
        else:
            # no errors
            if not self.excep_handle():
                self.score = self.parent.score
                return 

        # gets url
        try:
            response = requests.get(self.href)
        # url is trash
        except Exception as e:
            print("Exception: " + str(e))
            return
        

        # marked site as visited
        self.visited.append(self.href)
        text_raw = self.get_p_tags(response)
        
         # Exception that the child of one claim has no valid sentences, then add its parent to the leaf list.
        if len(text_raw) < 5:
            # Terminate the scraper and parse the parent node to the leaf list
            # TODO: if height == 1: send error to front end
            return 

        for unit in text_raw:
            if len(unit.findAll('a')) > 0:
                for ref in unit.findAll('a'):
                    try:
                        ref2text[unit.text] = ref['href']
                    except KeyError:
                        continue
            else:
                ref2text[unit.text] = ""

        # get tokenizer values
        scores = self.set_cand(ref2text)
        # creates leaf node or children
        self.create_children(ref2text, scores)
        
                    

    def get_jump(self, jumps):
        if self.parent == None:
            root = Node(self.href, self.text, True, self.score)
        else:
            root = Node(self.href, self.text, False, self.score)
        if len(self.child) == 0:
            # Jump terminate at this node
            jumps.append((root, None))
        
        else:
            for onechild in self.child:
                onechild.get_jump(jumps)
                # A jump start from a single node, ends at a list of children nodes
                jumps.append((root, Node(onechild.href, onechild.text, False, onechild.score)))


