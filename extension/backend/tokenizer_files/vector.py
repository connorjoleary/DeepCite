from gensim.test.utils import common_texts, get_tmpfile
from gensim.models import Word2Vec, KeyedVectors
import pandas as pd
import os

CWD_FOLDER = os.path.dirname(os.path.abspath(__file__))


def preprocessing_dataset(data):
    return [x.replace('\t', '').replace("\n", '').split(' ') for x in data]

# dummy dataset for model training
def train_vector(file_model, sentences, update):
    # model = KeyedVectors.load_word2vec_format('googlenews.bin', binary=True)
    # load pre-trained model
    model = Word2Vec.load(file_model)
    model.train(sentences, total_examples=model.corpus_count, epochs=model.epochs)

    # update model in directory
    if update:
        file_save = os.path.join(CWD_FOLDER, 'datasets', 'word2vec', f_name+'.txt')
        model.wv.save_word2vec_format(file_save)
        file_save = os.path.join(CWD_FOLDER, 'datasets', 'word2vec', f_name+'.model')
        model.save(file_save)
    
    return model
    

# create a model
def create_model(f_name, dataset, min_count, size):
    file_path = os.path.join(CWD_FOLDER, 'datasets', 'word2vec', f_name+'.model')
    path = get_tmpfile(file_path)

    model = Word2Vec(dataset, min_count=min_count,size=size)
    
    file_save = os.path.join(CWD_FOLDER, 'datasets', 'word2vec', f_name+'.txt')
    model.wv.save_word2vec_format(file_save)
    file_save = os.path.join(CWD_FOLDER, 'datasets', 'word2vec', f_name+'.model')
    model.save(file_save)

    return model


# testing purposes
if "__main__":
    f_name = 'redditWorldNews'
    f_type = '.csv'
    file_path = os.path.join(CWD_FOLDER, 'datasets', f_name + f_type )
    
    df = pd.read_csv(file_path)
    newsVec = preprocessing_dataset(df['title'].values)

    create_model(f_name, newsVec, 1, 32)

    file_model = file_path = os.path.join(CWD_FOLDER, 'datasets', 'word2vec', f_name+'.model')
    model = train_vector(file_model, common_texts, True)
    print(model.most_similar(positive=['woman', 'King'], negative=['man']))