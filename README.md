# About

`check-swear` is a machine learning and regular expression-based library designed to detect and filter profanity in text-based communication. Initially aimed at monitoring and improving the language used in school and student chats, `check-swear` offers a versatile solution that can be integrated into various environments requiring profanity filtering.

## Features

- **Machine Learning Driven**: Utilizes SVM classification algorithm to understand context and nuances, ensuring high accuracy in detecting offensive language.
- **Regular Expression Support**: Incorporates a comprehensive set of regular expressions to catch commonly used profane words and phrases.
- **Customizable Filters**: Offers the flexibility to customize and extend the list of profane words based on the specific needs of different user groups or cultural sensitivities.
- **Easy Integration**: Designed with simplicity in mind, SwearCheck can be easily integrated into chat applications, forums, and any platform requiring content moderation.

## Getting Started

To get started with `check-swear`, simply install the package via pip:

```bash
pip install check-swear
```

### Note on Importing the Library
Despite the library being named check-swear, when you import it into your Python project, you will need to replace the hyphen (-) with an underscore (_) This is a common convention in Python packaging because Python modules and packages cannot have hyphens in their names. The hyphen is not a valid character for Python identifiers, so it's replaced with an underscore for the actual package name.

```python
import check_swear
```

## Usage

```python
from check_swear import SwearingCheck

sch = SwearingCheck() # create filter

rude_comment = "а не пошел бы ты нахуй, дружище"
friendly_comment = "svm - алгоритм машинного обучения"

sch.predict(rude_comment)
# [1]

sch.predict_proba(rude_comment)
# [0.9822432776183899]

sch.predict(friendly_comment)
# [0]

sch.predict_proba(friendly_comment)
# [0.027772391001567764]

```

### Model and Regular Expression Checks
The library utilizes a pre-trained SVM (Support Vector Machine) model for profanity detection, which is adept at classifying text but isn't flawless. To enhance accuracy, each comment undergoes a preliminary scan with two sets of regular expressions before the machine learning model processes it. These regex checks aim to catch clear profanity patterns. If you wish to bypass this regex pre-check for any reason, you can set the reg_pred=False parameter when using the filter.

```python
clear_ml_sch = SwearingCheck(reg_pred=False)

hard2detect = "а вот это охуеньчик))"

clear_ml_sch.predict_proba(hard2detect)
# [0.02542796]

sch.predict_proba(hard2detect)
# [0.5127139801037626]

```

_Understanding Probability Scores:_ Even benign comments sometimes contain character sequences that resemble profane words, which could lead the filter to assign a roughly 30% probability of the comment being offensive. It's a cautious indicator, hinting at potential profanity without outright condemnation. If the regular expression engine detects a match in our default list or any custom list you supply, the probability jumps to around 50%, reflecting a stronger suspicion. Keep in mind that despite the robust training on over 700,000 comments, the nuances of language and the ever-evolving lexicon of slang can sometimes elude even the most sophisticated models. We are committed to continuously expanding our dataset of profane words and phrases.

### Additional Features of check-swear

*   **Custom Stop Words List:** Enhance regular expression detection by adding your own list of stop words.
    
*   **Flexible Input Formats:** The model accepts both single strings and lists of strings for analysis.
    
*   **Bin Parameter:** Divide large texts into manageable `bins` parts for efficient processing.

*   **Transliteration Support**: The library understands transliteration, recognizing Russian words written with English letters, making it robust in handling a variety of text inputs.

```python
adv_sch = SwearingCheck(reg_pred=True, bins=3, stop_words=["питон"])

long_comment = "буду с тобой асболютно честен но твой проект на питоне это просто абсолютно полная hueta.."

adv_sch.predict_proba(long_comment)
# [0.02110824940143035, 0.5090685358094555, 0.9741733209291503]

adv_sch.output_text_
# ['буду с тобой асболютно честен', 'но твой проект на питоне', 'это просто абсолютно полная hueta..']

# array of strings
array_comment = ["всем привет", "ты s__УкА blYa"]

adv_sch.predict_proba(array_comment)
# [0.023436897211045367, 0.9999479672960417]

```

### Conclusion on Model Limitations:

Please be aware that while `check-swear` is a robust tool for identifying profane content, it is not without limitations. Creative individuals may always find novel ways to bypass filters with new slang or coded language. Despite this, `check-swear` effectively identifies the majority of profane comments (about 0.95 F1 score), helping maintain a respectful and professional discourse in various settings.

