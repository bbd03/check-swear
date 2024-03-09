import re
import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords
from .words_prep import load_transliteration_dict

class ChatTokenization:
    
    """
    Performs tokenization specifically tailored for chat messages or similar texts in the Russian language. This class supports several preprocessing steps including transliteration, handling of long vowels, removal of stopwords, deletion of unigrams (single letters), and stemming.

    Parameters
    ----------
    language : str, default='russian'
        The language used for stemming and stopword removal. Currently, only 'russian' is directly supported.
    
    stemming_use : bool, default=True
        If True, enables stemming of tokens using the SnowballStemmer for the specified language.
    
    remove_stopwords : bool, default=True
        If True, removes stopwords based on the specified language's stopwords list from nltk.corpus.
    
    delete_unigrams : bool, default=True
        If True, removes single-character tokens from the token list.
    
    long_vowels_handle : bool, default=True
        If True, shortens sequences of three or more identical characters to a single character, addressing potential exaggerations in text (e.g., "heeeello" becomes "hello").

    Attributes
    ----------
    stemmer : SnowballStemmer or None
        The stemmer instance initialized based on the specified language if stemming is enabled; otherwise, None.
    
    russian_stopwords : list of str or None
        A list of stopwords for the specified language if stopword removal is enabled; otherwise, None.

    Methods
    -------
    tokenizer(text):
        Tokenizes the input text after applying transliteration, long vowel handling, stopword removal, unigram deletion, and stemming based on the class configuration.

    Examples
    --------
    >>> tokenizer = ChatTokenization()
    >>> tokenizer.tokenizer("Пример текста с длинныыыми гласными и смайликами :-) !!!")
    ['пример', 'текст', 'гласный', 'смайлик']

    Notes
    -----
    This class is specifically designed for processing Russian text, particularly in informal contexts such as chat messages. Adjustments or extensions may be required for use with other languages or formal texts.
    """

    def __init__(self, language='russian', stemming_use=True, remove_stopwords=True, delete_unigrams=True, long_vowels_handle=True):
        """
        Initializes the ChatTokenization class with the specified configuration for text preprocessing and tokenization.
        """
    
    def __init__(
        self,
        language='russian',
        stemming_use=True,
        remove_stopwords=True,
        delete_unigrams=True,
        long_vowels_handle=True
    ):
        
        self.language = language
        self.stemming_use = stemming_use
        self.stemmer = SnowballStemmer(language) if self.stemming_use else None
        self.remove_stopwords = remove_stopwords
        if self.remove_stopwords:
            self._download_stopwords(language=language)
            self.russian_stopwords = stopwords.words(language)
        else:
            self.russian_stopwords = None
        self.delete_unigrams = delete_unigrams
        self.long_vowels_handle = long_vowels_handle
        
    
    def tokenizer(self, text):
        # do_something, add later
        tokens = self._preprocess(text)
        return tokens
    
    def _preprocess(self, text):
        text = text.lower()
        text = self._transliterate(text)
        
        if self.long_vowels_handle:
            text = self._delete_long_vowels(text)
        
        "remove all symbols except for russian letters"
        letter_tokens = self._get_letters_only(text)

        
        # stop earlier
        if self._early_stopping(letter_tokens):
            return []
               
            
        if self.remove_stopwords:
            letter_tokens = self._delete_stopwords(letter_tokens)
        
        
        if self.delete_unigrams:
            letter_tokens = self._delete_unigrams(letter_tokens)
            
        if self.stemming_use:
            letter_tokens = [self.stemmer.stem(token) for token in letter_tokens]
        
        return letter_tokens
    
    def _download_stopwords(self, language):
        try:
            stopwords.words(language)
        except LookupError:
            nltk.download('stopwords')
    
    def _transliterate(self, text):
        transliterate_dict = load_transliteration_dict()
        for (key, value) in transliterate_dict.items():
            text = text.replace(key, value)
        return text
    
    def _get_letters_only(self, text):
        # remove all the non-russian langauge
        # from all the words
        letter_tokens = [re.sub(r'[^а-яё]', '', word) for word in text.split()]
        return letter_tokens
    
    
    def _early_stopping(self, letter_tokens):
        if not letter_tokens:
            return True
        # handle empty string because of the smiles
        if len(letter_tokens) == 1 and len(letter_tokens[0]) == 0:
            return True
        
        
            
    def _delete_long_vowels(self, text):
        "handling 3 and more same letters in a row"
        pattern = re.compile(r"(.)\1{2,}")
        new_text = pattern.sub(r"\1", text)
        return new_text
    
    
    def _delete_stopwords(self, tokens):
        new_letter_tokens = [
            token for token in tokens
            if token not in self.russian_stopwords
        ]
        return new_letter_tokens
    
    
    def _delete_unigrams(self, tokens):
        new_letter_tokens = [
            token for token in tokens
            if len(token) > 1
        ]
        return new_letter_tokens
    
 


    