from __future__ import absolute_import, unicode_literals
from api.models import *
import time, math

from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import tokenize
from nltk.tokenize.treebank import TreebankWordTokenizer
from nltk.stem.snowball import SnowballStemmer

from pyhtmm.utils import load_pickle
from pyhtmm.process import process_doc

sid = SentimentIntensityAnalyzer()
htmm = load_pickle('./htmm_trained_model.pickle')

idx_topic = [
    "Screen Size",
    "Graphics Coprocessor",
    "Processor",
    "RAM",
    "Operating System",
    "Hard Drive",
    "Number of USB 3.0 Ports",
    "Average Battery Life (in hours)",
]

import gensim, json, pickle, re, torch
import numpy as np

model = torch.load('./encoder/infersent.allnli.pickle')
centers = pickle.load(open('./data/centers.pickle', 'rb'))
model.set_glove_path('./data/glove.840B.300d.txt')
model.build_vocab_k_words(K=100000)

def keyword_match(properties, reviews):
    ret = []

    for p in properties:
        text = p["text_content"]
        p_word = [" " + word.lower() + " " for word in text.split(" ")]
        for review in reviews:
            if not isinstance(review["content"], str): continue
            sentences = tokenize.sent_tokenize(review["content"])
            dct = {}
            maxCount = 0
            best_sentence = ''
            for i in range(len(sentences)):
                count = sum(1 for w in p_word if w in sentences[i].lower())
                if count > maxCount:
                    maxCount = count
                    best_sentence = sentences[i]
            if maxCount >= 5:
                ps = sid.polarity_scores(best_sentence.lower())['compound']
                ret.append({
                    'related_property_id': p["id"],
                    'best_sentence': best_sentence,
                    'related_review_id': review["id"],
                    'sentiment': ps,
                })

    find_cluster(ret)
    return ret

def htmm_inference(properties, reviews):
    ret = []

    idx_id = [""] * len(idx_topic)
    for p in properties:
        for i in range(len(idx_topic)):
            if idx_topic[i] == p["topic"]: idx_id[i] = p["id"]

    for review in reviews:
<<<<<<< HEAD:amazon_review/api/matcher.py
        doc = process_doc(review["content"])
        path, entropy = htmm.predict_topic(doc)
        for i, stn in enumerate(doc.sentence_list):
            if entropy[i] >= 0.1: continue
            ps = sid.polarity_scores(stn.raw_content.lower())['compound']
            ret.append({
                'related_property_id': idx_id[path[i] % 8],
                'best_sentence': stn.raw_content,
                'related_review_id': review["id"],
                'sentiment': ps,
            })

    find_cluster(ret)
=======
        if not isinstance(review["content"], str): continue
        sentences = tokenize.sent_tokenize(review["content"])

        for sentence in sentences:
            tmp = [ss.stem(w.lower()) for w in twt.tokenize(sentence)]
            words = ["NUM" if w.isdigit() else w for w in tmp]
            for p in properties:
                score = 0
                for w in words:
                    if p["topic"] in topics and w in topics[p["topic"]]:
                        score += math.log(topics[p["topic"]][w])
                perplexity = math.exp(-score / len(words))
                if perplexity > 3.0:
                    ps = sid.polarity_scores(sentence.lower())['compound']
                    ret.append({'related_property_id': p["id"], 'best_sentence': sentence, 'related_review_id': review["id"], 'sentiment': ps})
>>>>>>> 6a4bde0d5efddde89ab6d5ac0522baa24f58dfd5:amazon_review/api/utils/matcher.py
    return ret

def find_cluster(relationships):
    margin = float('inf') ## Need testing
    for relationship in relationships:
        embeded_sentence = model.encode(review, bsize=128, tokenize=True, verbose=True)
        closest_cluster = None
        closest_dist = float('inf')
        for cluster in centers[relationships['related_property_id']]:
            dist = numpy.linalg.norm(center, embeded_sentence)
            if closest_dist > dist && dist < margin :
                 closest_cluster = cluster
                 ## Need definition of closest cluster in what kind of format
                 ## id? key words? Or anything else
        relationship["sub_cluster"] = closest_cluster
    return
