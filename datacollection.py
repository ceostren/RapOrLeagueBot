import praw
import json
import random
reddit = praw.Reddit(client_id='wdDqcPil1DISTw', client_secret="sByvEcauaXMiywjY03GLg9iBALM",
                     password='D3N73LCurry!', user_agent='python:com.raporgo2:v1 (by /u/raprogo2)',
                     username='Raporgo2')

# for comment in reddit.subreddit('rit').stream.comments():
# 	print(vars(comment))

hhhlst = []
nbalst = []
lst = []
fields = ('title','selftext','link_flair_text','subreddit_name_prefixed')

for post in reddit.subreddit('hiphopheads').top(limit=200):
    dict = vars(post)
    st = post.selftext
    url = post.url
    sub_dict = {}
    flair = post.link_flair_text
    if flair == None:
        flair = 'no flair'
    selftext = post.selftext
    if selftext == '':
        selftext = 'link'
    comment = ''
    post.comment_sort = 'best'
    comment = post.comments[0].body
    sub_dict['text'] = post.title + " " + selftext + " " + comment
    sub_dict['class'] = post.subreddit_name_prefixed
    hhhlst.append(sub_dict)



for post in reddit.subreddit('nba').top(limit=200):
    dict = vars(post)
    st = post.selftext
    # url = post.url
    # sub_dict = {field:dict[field] for field in fields}
    flair = post.link_flair_text
    sub_dict = {}
    if flair == None:
        flair = 'no flair'
    selftext = post.selftext
    if selftext == '':
        selftext = 'link'

    comment = ''
    post.comment_sort = 'best'
    comment = post.comments[0].body
    sub_dict['text'] = post.title + " " + selftext + " " + comment
    sub_dict['class'] = post.subreddit_name_prefixed
    nbalst.append(sub_dict)


print(hhhlst)

random.shuffle(hhhlst)
random.shuffle(nbalst)

trainnba = nbalst[0:100]
trainhhh = hhhlst[0:100]
traindata = trainnba + trainhhh
random.shuffle(traindata)

devnba = nbalst[100:150]
devhhh = hhhlst[100:150]
devdata = devnba + devhhh

testnba = nbalst[150:200]
testhhh = hhhlst[150:200]
testdata = testnba + testhhh

with open('hhhdata.json','w') as f:
    json.dump(hhhlst,f)

with open('nbadata.json','w') as f:
    json.dump(nbalst,f)

with open('traindata.json','w') as f:
    json.dump(traindata,f)

with open('hhhtrain.json','w') as f:
    json.dump(trainhhh,f)

with open('nbatrain.json','w') as f:
    json.dump(trainnba,f)

with open('hhhdev.json','w') as f:
    json.dump(devhhh,f)

with open('nbadev.json','w') as f:
    json.dump(devnba,f)

with open('devdata.json','w') as f:
    json.dump(devdata,f)

with open('hhhtest.json','w') as f:
    json.dump(testhhh,f)

with open('nbatest.json','w') as f:
    json.dump(testnba ,f)

with open('testdata.json','w') as f:
    json.dump(testdata,f)