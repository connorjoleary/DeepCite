from bs4 import BeautifulSoup
import requests
import sys
import io


class Claim(nn.Module):
    def __init__(self, href, text):
        super(Claim, self).__init__()
        # hrefs : several reference links, which is a list of str
        # text : the text of the claim
        # child: a list of claims
        # score: matching score computed by nlp algorithm. Will be edited by user response.
        self.href = href
        self.text = text
        self.child = []
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
                    ref2text [ref['href']] = unit.text
        cand = select_origin(self, ref2text)
        for link, text in cand.items():
            self.child.append(Claim(link, text))
        return self.child
        

    
