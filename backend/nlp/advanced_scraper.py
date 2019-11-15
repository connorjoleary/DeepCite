from bs4 import BeautifulSoup
import requests
import tokenizer
from wiki_scraper import wiki
import sys
import io
import re
import os
CWD_FOLDER = os.path.dirname(os.path.abspath(__file__))

jumps = []
class Node:
    def __init__(self, url, text, isroot, score):
        self.text = text
        self.url = url
        self.score = score
        self.isroot = isroot

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
        response = requests.get(self.href)
        self.visited.append(self.href)
        soup = BeautifulSoup(response.text, 'html.parser')
        text_raw = soup.findAll('p')

         # Exception that the child of one claim has no valid sentences, then add its parent to the leaf list.
        if len(text_raw) < 5:
            # Terminate the scraper and parse the parent node to the leaf list
            
            return 

        for unit in text_raw:
            if len(unit.findAll('a')) > 0:
                print(unit)
                for ref in unit.findAll('a'):
                    ref2text[unit.text] = ref['href']
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
                    

    def get_jump(self):
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
                onechild.get_jump()
                # A jump start from a single node, ends at a list of children nodes
                jumps.append((root, Node(onechild.href, onechild.text, False, onechild.score)))
                


def main():
    test_set_claims = os.path.join(CWD_FOLDER, 'testing_set', 'claims.txt')
    f_claim = open(test_set_claims, 'r', errors='replace')
    claims = [line for line in f_claim]
    f_claim.close()

    test_set_links = os.path.join(CWD_FOLDER, 'testing_set', 'links.txt')
    f_links = open(test_set_links, 'r', errors='replace')
    links = [line for line in f_links]
    f_links.close()

    claim_Class = []
    for x in range(len(claims) - 1):
        claim_new = Claim(links[x].strip(), claims[x].strip(), 0, None)
        claim_Class.append(claim_new)

    for claim in claim_Class:
        claim.get_jump()
        print(jumps)


if "__main__":
    main()
    '''
    main()
    url = "http://math.ucr.edu/home/baez/physics/Relativity/GR/grav_speed.html"
    # #cite_note-Burke,_pp._205–214-3
    text = "Gravity moves at the Speed of Light and is not Instantaneous. If the Sun were to disappear, we would continue our elliptical orbit for an additional 8 minutes and 20 seconds, the same time it would take us to stop seeing the light (according to General Relativity)."
    root = Claim(url, text, 0, None)
    #for keys, values in root.leaf.items():
        #print("claim: " + root.text + "keys of leaves: " + keys + "values of leaves: " + str(values))
    root.get_jump()
    print(jumps)
    #for (node1, node2) in jumps:
    #    print("text1: " + node1.text + "text2: " + node2.text)
    '''

