import string
import collections
import os
 
from nltk import word_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from pprint import pprint
import model
 
 
# def article_list(path):
#     articles = []
#     for subdir, dirs, files in os.walk(path):
#         for file in files:
#             file_path = subdir + os.path.sep + file
#             essay = open(file_path, 'r')
#             text = essay.read()
#             articles.append(text)
#     return articles

def article_list():
    # id = model.session.query(model.Project).with_entities(model.Project.col1).all()
    # synopses = model.session.query(model.Project).with_entities(model.Project.col13).all()
    articles = model.session.query(model.Project).with_entities(model.Project.col12).all() #fulfillment trailer column
    return articles

def process_text(text, stem=True):
    """ Tokenize text and stem words removing punctuation """
    text = text.encode("utf-8")
    text = text.translate(None, string.punctuation)
    text = text.decode("utf-8")
    tokens = word_tokenize(text)
 
    if stem:
        stemmer = PorterStemmer()
        tokens = [stemmer.stem(t) for t in tokens]
 
    return tokens
 
 
def cluster_texts(texts, clusters=3):
    """ Transform texts to Tf-Idf coordinates and cluster texts using K-Means """
    vectorizer = TfidfVectorizer(tokenizer=process_text,
                                 stop_words=stopwords.words('english'),
                                 max_df=0.5,
                                 min_df=0.1,
                                 lowercase=True)
 
    tfidf_model = vectorizer.fit_transform(texts)
    km_model = KMeans(n_clusters=clusters)
    km_model.fit(tfidf_model)
 
    clustering = collections.defaultdict(list)
 
    for idx, label in enumerate(km_model.labels_):
        clustering[label].append(idx)
 
    return clustering
 
 
if __name__ == "__main__":
    articles = article_list('Test_Essays')
    clusters = cluster_texts(articles)
    pprint(dict(clusters))