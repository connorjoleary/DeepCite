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
            self.leaf[self.parent.text[0]] = self.parent.score[0]
            return False
        
        return True

    
    def parse_child(self, maxheight):
        # Do nothing if there is a cycle
        ref2text = {}
        if not self.excep_handle():
            return 
        
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
                ref2text [unit.text] = ""
        cand = tokenizer.predict(self.text, list(ref2text.keys()), 1)
        texts = [] 
        scores = []
        for text in cand:
            try:
                if ref2text[text[1]] != "" and self.height < maxheight:
                    texts.append(text[1])
                    scores.append(text[2])
            except KeyError:
                ref_key = ""
                for key in ref2text.keys():
                    if text[1] in key:
                        ref_key = key
                        break
                #print(ref2text[ref_key])
                if ref2text[ref_key] != "" and self.height < maxheight:
                    texts.append(text[1])
                    scores.append(text[2])
                elif self.height < maxheight:
                    self.leaf[text[1]] = text[2]
                    return
        print("text: {}".format(texts))
        print("scores: {}".format(scores))
        self.text = texts
        self.score = scores
        for words in texts:
            try:
                if ref2text[text[1]] != "" and self.height < maxheight:
                    self.child.append(Claim(ref2text[words], words, (self.height +1), self))
            except KeyError:
                ref_key = ""
                for key in ref2text.keys():
                    if text[1] in key:
                        ref_key = key
                        break
                if ref2text[ref_key] != "" and self.height < maxheight:
                    self.child.append(Claim(ref2text[words], words, (self.height +1), self))


    def __repr__(self):
        for keys, values in self.leaf.items():
            return "claim: " + self.text + "keys of leaves: " + keys + "values of leaves: " + values

if "__main__":
    
    url = "http://math.ucr.edu/home/baez/physics/Relativity/GR/grav_speed.html"
    text = "Gravity moves at the Speed of Light and is not Instantaneous. If the Sun were to disappear, we would continue our elliptical orbit for an additional 8 minutes and 20 seconds, the same time it would take us to stop seeing the light (according to General Relativity)."
    root = Claim(url, text, 0, None)




        

