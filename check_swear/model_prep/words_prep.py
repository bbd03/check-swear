import json
from importlib import resources

def load_transliteration_dict():
    with resources.open_text('check_swear.model_prep', 'words.json') as file:
        translit_dict = json.load(file)["transliteration_dict"]
    return translit_dict

def load_stemmed_words():
    with resources.open_text('check_swear.model_prep', 'words.json') as file:
        stemmed_words = json.load(file)["stemmed_words"]
    return stemmed_words
