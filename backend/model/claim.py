import exceptions as error
import tokenizer
import sys
import io
import re
import os
import queue as q
from config import config
import uuid
import json
import boto3

CWD_FOLDER = os.path.dirname(os.path.abspath(__file__))
lambda_client = boto3.client('lambda')

regex = re.compile(
    r'^(?:http|ftp)s?://' # http:// or https://
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
    r'localhost|' #localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
    r'(?::\d+)?' # optional port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)


def new_indention(text):
    style =  'style = \"color:#8b0000; font-style: italic; font-weight: bold;\">'
    return "<div><p " + style + text + "</p></div>" 

def html_link(link):
    return "<a href= \"" + link + "\">" + link + "</a>"


class Claim:
    maxheight = config['model']['max_height']
    def __init__(self, href, text, score=1, height=0, parent=None):
        super(Claim, self).__init__()
        self.id = str(uuid.uuid4())
        # hrefs : several reference links, which is a list of str
        # text : the text of the claim
        # child: a list of claims
        # score: matching score computed by nlp algorithm.
        # parent: a instance of Claim class.
        # visited: a list to store all the hrefs for cycle detection.
        if href == '' or text == '':
            if parent == None:
                raise error.InvalidInput('Input is invalid.')
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


    # sets values based on previous jups, handles exceptions
    def to_claim_link_dict(self):
        cl_dict = {}
        cl_dict['source'] = self.text
        cl_dict['link'] = self.href
        cl_dict['score'] = self.score
        return cl_dict

    # # this changes what link is associated with what claim,
    # # making the frontend look nicer
    # def to_claim_parent_link_dict(self):
    #     cl_dict = {}
    #     cl_dict['source'] = self.text
    #     if (self.parent != None):
    #         cl_dict['link'] = self.parent.href
    #     else:
    #         cl_dict['link'] = ""
    #     cl_dict['score'] = self.score
    #     return cl_dict
    
    def excep_handle(self):
        if self.parent != None:
            self.visited = self.parent.visited
            self.realscore = self.parent.score
        
        # malformed link
        if re.match(regex, self.href) is None:
            if self.parent == None:
                raise error.MalformedLink(self.href +' is malformed\n.' + new_indention("Make sure to include, \'https\\\\\', and \'.com/.org/.edu/...\'"))
            return False

        # Cycle Detection
        if self.href in self.visited and self.parent != None:
            # Terminate the scraper and parse the parent node to the leaf list
            return False
        
        return True


    # calls tokenizer and gets potential sources to claim
    def set_cand(self, ref2text):
        cand = tokenizer.predict(self.text, list(ref2text.keys()))
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
            try:
                if ref2text[words] != "":  # if there is a link
                    self.child.append(Claim(ref2text[words], words, scores[i], (self.height +1), self)) # does ref2text allow for multiple links
                else:
                    self.child.append(Claim("", words, scores[i], (self.height +1), self))

            # tokenizer returned a sentence
            except KeyError:
                ref_key = ""
                # looks for paragraph that the sentence is in 
                for key in ref2text.keys():
                    if words in key:
                        ref_key = key
                        break

                # sentence was not found - creates a leaf node - should not be reached but okay
                if ref_key == "":
                    self.child.append(Claim("", words, scores[i], (self.height +1), self))
                    continue
                # has a link - creates new jump
                if ref2text[ref_key] != "" and self.height < Claim.maxheight:
                    self.child.append(Claim(ref2text[ref_key], words, scores[i], (self.height +1), self))
                # creates leaf node
                elif self.height < Claim.maxheight:
                    self.child.append(Claim("", words, scores[i], (self.height +1), self))



    def parse_child(self):
        # Do nothing if there is a cycle
        if self.href == "":
            return
        elif self.height >= Claim.maxheight:
            return

        # no errors
        if not self.excep_handle():
            self.score = self.parent.score
            return 

        ref2text = lambda_client.invoke(
            FunctionName = 'arn:aws:lambda:eu-west-1:890277245818:function:ChildFunction',
            InvocationType = 'RequestResponse',
            Payload = json.dumps({'website': self.href})
        )

        # marked site as visited
        self.visited.append(self.href)

        if ref2text == Error:
            raise ref2text
        elif len(ref2text) == 0:
            return


        # get tokenizer values
        scores = self.set_cand(ref2text)
        if self.parent == None:
            if scores[0] <= config['model']['similarity_cutoff']:
                raise error.ClaimNotInLink('Unable to find \"' + self.text + '\" in ' + html_link(self.href))
        # creates leaf node or children
        self.create_children(ref2text, scores)
