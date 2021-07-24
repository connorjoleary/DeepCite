import spacy
from spacy.parts_of_speech import  PUNCT, PROPN
from spacy.lang.en import English
from spacy.tokenizer import Tokenizer
from config import config
import queue as q
import os

nlp = spacy.load('en_core_web_lg')

def custom_tokenizer(nlp):

    prefixes_re = spacy.util.compile_prefix_regex(nlp.Defaults.prefixes)

    custom_infixes = ['\.\.\.+', '(?<=[0-9])-(?=[0-9])', '[?!&,:()]']
    infix_re = spacy.util.compile_infix_regex(tuple(list(nlp.Defaults.infixes) + custom_infixes))

    suffix_re = spacy.util.compile_suffix_regex(nlp.Defaults.suffixes)   

    return Tokenizer(nlp.vocab, nlp.Defaults.tokenizer_exceptions,
                     prefix_search = prefixes_re.search, 
                     infix_finditer = infix_re.finditer, suffix_search = suffix_re.search,
                     token_match=None)


nlp.tokenizer = custom_tokenizer(nlp)
nlp.add_pipe(nlp.create_pipe('sentencizer'))

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
        doc3 = nlp(paragraph)
        for sent in doc3.sents:
            sentence = sent.text.strip().replace('\t', '').replace("\n", '')
            if len(sentence) > 0:
                sentences.append(sentence)
    return sentences

def predict(claim, text) : #TODO: this doesn't take into account the original claim, this happens in beam_search in Tree, but it might be better here
    """ Finds the best matches to a given claim

    claim - the claim for comparison
    text - the text of the article, preferably paragraph by paragraph
    predict - list of sentences and similarities sorted by most similar
    """

    paragraph_queue = q.PriorityQueue()

    clean_claim = preprocessing(nlp(claim))
    doc1 = nlp(clean_claim)

    # compares claim to individual paragraphs
    for num, paragraph in enumerate(text):
        clean_paragraph = preprocessing(nlp(paragraph)) #TODO:why does nlp run twice
        doc2 = nlp(clean_paragraph)
        similarity = doc1.similarity(doc2) #TODO: this would probably be better with tfidf vector
        paragraph_queue.put(Paragraph(num, similarity))

    # compares to individual sentences
    sentence_queue = q.PriorityQueue()
    sentences = sentence_parsing(text)

    for num, sentence in enumerate(sentences):
        clean_sent = preprocessing(nlp(sentence))
        doc3 = nlp(clean_sent)
        similarity = doc1.similarity(doc3)
        sentence_queue.put(Paragraph(num, similarity))

    predict = []
    best_paragraph = paragraph_queue.get()
    best_sentence = sentence_queue.get()
    k = config['model']['num_claims_returned']
    for i in range(k):
        if best_paragraph.similarity > best_sentence.similarity:
            if len([True for prediction in predict if prediction[0] in text[best_paragraph.index]]) > 0: # There is already part of the top paragraph being returned
                i = i-1
            else:
                predict.append((text[best_paragraph.index], best_paragraph.similarity))
            if paragraph_queue.not_empty:
                best_paragraph = paragraph_queue.get()
            else:
                best_paragraph = Paragraph(0, -10)
        else:
            if len([True for prediction in predict if sentences[best_sentence.index] in prediction[0]]) > 0: # Part of the top sent is already contained in the return
                i = i-1
            else:
                predict.append((sentences[best_sentence.index], best_sentence.similarity))

            if paragraph_queue.not_empty:
                best_sentence = sentence_queue.get()
            else:
                best_sentence = Paragraph(0, -10)
        if best_paragraph == -10 and best_sentence == -10:
            break

    return predict
