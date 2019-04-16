# coding: utf-8

# In[2]:

import os
import praw
import time
import json
from dropboxUP import upload
number = 2500

user_data = {"username": os.environ["username"],
             "password": os.environ["password"],
             "client_id": os.environ["client_id"],
             "client_secret": os.environ["client_secret"],
             "user_agent": "Reddit python extractor by /u/Aad1tya23"}  
TOKEN = os.environ["dropbox_token"]
# In[3]:


def submissionData(num, submission, now):
    id_ = submission.id
    tmp = (now - submission.created_utc)/(60*60)
    utc_ = int(tmp * 1000)/1000
    upv_ = submission.score
    return {"rank": num, "id": id_, "time": utc_, "upvote": upv_}

def authorize():
      
    
    reddit = praw.Reddit(username = user_data["username"],
                         password = user_data["password"],
                        client_id = user_data["client_id"],
                        client_secret = user_data["client_secret"],
                        user_agent = user_data["user_agent"])
    return reddit


# In[4]:


def get_hot(reddit, now):
    num = 0
    data_hot = []

    #Make list of data
    for _ in reddit.subreddit('all').hot(limit=number):
        num = num+1
        if num%100 == 0: print(int(num/100), end=" ")
        data_hot.append(submissionData(num, _, now))
    return data_hot

def get_top(reddit, now):
    num = 0
    data_top = []

    #Make list of data
    for _ in reddit.subreddit('all').top("hour"):
        num = num+1
        if num%100 == 0: print(int(num/100), end=" ")
        data_top.append(submissionData(num, _, now))
    return data_top


# In[5]:


def output_json(now, data_hot, data_top):
    #Create empty data.json, start again
    # json_Data = json.dumps({"filename": []})
    # with open('data.json', 'w') as outfile:
    #     json.dump(json_Data, outfile)

    #Save data in json form
    json_dump = {
        "time": now,
        "data_hot": data_hot,
        "data_top": data_top,
        "keys": "Id, Hours uploaded, Upvotes"
    }
    
    
    dropbox_files = upload(TOKEN, str(int(now)), json_dump)
    return dropbox_files

    
def main():    
    reddit = authorize()
    print("Authorized: ", reddit.user.me())

    now = time.time()
    print("Hot: ", end="")
    data_hot = get_hot(reddit, now)
    print("Top: ", end="")
    data_top = get_top(reddit, now)
    print("\nNow uploading to Dropbox...\nFiles: ", end="")
    files = output_json(now, data_hot, data_top)
    print(files)




last_did = time.time()
print("Started at: ", last_did)

# while True:
#     present = time.time()
#     if present - last_did > 6*60:
#         print()
#         main()
#         last_did = present
#     else:
#         print(".", end=" ")
#         time.sleep(60* 2)


while True:
    main()
    time.sleep(3590)
