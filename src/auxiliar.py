import re
import string
from nltk.corpus import stopwords

stop_words = set(stopwords.words('english'))


def remove_header(input_str):
    i = input_str.find('\n\n')
    if i == -1:
        return input_str
    else:
        return input_str[i + 2:]


def remove_mails(input_str):
    return " ".join([word for word in input_str.split() if word.find("@") == -1])


def remove_single(input_str):
    return " ".join([word.lower() for word in input_str.split() if len(word) != 1])


def remove_punctuation(input_str):
    return input_str.translate(str.maketrans('', '', string.punctuation))


def replace_for_spaces(input_str):
    return re.sub('\s+', ' ', input_str)


def remove_stopwords(input_str):
    return " ".join([word for word in input_str.split() if word not in stop_words])


def preprocess_text(input_text):
    no_header = remove_header(input_text)
    no_mails = remove_mails(no_header)
    no_punct = remove_punctuation(no_mails)
    no_single = remove_single(no_punct)
    no_stop = remove_stopwords(no_single)
    return no_stop
