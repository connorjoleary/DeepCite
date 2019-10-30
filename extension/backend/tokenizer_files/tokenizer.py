import spacy
from spacy.parts_of_speech import  PUNCT, PROPN
from spacy.lang.en import English
import queue as q
import os

CWD_FOLDER = os.path.dirname(os.path.abspath(__file__))

# loads english library into space
# other libraries can be used for better accuracy
# en_core_web_md
# en_core_web_lg
# google news pre-trained network: https://code.google.com/archive/p/word2vec/ 
nlp = spacy.load("en_core_web_sm")
nlps = English()
nlps.add_pipe(nlps.create_pipe('sentencizer'))
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

# prints priority queue - mostly for testing purposes
def print_queue(queue):
    while not queue.empty():
        print( queue.get() )

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

# parses through sentences in a given paragraph
def sentence_parsing(text):
    sentences = []
    for num, paragraph in enumerate(text):
        doc3 = nlps(paragraph)
        for sent in doc3.sents:
            sentence = sent.text.strip().replace('\t', '').replace("\n", '')
            if len(sentence) > 0:
                sentences.append(sentence)
    return sentences

# claim will the the claim for comparison
# text is the text of the article, preferably paragraph by paragraph
def predict(claim, text) :

    queue = q.PriorityQueue()

    clean_claim = preprocessing(nlp(claim))
    doc1 = nlp(clean_claim)

    # compares claim to individual paragraphs
    for num, paragraph in enumerate(text):
        clean_paragraph = preprocessing(nlp(paragraph))
        doc2 = nlp(clean_paragraph)
        queue.put(Paragraph(num, doc1.similarity(doc2)))

    best_paragraph = queue.get()

    # compares to individual sentences
    sentence_queue = q.PriorityQueue()
    sentences = sentence_parsing(text)

    for num, sentence in enumerate(sentences):
        clean_sent = preprocessing(nlp(sentence))
        doc3 = nlp(clean_sent)
        sentence_queue.put(Paragraph(num, doc1.similarity(doc3)))
    
    best_sentence = sentence_queue.get()

    predict = text[best_paragraph.index] if best_paragraph.similarity > best_sentence.similarity else sentences[best_sentence.index]
    # test is solely for testing purposes, checks the return values
    test.append((claim, predict))

    return predict




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