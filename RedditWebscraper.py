#!/usr/bin/env python
# coding: utf-8

# In[1]:


"""
Sources -
    * https://towardsdatascience.com/scraping-reddit-data-1c0af3040768
    * https://medium.com/swlh/scraping-reddit-using-python-57e61e322486
    
About:
    * This is a simple Reddit webscraper to gather comments of various Reddit posts.
    * This was created for a SCU Imaginarium's Game Studies group.
"""


# In[2]:


import praw
import math
import pandas as pd


# In[3]:


def set_up_reddit_api():
    my_client_id = "CLIENT_ID"
    my_client_secret = "CLIENT_SECRET"
    my_user_agent = "NAME_OF_APP"

    reddit = praw.Reddit(client_id=my_client_id, client_secret=my_client_secret, user_agent=my_user_agent)
    return reddit


# In[4]:


def scrape_subreddits(reddit, list_of_subreddits, query, number_of_posts, comments_depth):
    for s in list_of_subreddits:
        subreddit = reddit.subreddit(s)   # Choosing the subreddit

        for item in query:
            post_dict = {
                "title" : [],      # title of the post
                "score" : [],      # score of the post
                "id" : [],         # unique id of the post
                "url" : [],        # url of the post
                "comms_num": [],   # the number of comments on the post
                "created" : [],    # timestamp of the post
                "body" : []        # the description of post
            }
            comments_dict = {
                "comment_id" : [],          # unique comm id
                "comment_parent_id" : [],   # comment parent id
                "comment_body" : [],        # text in comment
                "comment_link_id" : []      # link to the comment
            }

            for submission in subreddit.search(query, sort="top", limit=number_of_posts):
                post_dict["title"].append(submission.title)
                post_dict["score"].append(submission.score)
                post_dict["id"].append(submission.id)
                post_dict["url"].append(submission.url)
                post_dict["comms_num"].append(submission.num_comments)
                post_dict["created"].append(submission.created)
                post_dict["body"].append(submission.selftext)

                # Acessing comments on the post
                submission.comments.replace_more(limit=comments_depth)
                for comment in submission.comments.list():
                    comments_dict["comment_id"].append(comment.id)
                    comments_dict["comment_parent_id"].append(comment.parent_id)
                    comments_dict["comment_body"].append(comment.body)
                    comments_dict["comment_link_id"].append(comment.link_id)

            post_comments = pd.DataFrame(comments_dict)

            post_comments.to_csv(s+"_comments_"+ item +"_subreddit.csv")
            post_data = pd.DataFrame(post_dict)
            post_data.to_csv(s+"_"+ item +"_subreddit.csv")


# In[5]:


def main():
    api = set_up_reddit_api()
    
    subreddits = ["FireEmblemHeroes", "PokemonMasters"]
    query = ["build"] # "Theorycraft" in these subreddits = Making up a non-existent unit in the game
    number_of_posts = 5 # use an actual #, for testing purposes, or else this will run for a LONG time
    comments_depth = None
    
    scrape_subreddits(api, subreddits, query, number_of_posts, comments_depth)
    return


# In[6]:


main()


# In[7]:


# The following commented-out code is a Test for scraping the top 10 Hot posts + comments of just 1 subreddit

# subreddit_name = "FireEmblemHeroes"

# # get 10 hot posts from the FireEmblemHeroes subreddit
# hot_posts = reddit.subreddit(subreddit_name).hot(limit=10)
# for post in hot_posts:
#     print(post.title)
    


# In[8]:


# posts = []
# ml_subreddit = reddit.subreddit(subreddit_name)
# for post in ml_subreddit.hot(limit=10):
#     posts.append([post.title, post.score, post.id, post.subreddit, post.url, post.num_comments, post.selftext, post.created])
# posts = pd.DataFrame(posts,columns=['title', 'score', 'id', 'subreddit', 'url', 'num_comments', 'body', 'created'])
# print(posts)


# In[9]:


# file_name = "FEHdata.csv"
# posts.to_csv(file_name, sep='\t', encoding='utf-8', index=False)

# df = pd.read_csv(file_name, sep='\t')
# print(df)


# In[10]:


# submission = reddit.submission(id="10rek6c")

# submission.comments.replace_more(limit=0)
# #for top_level_comment in submission.comments:
# #    print(top_level_comment.body)

# for comment in submission.comments.list():
#     print(comment.body)
    

