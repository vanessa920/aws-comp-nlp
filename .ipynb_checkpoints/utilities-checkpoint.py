import regex as re
import spacy
import nltk
import string

from nltk.stem.porter import PorterStemmer

# Load English tokenizer, tagger, parser, NER and word vectors
parser = spacy.load('en_core_web_sm')
# Create the list of default punctuation marks
exclusion = string.punctuation + str(spacy.lang.en.stop_words.STOP_WORDS)

def clean_text(text):
    #text = text.decode("UTF-8")
    text = text.replace('\n'," ")
    text = text.replace('\x0c'," ")
    text = re.sub(r"-", " ", text) # Split the words with "-" (for example：pre-processing ==> pre processing）
    text = re.sub(r"\d+/\d+/\d+", "", text) # Take out the dates
    text = re.sub(r"[0-2]?[0-9]:[0-6][0-9]", "", text) # Take out the time
    text = re.sub(r"[\w]+@[\.\w]+", "", text) # Take out the emails
    text = re.sub(r"/[a-zA-Z]*[:\//\]*[A-Za-z0-9\-_]+\.+[A-Za-z0-9\.\/%&=\?\-_]+/i", "", text) # Take out the websites
    text = re.sub(r'\.',' ',text)
    pure_text = ''
    # Validate to check if there are any non-text content 
    for letter in text:
        # Keep only letters and spaces
        if letter.isalpha() or letter==' ':
            pure_text += letter
    # Join the words are not stand-alone letters
    text = ' '.join(word for word in pure_text.split() if len(word)>1)
    return text

# Creating our tokenizer function
def spacy_tokenizer(sentence,exclusion=exclusion):
    # Creating our token object, which is used to create documents with linguistic annotations.
    mytokens = parser(sentence)
    # Lemmatizing each token and converting each token into lowercase
    mytokens = [ word.lemma_.lower().strip() if word.lemma_ != "-PRON-" else word.lower_ for word in mytokens ]
    # Removing stop words
    mytokens = [ word for word in mytokens if word not in exclusion ]
    # return preprocessed list of tokens
    return ' '.join(mytokens)

# take text and return stemmed a list of text
def nltk_stemmer(text):
    porter_stemmer = PorterStemmer()
    word_data = ' '.join(text)
    # First Word tokenization
    nltk_tokens = nltk.word_tokenize(word_data)
    #Next find the roots of the word
    t = [porter_stemmer.stem(w) for w in nltk_tokens]
    return t

def test():
    pass

if __name__ == '__main__':
    test()