import gensim
from gensim import corpora
from nltk.corpus import stopwords

def article_id_list():
    # id = model.session.query(model.Project).with_entities(model.Project.col1).all()
    # synopses = model.session.query(model.Project).with_entities(model.Project.col13).all()
    articles_ids = model.session.query(model.Project).with_entities(model.Project.id, model.Project.fulfillment_trailer).all()
    return articles_ids

def article_list(list):
    articles = []
    for item in list:
        articles.append(item[1])
    return articles

def corpus(articles):
	all_articles = []
	for article in articles:
		all_articles.append(article[0])
	return all_articles

def normalize(articles):
	stop_words = stopwords.words('english')
	texts = [[word for word in article.lower().split() if word not in stop_words] for article in articles]
	dictionary = corpora.Dictionary(texts)
	corpus = [dictionary.doc2bow(text) for text in texts]

	# tfidf = models.TfidfModel(corpus, #id2word=dicionary)
	# corpus_tfidf = tfidf[corpus]
	##tdidf_corpus = MmCorpus(corpus=corpus_tfidf, id2word=dictionary)

	lda = gensim.models.ldamodel.LdaModel(corpus=corpus, id2word=dictionary, num_topics=20)

	lda.print_topics(20)
    # return "Ok"


if __name__ == "__main__":
    prelim = article_id_list()
    articles = article_list(prelim)
    # print type(articles)
    # print type(articles[0][0])
    print "article_list complete"
    all_articles = corpus(articles)
    print "corpus complete"
    normalize(all_articles)
    print "normalize complete"
    # print top_words


# using lda module
# array creation
# get list of all words
# get count per document as a list
# add that list to list of counting lists
# make matrix np.array(master list)