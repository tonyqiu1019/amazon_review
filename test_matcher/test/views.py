from django.shortcuts import render
from django.http import JsonResponse, HttpResponse

def match(request):
    query = request.POST.dict()
    properties = query["properties"]
    reviews = query["reviews"]
    relationships = keyword_match(properties, reviews)
    return JsonResponse(relationships)


def keyword_match(properties, reviews):
    sid = SentimentIntensityAnalyzer()
    ret = []

    for p in properties:
        text = p["text_content"];
        property_word = [" " + word.lower() + " " for word in text.split(" ")]
        for review in reviews:
            if not isinstance(review["content"], str): continue
            sentences = tokenize.sent_tokenize(review["content"])
            dct = {}
            maxCount = 0
            best_sentence = ''
            for i in range(len(sentences)):
                count = sum(1 for word in property_word if word in sentences[i].lower())
                if count > maxCount:
                    maxCount = count
                    best_sentence = sentences[i]
            if maxCount >= 5:
                ps = sid.polarity_scores(best_sentence.lower())['compound']
                ret.append({'related_property_id': p["id"], 'best_sentence': best_sentence, 'related_review_id': review["id"], 'sentiment': ps})

    return ret
