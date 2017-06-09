# -*- coding: utf-8 -*-

import vk
import requests
import time

#communities:
#bns_ru(off): 105256967
#overheard: 74555576
#funny: 106174694
#fans: 32024958

#CONNECT TO API
auth_params = {'client_id':'5837909', 'client_secret':'gihcjzIdvQ5sXXRg0xZa' } 
token = requests.get('https://oauth.vk.com/access_token', params = auth_params)
vers = 5.63 
session = vk.Session(access_token=token)
vkapi = vk.API(session, version = vers)

#GET POSTS FOR PERIOD
def getPosts(community,start, finish):
    try:
        posts = vkapi.wall.get(owner_id = -community)[0]
    except vk.exceptions.VkAPIError:
        time.sleep(0.3)        
    cycles = int((posts-(posts%100))/100)+1
    wall = []
    offset = 0
    for i in range(cycles):
        try:
            hundred = vkapi.wall.get(owner_id = -community, offset = offset, count = 100)
        except vk.exceptions.VkAPIError:
            time.sleep(0.3)
        wall.append(hundred)
        offset += 100
    fine_wall = []    
    for w in wall:
        for post in w:
            if type(post) == dict and post['date'] >= start and post['date'] <= finish:
                fine_wall.append(post)
    return fine_wall

def postData(post):
    post_id = post['id']
    reply_count = post['comments']['count']
    data = {post_id:reply_count}
    return data

#GET COMMENTS
def commentsFromPost(community,postid):
    post_comments = []
    comments_num = 0
    offset = 0
    hundred = []
    try:
        comments_num = vkapi.wall.getComments(owner_id = -community,post_id = postid)[0]
    except vk.exceptions.VkAPIError:
        time.sleep(0.3)
    except requests.exceptions.ReadTimeout:
        time.sleep(0.3)
    except requests.exceptions.ConnectionError:
        time.sleep(1)
    time.sleep(0.3)
    cycles = int((comments_num-(comments_num%100))/100)+1
    for i in range(cycles):
        try:
            hundred = vkapi.wall.getComments(owner_id = -community,post_id = postid,\
                                             sort = 'desc',need_likes = 1,offset = offset, count = 100)
        except vk.exceptions.VkAPIError:
            time.sleep(0.3)
        except requests.exceptions.ReadTimeout:
            time.sleep(0.3)
        except requests.exceptions.ConnectionError:
            time.sleep(1)
        time.sleep(0.3)
        for comment in hundred:
            if type(comment) == dict:
                comment['post_id'] = postid
                if comment not in post_comments:
                    post_comments.append(comment)
        offset += 100
    return post_comments

def allCommentsPeriod(community,start,finish):
    all_comments = []
    post_comments = []
    data = []
    posts = getPosts(community,start,finish)
    replies = 0
    for post in posts:
        data.append(postData(post))
    for i in range(len(data)): 
        replies += int(list(data[i].values())[0])
    while len(all_comments) < replies:
        for i in range(len(data)):
            post_id = list(data[i].keys())[0]
            post_comments += commentsFromPost(community,post_id)
            for comment in post_comments:
                if comment not in all_comments:
                    all_comments.append(comment)
                    print(len(all_comments))
                    print('Comments for period: ',replies)
                else:
                    post_comments.remove(comment)
            if len(all_comments) >= replies:
                break
        
    print('Ready: ',len(all_comments))
    return all_comments

#SAVE COMMENTS
def save_comment(community,comment):
    group_id = str(community)
    post_id = comment['post_id']
    comment_id = comment['cid']
    author = comment['from_id']
    date = comment['date']
    likes = comment['likes']['count']
    text = comment['text'].replace(',','_')
    text = text.replace(';','_')
    text = text.replace('\n','\\')
    try:
        reply_to_user = comment['reply_to_uid']
        reply_to_comment = comment['reply_to_cid']
    except KeyError:
        reply_to_user = 'empty'
        reply_to_comment = 'empty'
    comment_data = [group_id,post_id,comment_id,author,likes,reply_to_user,\
                    reply_to_comment,text,date]
    return comment_data

#SAVE POSTS
def save_post(post):
    post_id = post['id']
    date = post['date']
    #replies = post['reply_count']
    reposts = post['reposts']['count']
    likes = post['likes']['count']
    text = post['text'].replace(',','_') 
    text = text.replace('\n','')
    if post['post_type'] == 'copy':
        is_repost = 1
        copy_owner_id = post['copy_owner_id']
        copy_post_id = post['copy_post_id']
        try:
            copy_text = post['text'].replace(',','_')
            text = post['copy_text'].replace(',','_')
        except KeyError:
            copy_text = ''
        copy_text = copy_text.replace('\n','')
        text = text.replace('\n','')
    else:
        is_repost = 0
        copy_owner_id = ''
        copy_post_id = ''
        copy_text = ''
    post_data = [post_id,date,likes,reposts,\#replies,\
                is_repost,copy_owner_id,copy_post_id,copy_text,text]
    return post_data

community = 105256967 #bns ru 
start = 1445933550 
finish = 1491314739 
#posts = getPosts(community,start, finish)
#delta = (finish - start)/20 
#number = 8 #вот тут меняем!!! 
#comments = allCommentsPeriod(community,start+delta*number,start + delta*(number+1))

path = 'bns_ru\\posts bns_ru.csv'
with open(path,'w',encoding = 'utf-8')as f:
    #columns = ['group id','post id','comment id','author id','likes',\
    #'reply to user','reply to comment','text','date']
   # for column in columns:
    f.write('post id,date,likes,reposts,comments,is repost,owner,repost id,repost text,text\n')
    #for comment in comments:
     #   line = save_comment(community,comment)
      #  for element in line:
       #     f.write(str(element)+';')
        #f.write('\n')
    for post in posts:
        line = save_post(post)
        for element in line:
            f.write(str(element)+';')
        f.write('\n')
        