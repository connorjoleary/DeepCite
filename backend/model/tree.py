from bs4 import BeautifulSoup
import requests
import os
from claim import Claim
import queue as q

# Call the Claim constructor to create the instance root. Parse the root into constructor Tree to initialize instance 
# Tree.
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
        self.tree_root = Claim(url, claim)
        self.response_object = [{'citeID': self.tree_root.id, 'parentCiteID': 0, 'link': self.tree_root.href, 'score': self.tree_root.score, 'source': self.tree_root.text}]
        self.queue = q.PriorityQueue()
        inilist = []
        inilist.append(self.tree_root)
        self.queue.put(ClaimPath(inilist, 1))
        self.beam_search(self.tree_root)

    # This function multiplies the child scores by the parents... which isn't great
    def beam_search(self,root):
        #root = Node(claim.href, claim.text, claim.score)
        #jumps.append(root)
        recover_paths = []
        if len(root.child) == 0:
            return #TODO
        while self.queue.not_empty:
            cand_path = self.queue.get()
            if root in cand_path.claims:
                curr_score = cand_path.totscore
                for onechild in root.child:
                    temp_path = cand_path.claims.copy()
                    temp_path.append(onechild)
                    self.queue.put(ClaimPath(temp_path, curr_score * onechild.score))
                    self.response_object.append({'citeID': onechild.id, 'parentCiteID': root.id, 'link': root.href, 'score': curr_score * onechild.score, 'source': onechild.text})
                    self.beam_search(onechild)
                break
            else:
                recover_paths.append(cand_path)

        for path in recover_paths:
            self.queue.put(path)
