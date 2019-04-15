
# coding: utf-8

# In[2]:


import praw
import time
import json
import numpy as np
import matplotlib.pyplot as plt


# In[3]:


def submissionData(num, submission, now):
    id_ = submission.id
    tmp = (now - submission.created_utc)/(60*60)
    utc_ = int(tmp * 1000)/1000
    upv_ = submission.score
    return {"rank": num, "id": id_, "time": utc_, "upvote": upv_}

def authorize():
    user_data = {"username": "Aad1tya23",
            "password": "p@ssw0rd",
            "client_id": "cqtbqCS6tCeJ9g",
            "client_secret": "JQwcpZR8346OcezEg2XRQCYxksw",
            "user_agent": "Reddit python extractor by /u/Aad1tya23"}
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
    for _ in reddit.subreddit('all').hot(limit=2500):
        num = num+1
        if num%100 == 0: print(int(num/100), end=" ")
        data_hot.append(submissionData(num, _, now))
    print("\n")
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

    #output to json
    json_Data = json.dumps(json_dump)
    filename = str(int(now)) + '.json'

    #save data on file
    with open("collection_json/"+filename, 'w') as outfile:
        json.dump(json_Data, outfile)

    #save filename in json data.json
    json_data = json.loads(open('data.json').read())
    json1_data = json.loads(json_data.replace("\\", ""))
    now_value = json1_data["filename"]

    now_value.append(filename)
    json_Data = json.dumps({"filename": now_value})
    with open('data.json', 'w') as outfile:
        json.dump(json_Data, outfile)

    return now_value



#import from json
# json_data = json.loads(open('1555351939.json').read())
# json1_data = json.loads(json_data.replace("\\", ""))


# In[6]:


def main(display=False):
    if display==True:
        json_data = json.loads(open('data.json').read())
        json1_data = json.loads(json_data.replace("\\", ""))
        return json1_data["filename"]
    
    reddit = authorize()
    print(reddit.user.me())

    now = time.time()
    data_hot = get_hot(reddit, now)
    data_top = get_top(reddit, now)
    files = output_json(now, data_hot, data_top)
    return files


# In[ ]:


last = time.time()
interval = 60 #min

while True:
    gap = time.time() - last 
    print(gap)
    
    if (gap > interval*60):
        file = main(display=False)
        last = time.time()
    else:
        time.sleep(901)

