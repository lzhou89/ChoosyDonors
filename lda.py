import gensim
from gensim import corpora, models
from nltk.corpus import stopwords
import model

def article_id_list():
    # id = model.session.query(model.Project).with_entities(model.Project.col1).all()
    articles_ids = model.session.query(model.Project).with_entities(model.Project.id, model.Project.synopsis).all()
    # articles_ids = model.session.query(model.Project).with_entities(model.Project.id, model.Project.fulfillment_trailer).limit(100000)
    return articles_ids

def article_list(list):
    articles = []
    for item in list:
        articles.append(item[1])
    return articles

def id_list(list):
    ids = []
    for item in list:
        ids.append(item[0])
    return ids

def corpus(articles):
	all_articles = []
	for article in articles:
		all_articles.append(article)
	return all_articles

def normalize(articles, ids):
    stop_words = stopwords.words('english')
    # sep = "including"
    # for i in range(len(articles)):
    #     articles[i] = articles[i].split(sep)[0]

    texts = [[word for word in article.lower().split() if word not in stop_words] for article in articles]
    for word in texts:
        if word[:2] == "\n":
            word = word[2:]
    texts = [word for word in texts if word not in stop_words]
    print "texts done"
    # for article in articles:
    #     for word in article:
    #         if word[:2] == "\n":
    #             word = word[2:]
    #         if word not in stop_words:
    #             texts.append(word)
    dictionary = corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(text) for text in texts]

    tfidf = models.TfidfModel(corpus, id2word=dictionary)
    corpus_tfidf = tfidf[corpus]
    # tdidf_corpus = corpora.MmCorpus(corpus_tfidf)#, id2word=dictionary)

    lda = gensim.models.ldamodel.LdaModel(corpus=corpus_tfidf, id2word=dictionary, num_topics=100)

    lda.print_topics(20)

    # with open('topics.csv', 'w') as f:
    #     write_to_file = lda.print_topics(20)
    #     f.write(write_to_file)
    logfile = open('...topics.txt', 'w')
    print>>logfile, lda.show_topics(100)

    with open('clusters.csv', 'w') as f:
        for i in range(5000):
            probs = lda[dictionary.doc2bow(articles[i].lower().split())]
            topic = -1
            probability = 0
            for item in probs:
                if item[1] > probability:
                    probability = item[1]
                    topic = item[0]
            # write_to_file = str(i) + ", " + ids[i] + ", " + str(lda[dictionary.doc2bow(articles[i].lower().split())]) + "\n"
            write_to_file = str(i) + ", " + ids[i] + ", " + str(topic) + ", " + str(probability) + "\n"
            f.write(write_to_file)

    return "Ok"





if __name__ == "__main__":
    prelim = article_id_list()
    articles = article_list(prelim)
    print "article_list complete"
    ids = id_list(prelim)
    print ids[:5]
    print len(ids)
    all_articles = corpus(articles)
    print "corpus complete"
    normalize(all_articles, ids)
    print "normalize complete"
    # print top_words


# using lda module
# array creation
# get list of all words
# get count per document as a list
# add that list to list of counting lists
# make matrix np.array(master list)