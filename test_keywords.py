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
	all_articles = ""
	for article in articles:
		all_articles = all_articles + " " + article 
	all_articles = all_articles.lower.translate(None, string.punctuation)
	return all_articles

def normalize(string):
	stop_words = stopwords.words('english')
	stemmer = SnowballStemmer('english')
	tokens = word_tokenize(string)
	tokens = [word for word in tokens if word not in stop_words]
	tokens = [stemmer.stem(word) for word in tokens]
	return tokens

def count_frequencies(tokens):
	text = nltk.Text(tokens)
	fdist = nltk.FreqDist(text)
	words = fdist.keys()
	top_words = words[:100]
	return top_words

if __name__ == "__main__":
    articles = article_list()
    print "article_list complete"
    all_articles = corpus(articles)
    print "corpus complete"
    tokens = normalize(all_articles)
    print "normalize complete"
    top_words = count_frequencies(tokens)
    print top_words