import string
import nltk
 
from nltk import word_tokenize
# from nltk.stem import PorterStemmer
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords
import model

def article_list():
    # id = model.session.query(model.Project).with_entities(model.Project.col1).all()
    # synopses = model.session.query(model.Project).with_entities(model.Project.col13).all()
    articles = model.session.query(model.Project).with_entities(model.Project.fulfillment_trailer).all() #fulfillment trailer column
    return articles

def corpus(articles):
	new_list = []
	all_articles = ""
	for article in articles:
		# all_articles = all_articles + " " + article[0] 
		new_list.append(article[0])
	all_articles = " ".join(new_list)
	all_articles = all_articles.lower()
	all_articles = all_articles.encode('utf-8')
	all_articles = all_articles.translate(None, string.punctuation)
	all_articles = all_articles.decode('utf-8')
	return all_articles

def normalize(string):
	stop_words = stopwords.words('english')
	stemmer = SnowballStemmer('english')
	tokens = word_tokenize(string)
	tokens = [word for word in tokens if word not in stop_words]
	# tokens = [stemmer.stem(word) for word in tokens]
	return tokens

def count_frequencies(tokens):
	text = nltk.Text(tokens)
	fdist = nltk.FreqDist(text)
	print type(fdist)
	# words = fdist.keys()
	# top_words = words[:100]
	top_words = fdist.most_common(50)
	return top_words

if __name__ == "__main__":
    articles = article_list()
    # print type(articles)
    # print type(articles[0][0])
    print "article_list complete"
    all_articles = corpus(articles)
    print "corpus complete"
    tokens = normalize(all_articles)
    print "normalize complete"
    top_words = count_frequencies(tokens)
    # print top_words