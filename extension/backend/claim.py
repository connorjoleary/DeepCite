from bs4 import BeautifulSoup
import requests
#import tokenizer
import sys
import io

class Claim:
    def __init__(self, href, text, order):
        super(Claim, self).__init__()
        # hrefs : several reference links, which is a list of str
        # text : the text of the claim
        # child: a list of claims
        # score: matching score computed by nlp algorithm. Will be edited by user response.
        self.href = href
        self.text = text
        self.child = []
        self.branch = order
        # default value of score is 0
        self.score = 0 

    def parse_child(self):
        ref2text = {}
        response = requests.get(self.href)
        soup = BeautifulSoup(response.text, 'html.parser')
        text_raw = soup.findAll('p')
        for unit in text_raw:
            if len(unit.findAll('a')) > 0:
                for ref in unit.findAll('a'):
                    ref2text[unit.text] = ref['href']
        cand = tokenizer.predict(self.text, ref2text.keys, self.branch)
        for text in cand:
            self.child.append(Claim(ref2text[text], text, self.order))
        return self.child

if "__main__":
    
    url = "https://en.wikipedia.org/wiki/Draco_(lawgiver)"
    text = "Draconian laws are named after the 1st Greek legislator, Draco, who meted out severe punishment for very minor offenses. These included enforced slavery for any debtor whose status was lower than that of his creditor and the death sentence for stealing a cabbage."

    root = Claim(url, text, 5)
    print(root.parse_child())



        

