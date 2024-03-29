import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
__________________________________________________________________________________

%matplotlib inline
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import scipy as stats
from ast import literal_eval
from sklearn.feature_extraction.text import TfidfVectorizer,CountVectorizer
from sklearn.metrics.pairwise import linear_kernel, cosine_similarity
from nltk.stem.snowball import SnowballStemmer
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import wordnet


pd.pandas.set_option('display.max_columns',None)
_________________________________________________________________________________

link_small = pd.read_csv('/content/links_small.csv')
link_small.head()
_________________________________________________________________________________

print(link_small['tmdbId'].isnull().sum())
print(link_small.info())
_________________________________________________________________________________

link_small = link_small[link_small['tmdbId'].notnull()]['tmdbId'].astype('int')
link_small.head()
_________________________________________________________________________________

md=pd.read_csv('/content/movies_metadata.csv',error_bad_lines=False, engine="python")
_________________________________________________________________________________

md.isnull().sum()
_________________________________________________________________________________

md['id']
_________________________________________________________________________________

md['id'] = md['id'].astype('int')
_________________________________________________________________________________

smd = md[md['id'].isin(link_small)]
smd.shape
_________________________________________________________________________________

smd['tagline'] = smd['tagline'].fillna('')
_________________________________________________________________________________

smd['description'] = smd['overview'] + smd['tagline']
_________________________________________________________________________________

smd['description'] = smd['description'].fillna('')
_________________________________________________________________________________

from sklearn.feature_extraction.text import TfidfVectorizer

tf = TfidfVectorizer(analyzer='word',ngram_range=(1,2),min_df=0,stop_words='english')
tfid_mat = tf.fit_transform(smd['description'])
_________________________________________________________________________________

cos_sim = linear_kernel(tfid_mat,tfid_mat)
_________________________________________________________________________________

len(cos_sim[0])
_________________________________________________________________________________

smd = smd.reset_index()
_________________________________________________________________________________

titles = smd['title']
_________________________________________________________________________________

indices = pd.Series(smd.index,index=smd['title'])
indices
_________________________________________________________________________________

idx = indices['Toy Story']
_________________________________________________________________________________

sim_scores = list(enumerate(cos_sim[idx]))
sim_scores[:5]
_________________________________________________________________________________

sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True) #sorting the movies based on the max similarity score
sim_scores = sim_scores[1:31]
movie_indices = [i[0] for i in sim_scores]#getting the similarity score of the movies based on movie 'the dark night raises'
print(titles.iloc[movie_indices])
_________________________________________________________________________________

def get_recommendations(title):
    idx = indices[title]
    sim_scores = list(enumerate(cos_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:31]
    movie_indices = [i[0] for i in sim_scores]
    return titles.iloc[movie_indices]
_________________________________________________________________________________

get_recommendations('The Godfather').head(10)
_________________________________________________________________________________