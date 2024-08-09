
"""
Justin Carter
8/9/2024
Reddit Presidental and Vice Presidential Word Cloud

This script uses the Reddit API in order to obtain text data from political subreddits,
as well as a collection of all subreddits, for the purpose of ascertaining the 
words most closely assicuated with the Presidential and Vice Presidential Candidates 
for the 2024 election cycle

"""
#==================Import necessary packages, setup, make initial corpi

import praw
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from collections import Counter
import re
from my_credentials import app_client_id, app_client_secret, user_agent #local file

nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')

# Initialize a Reddit instance
reddit = praw.Reddit(client_id=app_client_id ,
                     client_secret=app_client_secret,
                     user_agent=user_agent)

# Make function for collecting corpi of subreddit post titles

def get_search_corpus(my_search_term, my_subreddit):
    
    search_term = my_search_term
    subreddit = reddit.subreddit(my_subreddit)
    posts = subreddit.search(search_term, limit=500)
    post_lst = [post.title for post in posts]
    corpus = ' '.join(post for post in post_lst)
    
    return corpus

#Conservative Corpi
con_kamala_corpus = get_search_corpus('Kamala', 'Conservative')
con_walz_corpus = get_search_corpus('Walz', 'Conservative')
con_trump_corpus = get_search_corpus('Trump', 'Conservative')
con_vance_corpus = get_search_corpus('Vance', 'Conservative')


#Liberal Corpi
lib_kamala_corpus = get_search_corpus('Kamala', 'Liberal')
lib_walz_corpus = get_search_corpus('Walz', 'Liberal')
lib_trump_corpus = get_search_corpus('Trump', 'Liberal')
lib_vance_corpus = get_search_corpus('Vance', 'Liberal')

#=====================use ml to find nouns most associated with terms

def make_noun_dataframe(corpus):
    
    #make function to remove non-nouns
    def remove_non_nouns(word_list):
        tagged_words = nltk.pos_tag(word_list)
        nouns = [word for word, pos in tagged_words if pos.startswith('N')]
        return nouns
    
    words = []
    word = ''
    for thing in corpus:
        if thing == ' ':
            words.append(word)
            word = ''
            continue
        else:
            word += thing

    my_nouns = remove_non_nouns(words)
    my_nouns = [word.title() for word in my_nouns]
    word_counts = Counter(my_nouns)
    
    #sort word counts in descending order, then take the top 30 words
    sorted_word_counts = {word: count for word, count in sorted(word_counts.items(), key=lambda item: item[1], reverse=True)}
    in_words = list(sorted_word_counts.keys())[:30]
    
    filtered_words = [word for word in my_nouns if word in in_words] #check words against in_list
    filtered_words_cleaned = [re.sub(r'[^\w\s]', '', word) for word in filtered_words]
    filtered_words_cleaned = [word for word in filtered_words_cleaned if word != ' ']

    #put list into df, make each element a row, reset index
    nouns_df = pd.DataFrame([{'Nouns':filtered_words_cleaned}]).explode('Nouns').reset_index(drop=True)
    return nouns_df

#================Make finalized datasets of nouns most associated w/ candidates for each subreddit
lib_kamala_nouns_df = make_noun_dataframe(lib_kamala_corpus)
lib_walz_nouns_df = make_noun_dataframe(lib_walz_corpus)
lib_trump_nouns_df = make_noun_dataframe(lib_trump_corpus)
lib_vance_nouns_df = make_noun_dataframe(lib_vance_corpus)

#==conservatives
con_kamala_nouns_df = make_noun_dataframe(con_kamala_corpus)
con_walz_nouns_df = make_noun_dataframe(con_walz_corpus)
con_trump_nouns_df = make_noun_dataframe(con_trump_corpus)
con_vance_nouns_df = make_noun_dataframe(con_vance_corpus)


#write to file; uncomment the following to save datasets:
"""
lib_kamala_nouns_df.to_csv('lib_kamala_nouns_df.csv', header=True, index=False)
lib_walz_nouns_df.to_csv('lib_walz_nouns_df.csv', header=True, index=False)
lib_trump_nouns_df.to_csv('lib_trump_nouns_df.csv', header=True, index=False)
lib_vance_nouns_df.to_csv('lib_vance_nouns_df.csv', header=True, index=False)

con_kamala_nouns_df.to_csv('con_kamala_nouns_df.csv', header=True, index=False)
con_walz_nouns_df.to_csv('con_walz_nouns_df.csv', header=True, index=False)
con_trump_nouns_df.to_csv('con_trump_nouns_df.csv', header=True, index=False)
con_vance_nouns_df.to_csv('con_vance_nouns_df.csv', header=True, index=False)

"""

