import warnings
import re
import joblib
from importlib import resources
from ..model_prep.words_prep import load_stemmed_words
from ..model_prep.tokenizer import ChatTokenization

class Validate:
    
    """
    Provides validation methods for input data to ensure it meets the requirements
    or expectations before processing.

    Methods
    -------
    string_validation(input_text, bins):
        Validates the 'bins' parameter against the length of 'input_text'. Adjusts
        'bins' if it exceeds the number of words in 'input_text'.

    array_validation(input_text):
        Validates if all elements in 'input_text' are strings. Useful for ensuring
        consistent input data type.
    """
    
    @staticmethod
    def string_validation(input_text, bins):
        if bins is None:
            pass
        else:
            text_len = len(input_text.split())
            if text_len < bins:
                warnings.warn(
                    f"Bins amount is larger than the input_text, bins value is set to {text_len}"
                )
                bins = text_len
                
        return bins
    
    @staticmethod
    def array_validation(input_text):       
        if input_text is None:
            return True
        for string in input_text:
            if not isinstance(string, str):
                return False
        return True
         
            
class Preprocess:
    
    """
    Contains methods for preprocessing text data, including segmentation and
    preparation for further analysis or modeling.

    Methods
    -------
    string_prep(input_text, bins):
        Splits a string into specified bins or segments.

    array_prep(input_text):
        Prepares an array of strings for processing, maintaining its structure.
    """
    
    @staticmethod
    def string_prep(input_text, bins):
        if bins is None:
            # convert everything to an array
            return [input_text]
        
        split_str = input_text.split()
        str_len = len(split_str)
        bin_step = str_len // bins
        
        text_arr = [' '.join(split_str[i * bin_step: min((i + 1) * bin_step, str_len)]) for i in range(bins)]
        remaining_words = str_len % bins
        
        if remaining_words > 0:
            text_arr[-1] += ' ' + ' '.join(split_str[-remaining_words:])
        
        return text_arr
    
    @staticmethod
    def array_prep(input_text):
        text_arr = [i for i in iter(input_text)]
        return text_arr


class RegularExpr:
    
    """
    Utilizes regular expressions for analyzing text data, including searching for
    patterns and extracting relevant information.

    Methods
    -------
    analyze(input_text, strong_pattern, weak_pattern):
        Applies strong and weak pattern matching to input text and returns a
        boolean mask indicating matches.

    concatenate(stop_words):
        Combines a list of stop words with a preloaded list, preparing it for
        pattern generation.

    get_patterns(stop_words):
        Generates strong and weak regular expression patterns from a list of
        stop words.
    """
    
    @staticmethod
    def analyze(input_text, strong_pattern, weak_pattern):
        # strong stemmatization
        stok = ChatTokenization(remove_stopwords=False, delete_unigrams=False)
        strong_stemmed_input_text = list(map(lambda string: ''.join(stok.tokenizer(string)), input_text))
        
        # weak stemmatization
        wtok = ChatTokenization() 
        weak_stemmed_input_text = list(map(lambda string: ' '.join(wtok.tokenizer(string)), input_text))
        
        strong_bool_mask = list(map(lambda string: strong_pattern.search(string), strong_stemmed_input_text))
        weak_bool_mask = list(map(lambda string: weak_pattern.search(string), weak_stemmed_input_text))
        
        bool_mask = [bool(s) + bool(w) for s, w in zip(strong_bool_mask, weak_bool_mask)]
        return bool_mask
    
    @staticmethod
    def concatenate(stop_words):
        stemmed_words = load_stemmed_words()
        if stop_words is None:
            return stemmed_words
        
        tok = ChatTokenization()
        stemmed_stop_words = tok.tokenizer(' '.join(stop_words))
        return stemmed_words + stemmed_stop_words
    
    
    @staticmethod
    def get_patterns(stop_words):
        strong_pattern = '|'.join(stop_words)
        strong_compiled_pattern = re.compile(strong_pattern)
        
        weak_pattern = r'\b(' + '|'.join(stop_words) + r')\b'
        weak_compiled_pattern = re.compile(weak_pattern)
        
        return (strong_compiled_pattern, weak_compiled_pattern)
        

def vectorizer_load():
    with resources.path('check_swear.data', 'vectorizer.joblib') as vectorizer_path:
        vectorizer = joblib.load(vectorizer_path)
        return vectorizer
    
def model_load():
    with resources.path('check_swear.data', 'model.joblib') as model_path:
        model = joblib.load(model_path)
        return model