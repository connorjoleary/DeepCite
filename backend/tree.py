from bs4 import BeautifulSoup
import requests
# from advanced_scraper import Claim
import os
from controller import Claim
import queue as q

CWD_FOLDER = os.path.dirname(os.path.abspath(__file__))
# Call the Claim constructor in advanced_scraper to create the instance root. Parse the root into constructor Tree to initialize instance 
# Tree. Call tree.tofront() to return a list of tree nodes used for visualization.
class ClaimPath(object):
    def __init__(self, claim_path, totscore):
        self.claims = claim_path
        self.totscore = totscore
    
    def __lt__(self, other):
        # comparison in largest to smalled
        return not (self.totscore < other.totscore)
    def __repr__(self):
        return "claim path: " + [claim.to_claim_link_dict() for claim in self.claims] + " total score: " + str(self.totscore)
    

class Tree:
    def __init__(self, url, claim):
        # root: Claim
        root = Claim(url, claim)
        self.queue = q.PriorityQueue()
        inilist = []
        inilist.append(root)
        self.queue.put(ClaimPath(inilist, 1))
        self.best_queue = q.PriorityQueue()
        self.beam_search(root)



    def beam_search(self,root):
        #root = Node(claim.href, claim.text, claim.score)
        #jumps.append(root)
        recover_paths = []
        if len(root.child) == 0:
            return
        while self.queue.not_empty:
            cand_path = self.queue.get()
            if root in cand_path.claims:
                self.best_queue.put(cand_path)
                curr_score = cand_path.totscore
                for onechild in root.child:
                    temp_path = cand_path.claims.copy()
                    temp_path.append(onechild)                            
                    self.queue.put(ClaimPath(temp_path, curr_score * onechild.score))
                    self.beam_search(onechild)
                break
            else:
                recover_paths.append(cand_path)

        for path in recover_paths:
            self.queue.put(path)
      
        
    def get_best_path(self):
        best_path = self.queue.get()
        # nodes = [claim.to_claim_link_dict() for claim in best_path.claims]   
        nodes = [claim.to_claim_parent_link_dict() for claim in best_path.claims]        
        
        return nodes




