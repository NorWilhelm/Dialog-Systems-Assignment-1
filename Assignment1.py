
import requests
import json # TODO: Remove? -For making the JSON beautiful - May not be needed
import time
import pandas as pd 

CLIENT_ID = '-JCzTg4Ls5r0lRxKK9XTzw'
SECRET_TOKEN = 'qCi-jTwE51swqEr8re08z1fh4rzc0A'

client_auth = requests.auth.HTTPBasicAuth(CLIENT_ID, SECRET_TOKEN)

post_data = {'grant_type': 'password',
        'username': 'NorWilhelm',
        'password': 'VaskebjornNELLIK!'}

# Header info which gives reddit a brief description of the app
headers = {'User-Agent': 'assignment1/0.0.1'}

# send request for an OAuth token
response = requests.post('https://www.reddit.com/api/v1/access_token',
                    auth=client_auth, data=post_data, headers=headers)

# convert response to JSON and pull access_token value
TOKEN = response.json()['access_token']

# add authorization to headers dictionary
headers = {**headers, **{'Authorization': f"bearer {TOKEN}"}}

# while the token is valid (~2 hours) we just add headers=headers to our requests
# Getting the "Hot" posts of /r/AskReddit
response = requests.get("https://oauth.reddit.com/r/AskReddit/hot",
                   headers=headers, params={'limit': '200'}) # TODO: Remove limit

# Easy to read JSON format
#print(json.dumps(response.json(), indent=4, sort_keys=True))

posts = pd.DataFrame()
comments = pd.DataFrame()

for post in response.json()['data']['children']:
        posts = posts.append({
                'title': post['data']['title'],
                'id': post['data']['id'],
                'created_utc': post['data']['created_utc'],
                'selftext': post['data']['selftext'],
                'author_fullname': post['data']['author_fullname'],
                'score': post['data']['score']
                # 'full name': post['kind'] + '_' + post['data']['id']
        }, ignore_index=True)

        time.sleep(1) # To not exceed reddit's limit of 60 calls per minute.
        
        # Not Ideal because this leads to very many requests which will take a long time
        # I did not find another way of doing this.
        response_comments = requests.get("https://oauth.reddit.com/r/AskReddit/comments/" + post['data']['id'],
                headers=headers, params={'limit': '2'}) # TODO: Remove limit

        for comment in response_comments.json():
                comments = comments.append({
                        #'author fullname': comment['author_fullname'],
                        #'id': comment['data']['id'],
                        #'created_utc': comment['data']['created_utc'],
                        #'parent_id': comment['data']['parent_id'],
                        'body': comment['data']['body']
                }, ignore_index=True)
                print(comment)


posts.to_csv('reddit_posts.csv')
comments.to_csv('reddit_comments.csv')


# Prints data to terminal in a pretty way
#with pd.option_context('display.max_rows', None, 'display.max_columns', None):
#        print(posts)