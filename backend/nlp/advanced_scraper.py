from bs4 import BeautifulSoup
import requests
#import tokenizer
import sys
import io

class Claim:
    def __init__(self, href, text, height, parent):
        maxheight = 0 # TODO: iteration 2 problem
        super(Claim, self).__init__()
        # hrefs : several reference links, which is a list of str
        # text : the text of the claim
        # child: a list of claims
        # score: matching score computed by nlp algorithm. Will be edited by user response.
        self.href = href
        self.text = text
        self.parent = parent
        self.child = []
        self.height = height
        self.childtext = self.parse_child(maxheight)
        
        # self.branch = order
        # default value of score is 0

    def parse_child(self, maxheight):
        ref2text = {}
        print(self.href, self.height)
        if self.href[:5] != "https":
            #print(self.parent)
            #print(self.parent.split('/'))
            preref = "https://" + self.parent.split('/')[2]
            print(preref)
            self.href = "".join([preref, self.href])
        response = requests.get(self.href)
        soup = BeautifulSoup(response.text, 'html.parser')
        text_raw = soup.findAll('p')
        child_text = []
        for unit in text_raw:
            if len(unit.findAll('a')) > 0:
                for ref in unit.findAll('a'):
                    ref2text[unit.text] = ref['href']
        for text in ref2text.keys(): 
            #if self.height < maxheight:
            self.child.append(Claim(ref2text[text], text, (self.height +1), self.href))
        for child in self.child:
            child_text.append(child.text)
        '''
        cand = tokenizer.predict(self.text, list(ref2text.keys()), 1)
        texts = [] 
        scores = []
        for text in cand:
            try:
                if ref2text[text[1]] != "" and self.height < maxheight:
                    print(ref2text[text[1]])
                    self.child.append(Claim(ref2text[text[1]], text[1], (self.height + 1)))
            except KeyError:
                ref_key = ""
                for key in ref2text.keys():
                    if text[1] in key:
                        ref_key = key
                        break
                if ref2text[ref_key] != "" and self.height < maxheight:
                    self.child.append(Claim(ref2text[text[1]], text[1], (self.height +1)))
                    print(ref2text[text[1]])

            texts.append(text[1])
            scores.append(text[2])
        return texts, scores'''
        return child_text

    def cycledetection():
        return 0
        

   # def __repr__(self):
   #     return "claim: " + self.text + " text: " + str(self.childtext)
        

if "__main__":
    
    url = "https://www.britannica.com/biography/Aristotle"
    text = "Draconian laws are named after the 1st Greek legislator, Draco, who meted out severe punishment for very minor offenses. These included enforced slavery for any debtor whose status was lower than that of his creditor and the death sentence for stealing a cabbage."
    root = Claim(url, text, 0, "")
    print(str(root.child))



        

