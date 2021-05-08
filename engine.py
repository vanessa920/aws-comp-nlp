import pandas as pd
import sys
import re
import spacy
import string
import pickle
import datetime
import gensim

from gensim import corpora, models, similarities
from client import userInput
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer, ENGLISH_STOP_WORDS
from sklearn.decomposition import LatentDirichletAllocation

class engine:
    '''
    A NLP process engine.
    initialization:
        + n, for LDA component number,
        + parser, for preset spacy object,
        + purge, for a dictionary of regex pattern to identify in string and purge,
        + exclusion, for a string contains all excluding punctuations and stop words,
    attributes:
    
    methods:
    
    '''

    SPACY_PARSER = spacy.load('en_core_web_sm')
    
    LDA_COMPONENT_DEFAULT = 10
    TEXT_PURGE_LS = {'return sym'   :re.compile(r'\n'),
                    'unknown char'  :re.compile(r'\x0c'),
                    'miscellaneous' :re.compile(r'[-.]'),
                    'dates'         :re.compile(r"\d+/\d+/\d+"),
                    'time'          :re.compile(r"[0-2]?[0-9]:[0-6][0-9]"),
                    'emails'        :re.compile(r"[\w]+@[\.\w]+"),
                    'websites'      :re.compile(r"/[a-zA-Z]*[:\//\]*[A-Za-z0-9\-_]+\.+[A-Za-z0-9\.\/%&=\?\-_]+/i")}
    TEXT_EXCLUSION = string.punctuation + str(spacy.lang.en.stop_words.STOP_WORDS)
    
    def __init__(self,
                n       = LDA_COMPONENT_DEFAULT,
                parser  = SPACY_PARSER,
                purge   = TEXT_PURGE_LS,
                exclusion = TEXT_EXCLUSION):
        self.component_n= n
        self.parser     = parser
        self.purgeLS    = purge
        self.exclusion  = exclusion
        self.TFIDF_core = TfidfVectorizer(min_df=0.0085, max_df=0.9, stop_words=ENGLISH_STOP_WORDS)
        self.LDA_core   = LatentDirichletAllocation(n_components=n, random_state=0)
        self.status     = 'OFF'
    
    def loadCSV(self,fileDIR):
        '''
        load csv file into a dataframe,
        clean all excessive contents,
        
        '''
        statusUpdate('--loading CSV--')
        df = pd.read_csv(fileDIR, index_col = 0)
        
        statusUpdate('--converting dataframe--')
        df['date'] = pd.to_datetime(df['date'])
        art_df = pd.DataFrame(df.groupby('artID').sum('content')['subID'])
        art_df = art_df.loc[art_df.subID>3]
        
        df = df.merge(art_df, on='artID', how = 'inner')
        
        statusUpdate('--created object dataframe df_subID--')
        self.df_subID = df[df['subID_x']!=0].reset_index()
        
        statusUpdate('--clean and spacy transforming dataframe content I--')
        text = self.df_subID['content']
        text = text.apply(lambda x: self.clean_text(x))
        text = text.apply(lambda x: self.spacy_tokenizer(x))
        
        statusUpdate('--clean and spacy transforming dataframe content II--')
        clean_list = [self.clean_text(i) for i in text]
        self.spacy_list = [self.spacy_tokenizer_2(i) for i in clean_list]
        
        statusUpdate('--get word matrix and vocabulary--')
        self.word_matrix = self.TFIDF_core.fit_transform(text)
        self.vocab = self.TFIDF_core.get_feature_names()
        
        statusUpdate('--initializing LDA core--')
        self.content_df, self.word2topic_df = self.LDA_init()
        
        statusUpdate('--initializing word to vector core--')
        self.w2v = gensim.models.Word2Vec(self.spacy_list, size=100, window=5, min_count=1, workers=2, sg=1)
        
        self.status = 'ON'
        
    def clean_text(self,text):
        '''
        '''
        for k,p in self.purgeLS.items():
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
    def spacy_tokenizer(self,text):
        # Creating our token object, which is used to create documents with linguistic annotations.
        mytokens = self.parser(text)
        # Lemmatizing each token and converting each token into lowercase
        mytokens = [ word.lemma_.lower().strip() if word.lemma_ != "-PRON-" else word.lower_ for word in mytokens ]
        # Removing stop words
        mytokens = [ word for word in mytokens if word not in self.exclusion ]
        # return preprocessed list of tokens
        return ' '.join(mytokens)

    def spacy_tokenizer_2(self,text):
        # Creating our token object, which is used to create documents with linguistic annotations.
        mytokens = self.parser(text)
        # Lemmatizing each token and converting each token into lowercase
        mytokens = [ word.lemma_.lower().strip() if word.lemma_ != "-PRON-" else word.lower_ for word in mytokens ]
        # Removing stop words
        mytokens = [ word for word in mytokens if word not in self.exclusion ]
        # return preprocessed list of tokens
        return mytokens

    def LDA_init(self):
        try:
            self.LDA_core.fit(self.word_matrix)
        except Exception as err:
            print(err)
            return
        
        topic_matrix = self.LDA_core.transform(self.word_matrix)
        topic_matrix_df = pd.DataFrame(topic_matrix).add_prefix('topic_')
        topic_matrix_df["topic"] = topic_matrix_df.iloc[:,:].idxmax(axis=1)
        content_df = pd.concat([self.df_subID,topic_matrix_df], axis=1)
        
        word2topic_df = pd.DataFrame(self.LDA_core.components_, columns=self.vocab).T.add_prefix('topic_')
        return content_df, word2topic_df

    def getSimilar(self,keywords,topn = 20):
        if self.status != 'ON':
            print('need to load source file to initialize.')
            return
        try:
            result = [w[0] for w in self.w2v.wv.most_similar(keywords,topn = topn)]
        except Exception as err:
            print(err)
            print("Try Another Word")
        
        for i in range(topn):
            try:
                result.append(self.w2v.wv.most_similar(keywords,topn = topn)[i][0])
            except Exception as err:
                print(err)
                print("Try Another Word")
        return result
    '''
    def saveEngine(self,filename):
        statusUpdate('--saving engine--')
        with open(filename,'wb') as outputfile:
            pickle.dump(self,outputfile,pickle.HIGHEST_PROTOCOL)
        return True
        
    def loadEngine(self,filename):
        statusUpdate('--load engine--')
        try:
            with open(filename,'rb') as inputfile:
                self = pickle.load(inputfile)
            return True
        except Exception as err:
            print(err)
            statusUpdate('--fail to load engine--')
            return False
    '''
    
    def wordWeight(self,):
        print('hello')
    
    
def statusUpdate(status,end = '\r'):
    sys.stdout.write("\033[K")
    print(status,end=end)
    

def test():
    # User Inputs
    # keywords,date,user_logics = userInput()

    # print(keywords,date,user_logics)
    keywords = ['covid','action']
    
    engineName1 = 'nlp_engine_1.pkl'
    engineName3 = 'nlp_engine_3.pkl'
    '''
    Engine_1 = engine()
    Engine_1.loadCSV('city_SanJose_Minutes.csv')
    similar = Engine_1.getSimilar(keywords)
    #print(similar)
    
    Engine_1.saveEngine(engineName1)
    
    Engine_2 = engine(n=15)
    Engine_2.loadEngine(engineName1)
    print(Engine_2.component_n)
    #print(Engine_2.word2topic_df)
    
    Engine_3 = engine()
    Engine_3.loadCSV('city_SanJose_Minutes.csv')
    similar = Engine_1.getSimilar(keywords)
    print(similar)
    
    with open(engineName3,'wb') as outfile:
        pickle.dump(Engine_3,outfile,pickle.HIGHEST_PROTOCOL)
    '''
    with open(engineName3,'rb') as infile:
        Engine_4 = pickle.load(infile)
        
    print(Engine_4.word2topic_df)
    
if __name__ == '__main__':
    # User Inputs
    test()
