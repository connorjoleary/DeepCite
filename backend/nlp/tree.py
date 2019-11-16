from bs4 import BeautifulSoup
import requests
# from advanced_scraper import Claim
import os
CWD_FOLDER = os.path.dirname(os.path.abspath(__file__))

class Tree:
    def __init__(self, root):
        self.root = root
        self.jumps = [] 
        root.get_jump(self.jumps)

    def tofront(self):
        nodes = []
        for jump in self.jumps:
            nodes.append(jump[0])
        return nodes


if __name__ == '__main__':
    from advanced_scraper import Claim
    url = "http://math.ucr.edu/home/baez/physics/Relativity/GR/grav_speed.html"
    text = "Gravity moves at the Speed of Light and is not Instantaneous. If the Sun were to disappear, we would continue our elliptical orbit for an additional 8 minutes and 20 seconds, the same time it would take us to stop seeing the light (according to General Relativity)."
    root = Claim(url, text, 0, None)
    tree = Tree(root)
    # The list of jumps, each element of the list is a tuple including start and end claim.
    # Ignore the score of the root node, the goal of it is to make scraper and nlp more convenient
    print(tree.tofront())
    #print(tree.tofront()[1][0].text)
    #print(tree.tofront()[1][1].text)
    

    #------------------Testing---------------------------------------------
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
        tree = Tree(claim)
        print(tree.tofront())


