from gensim.models.word2vec import Word2Vec
from gensim.models import KeyedVectors
model = KeyedVectors.load_word2vec_format('word_vectors/GoogleNews-vectors-negative300.bin', binary=True)
model.save_word2vec_format('word_vectors/googlenews.txt')

# cd word_vectors
# gzip googlenews.txt    

# python3 -m spacy init-model en ./googlenews.model --vectors-loc googlenews.txt.gz
