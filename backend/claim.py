from bs4 import BeautifulSoup
import requests
import tokenizer
import sys
import io

class Claim:
    def __init__(self, href, text, height):
        maxheight = 0 # TODO: iteration 2 problem
        super(Claim, self).__init__()
        # hrefs : several reference links, which is a list of str
        # text : the text of the claim
        # child: a list of claims
        # score: matching score computed by nlp algorithm. Will be edited by user response.
        self.href = href
        self.text = text
        self.child = []
        self.height = height
        self.cand, self.score = self.parse_child(maxheight)
        
        # self.branch = order
        # default value of score is 0

    def parse_child(self, maxheight):
        ref2text = {}
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(self.href, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        text_raw = soup.findAll('p')
        for unit in text_raw:
            if len(unit.findAll('a')) > 0:
                for ref in unit.findAll('a'):
                    ref2text[unit.text] = ref['href']
            else:
                ref2text [unit.text] = ""
        # print(str(len(ref2text.keys())))
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
        return texts, scores


    def __repr__(self):
        return "claim: " + self.text + " text: " + str(self.cand)


    def get_full_claim(self):
        return "\n\nClaim: {}\ntext: {}\nscore: {}\n".format(self.text, str(self.cand), str(self.score))


""" if "__main__":
    
    url = "https://www.independent.co.uk/arts-entertainment/films/features/the-strained-making-of-apocalypse-now-1758689.html"
    text = "real dead bodies were used on the set of “Apocalypse Now.” The man who supplied them turned out to be a grave robber and was arrested"
    root = Claim(url, text, 0)
    #root.parse_child()
    print(str(root)) """



        

