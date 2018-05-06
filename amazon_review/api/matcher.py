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
    return ret
