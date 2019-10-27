import spacy
from spacy.parts_of_speech import  PUNCT, PROPN
import queue as q
import os

CWD_FOLDER = os.path.dirname(os.path.abspath(__file__))

# loads english library into space
# other libraries can be used for better accuracy
# en_core_web_md
# en_core_web_lg
# google news pre-trained network: https://code.google.com/archive/p/word2vec/ 
nlp = spacy.load("en_core_web_sm")
# importing different vectors for similiarites - word2vec
# training dataset
# nlp = spacy.load('en_core_web_sm', vectors='<directory>') 

# solely for testing purposes
test = []

class Paragraph(object):
    def __init__(self, index, similarity):
        self.index = index
        self.similarity = similarity
    
    def __lt__(self, other):
        # comparison in largest to smalled
        return not (self.similarity < other.similarity)
    # for testing
    def __repr__(self):
        return "index: " + str(self.index) + " similarity: " + str(self.similarity)


# any preprocessing of data if necessary
# remove punctuation - all lower case, lemmanization
def preprocessing(doc):
    clean_claim = []
    for token in doc:
        add = token.text
        if token.pos == PUNCT:
            add = ""
        elif token.pos != PROPN:
            add = token.lower_
        elif not token.is_stop:
            add = token.lemma_
        clean_claim.append(add)
    return " ".join(x for x in clean_claim if x != "")



# claim will the the claim for comparison
# text is the text of the article, preferably paragraph by paragraph
def predict(claim, text) :

    queue = q.PriorityQueue()

    #print(claim)
    clean_claim = preprocessing(nlp(claim))
    #print(clean_claim)
    doc1 = nlp(clean_claim)

    for num, paragraph in enumerate(text):
        clean_paragraph = preprocessing(nlp(paragraph))
        doc2 = nlp(clean_paragraph)
        queue.put(Paragraph(num, doc1.similarity(doc2)))

    index = queue.get().index
    predicted = text[index]
    # soley for testing purposes
    #test.append((claim, text[index]))

    # while not queue.empty():
        # print( queue.get() )
    # TODO: test for setence accuracy in paragraph(?)
    return predicted




# for testing purposes
if "__main__":
    
    test_set_claims = os.path.join(CWD_FOLDER, 'testing_set', 'claims.txt')
    f_claim = open(test_set_claims, 'r', errors='replace')

    claims = [line for line in f_claim]
    f_claim.close()

    for num, claim in enumerate(claims):
        test_set_links = os.path.join(CWD_FOLDER, 'testing_set', 'link')
        f_text = open(test_set_links+ str(num) + ".txt", 'r', errors='replace')

        text = [paragraph for paragraph in f_text]
        f_text.close()

        predict(claim, text)
        #print("\nNext set: \n")

    file_path = os.path.join(CWD_FOLDER, 'test-file.txt')
    test_file = open(file_path, 'w+', errors='replace')
    for x in test:
        test_file.write(str(x) + '\n\n\n\n\n\n')
    test_file.close()