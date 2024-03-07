import warnings
from .utils import Validate
from .utils import Preprocess
from .utils import RegularExpr
from .utils import vectorizer_load
from .utils import model_load
from ..model_prep.tokenizer import ChatTokenization

class SwearingCheck:
    
    """
    A tool for checking and moderating swearing in Russian comments. It uses
    a combination of regular expression pattern matching and machine learning
    models to predict the presence of profanity and to classify text accordingly.

    The class supports preprocessing of input text, tokenization, and the
    application of a pre-trained model for profanity detection. It allows
    for the customization of stop words and employs both "strong" and "weak"
    pattern matching to enhance detection accuracy.

    Parameters
    ----------
    reg_pred : bool, default=True
        If set to True, enables the regular expression-based prediction
        enhancement. When enabled, stop words are utilized in pattern matching
        to adjust the prediction probabilities.
        
    bins : int or None, optional
        Specifies the number of bins (segments) into which the input text
        should be divided for analysis. This parameter is intended to be used
        when processing longer texts. If None, the text will not be segmented.

    stop_words : list of str or None, optional
        A list of words considered as stop words, which are used in the
        regular expression-based prediction enhancement. If None, no additional
        stop words are added to the default list.

    Attributes
    ----------
    predict_probs : list of float
        The probabilities of each text segment being classified as containing
        profanity, as determined by the pre-trained model and optionally
        adjusted by regular expression analysis.

    output_text_ : list of str
        The preprocessed and tokenized version of the input text.

    stop_words_ : str
        The concatenated string of stop words used for pattern matching.

    _strong_pattern, _weak_pattern : compiled regex
        Compiled regular expression patterns derived from the stop words for
        "strong" and "weak" matches. These patterns are used to analyze the
        input text if `reg_pred` is True.

    Methods
    -------
    predict(input_text, threshold=0.5):
        Predict whether the input text contains profanity based on a specified
        threshold. 

    predict_proba(input_text):
        Predict the probability that the input text contains profanity.

    Examples
    --------
    >>> swear_filter = SwearingCheck(reg_pred=True, bins=3, stop_words=["питон"])
    >>> swear_filter.predict_proba("только посмотри на этот охуенный проект сделанный полностью на питоне!")
    [0.01783845789104434, 0.9723342111371316, 0.5077507666782685]
    >>> checker.output_text_
    ['только посмотри на', 'этот охуенный проект', 'сделанный полностью на питоне!']

    Notes
    -----
    The class utilizes a pre-trained machine learning model and custom regular
    expression patterns for its predictions. Accuracy can vary based on the
    input text's content and context.
    
    When utilizing the stop_words parameter, it is recommended to retain the default
    threshold value of 0.5. This recommendation is based on the consideration that 
    stop words specified by the user might not inherently be profane. As a result, the model's 
    confidence in predicting profanity for texts containing these user-defined stop words
    may hover around the 0.5 mark.
    
    To examine the processed version of your input text, refer to the output_text_ attribute
    Note, however, that output_text_ reflects preprocessing results and will remain unchanged for array
    inputs pre-segmented into bins. For detailed preprocessing  insights, including text segmentation
    into bins, input your text as a single string. 
    
    """
    
    _parameter_constraints : dict = {
        "reg_pred": [bool],
        "bins": [int,  None],
        "stop_words": [list, None]
    }
    
    def __init__(self, reg_pred=True, bins=None, stop_words=None):
        self._validate_params(reg_pred=reg_pred, bins=bins, stop_words=stop_words)
        self.reg_pred = reg_pred
        self.bins = bins
        self.stop_words = stop_words
            
        pass
    
    def _validate_params(self, **kwargs):
                
        if not isinstance(kwargs['reg_pred'], bool):
            raise ValueError(
                f"reg_pred must be boolean, got {type(kwargs['reg_pred'])}"
            )
            
        if not isinstance(kwargs['bins'], int) and not kwargs['bins'] is None:
            raise ValueError(
                f"bins must be integer values or None, got {type(kwargs['bins'])}"
            )
            
        if not isinstance(kwargs['stop_words'], list) and not kwargs['stop_words'] is None:
            raise ValueError(
                f"stop words must be a Python list, got {type(kwargs['stop_words'])}"
            )
                
        if not kwargs['reg_pred'] and not kwargs['stop_words'] is None:
            warnings.warn(
                "Attention: add stop words only if reg_pred is set to True."
            )
            
        if not Validate.array_validation(kwargs['stop_words']):
            raise TypeError(
                "All elements of stop words must be strings."
            )
        pass
    
    
    def predict(self, input_text, threshold=0.5):
        self.predict_probs = self._get_predict(input_text)
        preds = list(map(lambda p: 0 if p < threshold else 1, self.predict_probs))
        return preds
    
    def predict_proba(self, input_text):
        self.predict_probs = self._get_predict(input_text)
        return self.predict_probs
    
    def _get_predict(self, input_text):
        prep_text = self._text_validation(input_text)
        
        # see how the text changes
        self.output_text_ = prep_text
        
        # add new words to stop words, make it an external attribute
        # and create strong and weak patterns
        if not hasattr(self, 'stop_words_'):
            self.stop_words_ = RegularExpr.concatenate(self.stop_words)
            (self._strong_pattern, self._weak_pattern) = RegularExpr.get_patterns(self.stop_words_)
        
            
        tok = ChatTokenization()
        tokenized_text = [' '.join(tok.tokenizer(string)) for string in prep_text]
        

        vectorizer = vectorizer_load()
        vec_text = vectorizer.transform(tokenized_text)
        
        model = model_load()
        probabilities = model.predict_proba(vec_text)[:, 1]
        
        
        if self.reg_pred:
            bool_mask = RegularExpr.analyze(prep_text, self._strong_pattern, self._weak_pattern)  
            return [(probabilities[i] + bool_mask[i] * 0.5) / (1.0 + bool_mask[i] * 0.5) for i in range(len(probabilities))]
        else:
            return probabilities

    
    def _text_validation(self, input_text):
        if isinstance(input_text, str):
            # string preprocess
            self.bins = Validate.string_validation(input_text, self.bins)
            preprocessed_text = Preprocess.string_prep(input_text, self.bins)
            return preprocessed_text

        elif hasattr(input_text, '__iter__'):
            # array preprocess
            if not Validate.array_validation(input_text):
                raise TypeError("All elements must be strings.")
            
            if not self.bins is None:
                warnings.warn(
                    "If a string array is passed, bins parameter will be ignored."
                )
                
            preprocessed_text = Preprocess.array_prep(input_text)
            return preprocessed_text
        else:
            raise TypeError(
                "Input text must be a string or an array-like object"
            )
            
