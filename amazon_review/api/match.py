from api.models import *

def keyword_match(properties, reviews):
    ret = []
    for property in properties:
        text = property.text_content;
        print(text)
        property_word = [" " + word.lower() + " " for word in text.split(" ")]
        for review in reviews:
            sentences = review.content.lower().split('.')
            dct = {}
            for sentence in sentences:
                dct[sentence] = sum(1 for word in property_word if word in sentence)
            best_sentences = [key for key,value in dct.items() if value == max(dct.values())]
            if dct[best_sentences[0]] > len(property_word) / 2:
                ret.append({'related_property': property, 'best_sentence': best_sentences[0], 'related_review': review})
    return ret
