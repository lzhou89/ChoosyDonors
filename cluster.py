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
 
# Works to add different files to a list for processing 
# def article_list(path):
#     articles = []
#     for subdir, dirs, files in os.walk(path):
#         for file in files:
#             file_path = subdir + os.path.sep + file
#             essay = open(file_path, 'r')
#             text = essay.read()
#             articles.append(text)
#     return articles

def article_id_list():
    """Create list of tuples of all fulfillment trailers & project ids"""
    articles_ids = model.session.query(model.Project).with_entities(
                   model.Project.id, model.Project.fulfillment_trailer).all()
    return articles_ids

def article_list(list):
    """Creates a list of just articles"""
    articles = []
    for item in list:
        articles.append(item[1])
    return articles

def id_list(list):
    """Creates a list of just ids"""
    ids = []
    for item in list:
        ids.append(item[0])
    return ids

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
 
 
def cluster_texts(texts, clusters=100):
    """ Transform texts to Tf-Idf coordinates and cluster texts using K-Means """
    vectorizer = TfidfVectorizer(tokenizer=process_text,
                                 stop_words=stopwords.words('english'),
                                 max_features=1000,
                                 lowercase=True)
 
    tfidf_model = vectorizer.fit_transform(texts)
    terms = vectorizer.get_feature_names()
    features = dict(zip(terms, tfidf_model.data))
    print features
    km_model = KMeans(n_clusters=clusters)
    km_model.fit(tfidf_model)
 
    clustering = collections.defaultdict(list)
 
    for idx, label in enumerate(km_model.labels_):
        clustering[label].append(idx)
 
    return clustering
 
 
if __name__ == "__main__":
    prelim = article_id_list()
    articles = article_list(prelim)
    ids = id_list(prelim)
    with open('ids.txt', 'w') as f:
        for item in ids:
            item = item.encode('utf-8')
            f.write("%s\n" % item)
    # print articles[0:5]
    # print ids[0:5]
    clusters = cluster_texts(articles)
    with open('clusters.txt', 'w') as out:
        pprint(dict(clusters), stream=out)