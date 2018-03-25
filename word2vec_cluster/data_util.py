import gensim, json
import numpy as np
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from sklearn.cluster import KMeans

def sentence_to_array(file):
    data = json.load(open(file))
    stopset = set(stopwords.words('english'))
    tokenizer = RegexpTokenizer(r'\w+')
    ret = {}
    for topic in data['payload']:
        ret[topic['topic']] = []
        for review in topic['reviews']:
            tokens = tokenizer.tokenize(review['content'])
            tokens = [w for w in tokens if not w in stopset]
            ret[topic['topic']].append(tokens)
    return ret

def load_to_vec(sentences):
    global model
    ret = {}
    for topic in sentences:
        ret[topic] = []
        for sentence in sentences[topic]:
            sentence_vec = [model[word] for word in sentence if word in model]
            ret[topic].append(np.mean(np.array(sentence_vec), axis = 0))
        ret[topic] = np.array(ret[topic])
    return ret

def load_uniform_vec(sentences):
    global model
    ret = []
    for topic in sentences:
        for sentence in sentences[topic]:
            sentence_vec = [model[word] for word in sentence if word in model]
            ret.append(np.mean(np.array(sentence_vec), axis = 0))
    ret = np.array(ret)
    return ret

def cluster(sentence_vec):
    global model
    kmeans = KMeans(n_clusters=6, random_state=0).fit(sentence_vec)
    print(kmeans.labels_)
    for center in kmeans.cluster_centers_:
        print(model.most_similar(positive=[center], topn=5))

print("Loading GoogleNews_word2vec...")
model = gensim.models.KeyedVectors.load_word2vec_format('./data/GoogleNews-vectors-negative300.bin', binary=True)
print("Finish Loading")
ret = load_uniform_vec(sentence_to_array("data/sample.json"))
cluster(ret)
# for topic in ret:
#     if len(ret[topic]) > 5:
#         print(topic)
#         cluster(ret[topic])
