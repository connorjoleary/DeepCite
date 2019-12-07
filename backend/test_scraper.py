from tree import Tree
from controller import Claim

# Link 0 doesn't work because the references split the text into several parts.
# Therefore there is a keyerror.
url = "https://en.wikipedia.org/wiki/Doro_(musician)"
text = "Doro is a nickname for the German name Dorothee, so now I know how the heavy metal singer, Doro, former front-woman for Warlock, got her name"
root = Claim(url, text)
tree = Tree(root)
print(tree.tofront())