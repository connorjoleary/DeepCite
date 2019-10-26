from bs4 import BeautifulSoup
import requests
import uuid
from bplustree import BPlusTree, UUIDSerializer
import Claim from claim
import sys
import io

class BplusTree(nn.Module):

    def __init__(self, height, order, rootorder, ref_text_dict):
        # claim is a List Claim object, which is parsed from the input by the client.
        super(BplusTree, self).__init__()
        self.height = height
        self.order = order
        self.rootorder = rootorder
        self.root = []
        for ref, text in ref_text_dict.items():
            self.root.append(Claim(ref, text))
    

    def set_tree(self, height = 0, node = root):
        for claim in node:
            if height < self.height:
                set_tree(height + 1, claim.parse_child())

def main():
    """ Main func.
    """
    set_tree()

if __name__ == '__main__':
    main()    