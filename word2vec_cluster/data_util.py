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

def load_console(file):
    with open(file) as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    stopset = set(stopwords.words('english'))
    tokenizer = RegexpTokenizer(r'\w+')
    ret = [[] for i in range(15)]
    for j in range(1000):
        tokens = tokenizer.tokenize(content[j * 2])
        tokens = [w for w in tokens if not w in stopset]
        ret[int(content[2 * j + 1]) % 15].append(tokens)
    # print(len(ret))
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
    print(ret)
    return ret

def load_uniform_vec(sentences):
    global model
    ret = [[] for i in range(15)]
    i = 0
    for topic in sentences:
        for sentence in topic:
            sentence_vec = [model[word] for word in sentence if word in model]
            ret[i].append(np.mean(np.array(sentence_vec), axis = 0))
        i += 1
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
ret = load_uniform_vec(load_console("data/consoleOutput.txt"))
for topic in ret:
    print(topic)
    cluster(topic)
# ret = load_uniform_vec(sentence_to_array("data/sample.json"))
# cluster(ret)
# for topic in ret:
#     if len(ret[topic]) > 5:
#         print(topic)
#         cluster(ret[topic])
