from tree import Tree
from pathlib import Path
# Link 0 doesn't work because the references split the text into several parts.
# Therefore there is a keyerror.
urls = []
def test():
    for line in open(Path('testing_set/links.txt')).readlines():
        urls.append(line)
    claims = []
    for line in open(Path('testing_set/claims.txt')).readlines():
        claims.append(line)
    for i in range(len(claims)):
        url = urls[i]
        claim = claims[i]
        tree = Tree(url, claim)
        print("Try {}".format(i))
        print(tree.get_best_path())

def main():
    url = "https://en.wikipedia.org/wiki/Doro_(musician)"
    claim = "Doro is a nickname for the German name Dorothee, so now I know how the heavy metal singer, Doro, former front-woman for Warlock, got her name"
    tree = Tree(url, claim)
    print(tree.get_best_path())   

if __name__=='__main__':
    main()