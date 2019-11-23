from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import tokenizer
from wiki_scraper import wiki
from tree import Tree
import sys
import io
import re
import os
CWD_FOLDER = os.path.dirname(os.path.abspath(__file__))

#jumps = []
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
        return cl_dict

class Claim:
    def __init__(self, href, text, height, parent, maxheight = 8):
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
        self.height = height
        self.visited = []
        self.parse_child(maxheight)
        self.realscore = 0
        self.jumps = []
        
        # Add field cand and score to the parent so that children can work correctly
        # self.branch = order
        # default value of score is 0
    
    # def __str__(self):
    #     return "text: " + self.text + "href: " + self.hre


    def excep_handle(self):
        if self.parent != None:
            self.visited = self.parent.visited
            self.realscore = self.parent.score

        
        # fix broken link
        if self.href[:5] != "https" and self.parent != None and self.href[:1] == "/":
            preref = "https://" + self.parent.href.split('/')[2]
            #print(preref)
            self.href = "".join([preref, self.href])
            print(self.href)
        
        
        # Cycle Detection
        if self.href in self.visited and self.parent != None:
            # Terminate the scraper and parse the parent node to the leaf list
            return False
        
        return True
     
    
    def parse_child(self, maxheight):
        # Do nothing if there is a cycle
        ref2text = {}
        if self.href == "":
            self.score = self.parent.score
            return
        print(self.href)
        if self.parent != None and  "https://en.wikipedia.org" in self.parent.href:
            if len(wiki(self.href, self.parent.href)) == 0:
                #print(self.parent.cand[0])
                #print(self.parent.score[0])
                self.score = self.parent.score
                return
            else:
                self.href = wiki(self.href, self.parent.href)[0]
        else:
            if not self.excep_handle():
                self.score = self.parent.score
                return 
        try:
            response = requests.get(self.href)
        except Exception as e:
            print("Exception: " + str(e))
            return

        # if js is used to load HTML contents
        driver = webdriver.Chrome()
        driver.get(self.href)
        js_soup = BeautifulSoup(driver.page_source, "html.parser")
        article_text = js_soup.findAll('p')

        # normal p tag find all
        self.visited.append(self.href)
        soup = BeautifulSoup(response.text, 'html.parser')
        text_raw = soup.findAll('p')

        # checks if JS was used to load HTML content
        if len(text_raw) < len(article_text):
            text_raw = article_text
         # Exception that the child of one claim has no valid sentences, then add its parent to the leaf list.
        if len(text_raw) < 5:
            # Terminate the scraper and parse the parent node to the leaf list
            
            return 

        for unit in text_raw:
            if len(unit.findAll('a')) > 0:
                print(unit)
                for ref in unit.findAll('a'):
                    try:
                        ref2text[unit.text] = ref['href']
                    except KeyError:
                        continue
            else:
                ref2text[unit.text] = ""
        cand = tokenizer.predict(self.text, list(ref2text.keys()), 1)
        texts = [] 
        scores = []
        for text in cand:
            texts.append(text[1])
            scores.append(text[2])
        #print("text: {}".format(texts))
        #print("scores: {}".format(scores))
        self.cand = texts
        self.score = scores
        for words in texts:
            try:
                if ref2text[text[1]] != "" and self.height < maxheight:
                    print("Branch 1")
                    self.child.append(Claim(ref2text[words], words, (self.height +1), self))
                elif self.height < maxheight:
                    print("Branch 2")
                    self.child.append(Claim("", words, (self.height +1), self))
                        
            except KeyError:
                ref_key = ""
                #print(ref2text.keys())
                for key in ref2text.keys():
                    #print(key)
                    if text[0] in key:
                        #print("8")
                        ref_key = key
                        #print(ref_key)
                        break
                if ref2text[ref_key] != "" and self.height < maxheight:
                    print("Branch 3")
                    self.child.append(Claim(ref2text[words], words, (self.height +1), self))
                elif self.height < maxheight:
                    print("Branch 4")
                    self.child.append(Claim("", words, (self.height +1), self))
                    

    def get_jump(self, jumps):
        if self.parent == None:
            root = Node(self.href, self.text, True, self.score)
        else:
            root = Node(self.href, self.text, False, self.score)
            # print(len(self.child))
        #print(len(self.child))
        if len(self.child) == 0:
            # Jump terminate at this node
            jumps.append((root, None))
        
        else:
            for onechild in self.child:
                onechild.get_jump(jumps)
                # A jump start from a single node, ends at a list of children nodes
                jumps.append((root, Node(onechild.href, onechild.text, False, onechild.score)))
                

