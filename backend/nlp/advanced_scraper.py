from bs4 import BeautifulSoup
import requests
import tokenizer
import sys
import io

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
        self.leaf = {}
        self.visited = []
        self.parse_child(maxheight)
        self.realscore = 0
        # Add field cand and score to the parent so that children can work correctly
        # self.branch = order
        # default value of score is 0
    
    

    def excep_handle(self):
        if self.parent != None:
            self.visited = self.parent.visited
            self.realscore = self.parent.score

        
        # fix broken link
        if self.href[:5] != "https" and self.parent != None:
            preref = "https://" + self.parent.href.split('/')[2]
            #print(preref)
            self.href = "".join([preref, self.href])
            
        
        # Cycle Detection
        if self.href in self.visited and self.parent != None:
            # Terminate the scraper and parse the parent node to the leaf list
            self.leaf[self.parent.cand[0]] = self.parent.score[0]
            return False
        
        return True

    
    def parse_child(self, maxheight):
        # Do nothing if there is a cycle
        ref2text = {}
        if not self.excep_handle():
            return 
        print(self.href)
        response = requests.get(self.href)
        self.visited.append(self.href)
        soup = BeautifulSoup(response.text, 'html.parser')
        text_raw = soup.findAll('p')

         # Exception that the child of one claim has no valid sentences, then add its parent to the leaf list.
        if len(text_raw) < 5:
            # Terminate the scraper and parse the parent node to the leaf list
            self.leaf[self.parent.text] = self.parent.score
            return 

        for unit in text_raw:
            if len(unit.findAll('a')) > 0:
                for ref in unit.findAll('a'):
                    ref2text[unit.text] = ref['href']
            else:
                ref2text[unit.text] = ""
        cand = tokenizer.predict(self.text, list(ref2text.keys()), 1)
        #print(cand)
        texts = [] 
        scores = []
        for text in cand:
            texts.append(text[1])
            scores.append(text[2])
        print("text: {}".format(texts))
        print("scores: {}".format(scores))
        self.cand = texts
        self.score = scores
        for words in texts:
            try:
                if ref2text[text[1]] != "" and self.height < maxheight:
                    self.child.append(Claim(ref2text[words], words, (self.height +1), self))
                elif self.height < maxheight:
                    self.leaf[self.text] = scores
            except KeyError:
                ref_key = ""
                for key in ref2text.keys():
                    if text[1] in key:
                        ref_key = key
                        break
                if ref2text[ref_key] != "" and self.height < maxheight:
                    #print("Success")
                    self.child.append(Claim(ref2text[words], words, (self.height +1), self))
                elif self.height < maxheight:
                    self.leaf[self.text] = self.score


    def __repr__(self):
        for keys, values in self.leaf.items():
            return "claim: " + self.text + "keys of leaves: " + keys + "values of leaves: " + str(values)

if "__main__":
    
    url = "https://en.wikipedia.org/wiki/Draco_(lawgiver)"
    text = "Draconian laws are named after the 1st Greek legislator, Draco, who meted out severe punishment for very minor offenses. These included enforced slavery for any debtor whose status was lower than that of his creditor and the death sentence for stealing a cabbage."
    root = Claim(url, text, 0, None)
    for keys, values in root.leaf.items():
        print("claim: " + root.text + "keys of leaves: " + keys + "values of leaves: " + str(values))




        

