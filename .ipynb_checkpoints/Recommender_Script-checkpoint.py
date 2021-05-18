import pandas as pd
import re
import spacy
import string
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer, ENGLISH_STOP_WORDS
from sklearn.decomposition import LatentDirichletAllocation
import datetime
import gensim
from gensim import corpora, models, similarities
from client import userInput



# List of content patterns which post no value for current NLP modules.
purgeLS    = {'return sym':re.compile(r'\n'),
              'unknown char':re.compile(r'\x0c'),
              'miscellaneous':re.compile(r'[-.]'),
              'dates':re.compile(r"\d+/\d+/\d+"),
              'time':re.compile(r"[0-2]?[0-9]:[0-6][0-9]"),
              'emails':re.compile(r"[\w]+@[\.\w]+"),
              'websites':re.compile(r"/[a-zA-Z]*[:\//\]*[A-Za-z0-9\-_]+\.+[A-Za-z0-9\.\/%&=\?\-_]+/i")}

# Load English tokenizer, tagger, parser, NER and word vectors.
parser = spacy.load('en_core_web_sm')

# List of stopwords which post no value for current NLP module.
stop_words = spacy.lang.en.stop_words.STOP_WORDS

# list of punctuation marks which posts no value for current NLP module.
punctuations = string.punctuation

# quick clean method to remove all alphabic charaters and additional patterns.
def clean_text(text,purgeLS = purgeLS):
    # purge all nlp none processable characters.
    for k,p in purgeLS.items():
        text = re.sub(p,' ',text)
    
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
def spacy_tokenizer(sentence):
    # Creating our token object, which is used to create documents with linguistic annotations.
    mytokens = parser(sentence)
    # Lemmatizing each token and converting each token into lowercase
    mytokens = [ word.lemma_.lower().strip() if word.lemma_ != "-PRON-" else word.lower_ for word in mytokens ]
    # Removing stop words
    mytokens = [ word for word in mytokens if word not in stop_words and word not in punctuations ]
    # return preprocessed list of tokens
    return ' '.join(mytokens)

def spacy_tokenizer_2(sentence):
    # Creating our token object, which is used to create documents with linguistic annotations.
    mytokens = parser(sentence)
    # Lemmatizing each token and converting each token into lowercase
    mytokens = [ word.lemma_.lower().strip() if word.lemma_ != "-PRON-" else word.lower_ for word in mytokens ]
    # Removing stop words
    mytokens = [ word for word in mytokens if word not in stop_words and word not in punctuations ]
    # return preprocessed list of tokens
    return mytokens

def n_topic_df(n,word_matrix,df_subID):
    lda_tfidf = LatentDirichletAllocation(n_components=n, random_state=0)
    lda_tfidf.fit(word_matrix)
    topic_matrix = lda_tfidf.transform(word_matrix)
    topic_matrix_df = pd.DataFrame(topic_matrix).add_prefix('topic_')
    topic_matrix_df["topic"] = topic_matrix_df.iloc[:,:].idxmax(axis=1)
    all_df = pd.concat([df_subID,topic_matrix_df], axis=1)
    return all_df

def n_topic_word(n):
    lda_tfidf = LatentDirichletAllocation(n_components=n, random_state=0)
    lda_tfidf.fit(word_matrix)
    word_topic_matrix_df = pd.DataFrame(lda_tfidf.components_, columns=vocab).T.add_prefix('topic_')
    return word_topic_matrix_df


df = pd.read_csv("city_SanJose_Minutes.csv", index_col = 0)

df['date'] = pd.to_datetime(df['date'])

art_df = pd.DataFrame(df.groupby('artID').sum('content')['subID'])

art_df = art_df.loc[art_df.subID>3]

df = df.merge(art_df, on='artID', how = 'inner')

df_subID = df[df['subID_x']!=0]

df_subID = df_subID.reset_index()

text = df_subID['content']

text = text.apply(lambda x: clean_text(x))

text = text.apply(lambda x: spacy_tokenizer(x))

tfidf_vectorizer = TfidfVectorizer(min_df=0.0085, max_df=0.9, stop_words=ENGLISH_STOP_WORDS)

word_matrix = tfidf_vectorizer.fit_transform(text)

vocab = tfidf_vectorizer.get_feature_names()

all_df = n_topic_df(10,word_matrix,df_subID)

word_topic_matrix_df = n_topic_word(10)

clean_list = [clean_text(i) for i in text]

spacy_list =[spacy_tokenizer_2(i) for i in clean_list]

w2v = gensim.models.Word2Vec(spacy_list, size=100, window=5, min_count=1, workers=2, sg=1)



    
    
if __name__ == '__main__':
    # User Inputs
    keywords,date,user_logics = userInput()
    
    keywords = keywords.split()

    key_word=[]
    for i in range(20):
        try:
            key_word.append(w2v.wv.most_similar(keywords ,topn=20)[i][0])
        except:
            print("Try Another Word")

    topic_list =[]
    for i in key_word:
        try:
            topic_list.append(word_topic_matrix_df.loc[i].idxmax())
        except:
            pass

    sub_df = all_df[(all_df['date'] > datetime.datetime.strptime(oldTime, '%Y-%m-%d')) & (all_df['date'] < datetime.datetime.strptime(newTime, '%Y-%m-%d'))]


    notes = pd.DataFrame()

    for j in range(len(list(set(topic_list)))): # number of unique topics

        n = 0
        for i in range(len(topic_list)):

            if list(set(topic_list))[j] == topic_list[i]:
                n = n+3  # Number of notes can be controled to show 

        notes = pd.concat([notes, sub_df.sort_values(list(set(topic_list))[j], ascending = False)[0:n]])

    for i in notes.sort_values('date').content:
        print(i)