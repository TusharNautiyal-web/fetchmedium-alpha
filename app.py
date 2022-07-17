import uvicorn
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
import os
from dotenv import load_dotenv
import feedparser as feed
from bs4 import BeautifulSoup as bs
import uvicorn
import pymongo
from pymongo import MongoClient
import string    
import random 
import re
 
regex = re.compile('([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
 
 
load_dotenv()
database_url = os.getenv("MONGODB_URL")

app = FastAPI(title="fetchmedium", version="0.0.1")

# DB Setup
client = pymongo.MongoClient(database_url)
db = client.apirecords
collections = db['User_records']
templates = Jinja2Templates(directory="templates")


def validateEmail(email):
   if re.fullmatch(regex, email):
       return True
   else:
        return False
     
    
def checkifalreadyexist(username):
    cursor = collections.find({'Username': username})
    for doc in cursor:
        if(len(doc)!=0):
            return True
        else:
            return False

def checkifalreadyexist_user_key(username,key):
    result_key = ""
    result_user = ""
    cursor = collections.find({'Key': key})
    
    for doc in cursor:
        if(len(doc)!=0):
            result_key = True
        else:
            result_key = False
    cursor = collections.find({'Username': username})
    for doc in cursor:
        if(len(doc)!=0):
            result_user = True
        else:
            result_user = False
    if(result_user == False or result_key == False):
        return False
    elif(result_key==True and result_user == True):
        return True
    else:
        return False
    
def get_all_images(article_dict,feed,image_value = 'thumbnail',):
    article_wise_images = {}
    thumbnail_image = {}
    temp = []
    if(feed == 'user'):   
        for article in article_dict: 
            content = article_dict[article]['content'][0]['value']
            soup = bs(content,features="lxml")
            images = soup.findAll('img')
            for img in images:
                if img.has_attr('src'):
                     temp.append(img['src'])
            article_wise_images[article] = temp
            thumbnail_image[article] = temp[0] 
            
    if(feed == 'tag'):
        for article in article_dict: 
            content = article_dict[article]['summary']
            soup = bs(content,features="html.parser")
            images = soup.findAll('img')
            for img in images:
                if img.has_attr('src'):
                     temp.append(img['src'])
            article_wise_images[article] = temp
            thumbnail_image[article] = temp[0]
    
    if(image_value == 'all'):
        return article_wise_images
    elif(image_value == 'thumbnail'):
        return thumbnail_image



@app.get('/')
def root():
    message = {
    'Message': 'Please Read Docs To Understand Working of this API.',
    'Platforms-Supported': 'Medium.com',
    'Channels': '/get_latest/tags, /@username/key, /@publication-name/key',
    'Authentication': 'Please Generate your unique key first',
    'Auth-url':'generate/@username/',
    'Docs': '/docs' 
        }
    return message


@app.get('/register')
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post('/process_form', response_class=HTMLResponse)
def process_application(request: Request, Username: str = Form(...) , Email: str = Form(...), Exist: str = Form(...)):
    username  = Username
    email = Email
    exists = Exist
    if(exists == 'not_exist'):
        if username[0] != '@':
            return JSONResponse(
            status_code=400,
            content={"message": str("Try Again"),"Error": "Wrong Format of Username"},)
        if (validateEmail(email)==False):
            return JSONResponse(
            status_code=400,
            content={"message": str("Try Again"),"Error": "Wrong Format of Email"},)
        else:
            response = generate_key(username,email)
            return JSONResponse(
            status_code=200,
            content={"message": str("Success"),"response":response},
            )
    
    elif(exists =='exist'):
        if username[0] != '@':
            return JSONResponse(
            status_code=400,
            content={"message": str("Try Again"),"Error": "Wrong Format of Username"},)
        if (validateEmail(email)==False):
            return JSONResponse(
            status_code=400,
            content={"message": str("Try Again"),"Error": "Wrong Format of Email"},) 
        else:   
            S = 10
            key = ''.join(random.choices(string.ascii_uppercase + string.digits, k = S))
            collections.insert_one({'Email':email,'Username':username,'Key': key})
            response =  {"Your Key" : key, "Your Username": username}
            return JSONResponse(
            status_code=200,
            content={"message": str("Success"),"username": username, "key": key},
        )
    
    

@app.get('/{name}')
def root_name(name: str):
    return f"Hi {name} Please Generate your unique key."

@app.get('/generate/{username}/{email}/key')
def generate_key(username: str, email: str):
   
    if username[0] != '@':
        return {'Wrong Username': 'This API Only support medium articles for now.'}
    elif(validateEmail(email)==False):
        return JSONResponse(
        status_code=400,
        content={"message": str("Try Again"),"Error": "Wrong Format of Email"},)
    
    elif(checkifalreadyexist(username)==True):
        return {'Error': 'Username Already Exist Please Get your Key Using Form'}
    
    else:
        S = 10
        key = ''.join(random.choices(string.ascii_uppercase + string.digits, k = S))
        collections.insert_one({'Email':email,'Username':username,'Key': key})
        return JSONResponse(
        status_code=200,
        content={"message": str("Sucess"),"Your Username": username, "Your Key": key},)
    
# Latest Post Top 10
@app.get("/get_latest/{tags}")
def get_latest(tags: str):
    data_dict = {}
    tag_link = f'http://medium.com/feed/tag/{tags}'
    fetch_data = feed.parse(tag_link)
    for i,d in enumerate(fetch_data.entries):
        data_dict[f"article_{i}"] = fetch_data.entries[i]
    
    #Popping out useless content.
    pop_list1 = ["title_detail","id","guidislink","authors","published_parsed","updated_parsed","links"]
    for article in data_dict:
        for items in pop_list1:
            if(data_dict[article].has_key("summary_detail")):
                data_dict[article].pop(items)
                data_dict[article].pop("summary_detail")
            else:
                data_dict[article].pop(items)
    # Data Cleaning Process and Adding Process
    for article in data_dict:
        link = data_dict[article]["link"]
        data_dict[article]["link"] = link.split('?',1)[0]
        
    # Getting All images
    all_images = get_all_images(data_dict,"tag",image_value = "all")
    thumbnails =  get_all_images(data_dict,"tag",image_value = "thumbnail")
    
    for article in data_dict:
        data_dict[article]['image_links'] = all_images[article]
        data_dict[article]['thumbnail'] = thumbnails[article]
    
    return data_dict

# Medium User Profie Data
@app.get("/{username}/{key}/user_data")
def user_data(username: str,key: str):
    if(checkifalreadyexist_user_key(username,key)==True):
        user_data_link = f"http://medium.com/feed/{username}"
        data = feed.parse(user_data_link)
        user_data  = data.feed
        user_data['profile_pic'] = user_data['image'].href
        user_data['link'] = str(user_data['link']).split('?',1)[0]
        unecessary = ['title_detail','subtitle','subtitle_detail','links','generator_detail','image','updated_parsed','publisher','publisher_detail'] 
        for e in unecessary: 
            user_data.pop(e)
        return user_data
    
    else:
        return "please genearte your key or username first"


@app.get("/{username}/{key}/recent-articles/name")
def get_articles_name(username: str, key: str):
    if(checkifalreadyexist_user_key(username,key)==True):
        user_data_link = f"http://medium.com/feed/{username}"
        info = feed.parse(user_data_link)
        data = info['entries']
        article_dict = {}
        for i,info in enumerate(data):
            article_dict[f'article_{i}'] = info

        # Removing Unecessary things from the feed
        for article in article_dict:
            article_dict[article].pop('title_detail')
            if(article_dict[article].has_key('summary_detail')):
                article_dict[article].pop('summary_detail')
            article_dict[article].pop('links')
            article_dict[article].pop('guidislink')
            article_dict[article].pop('published_parsed')
            article_dict[article].pop('authors')
            article_dict[article].pop('author_detail')
            article_dict[article].pop('updated_parsed')

        # Converting link from rss to normal
        for article in article_dict:
            temp = str(article_dict[article]['link'])
            article_dict[article]['link'] = temp.split('?',1)[0]
        
        top10 = []
        for article in article_dict:
            top10.append(article_dict[article].title)
            
        return top10
    
    else:
        return "Invalid Registration Please Get your api key or Register."
        
@app.get("/{username}/{key}/recent-articles")
def get_articles(username: str, key: str):
    if(checkifalreadyexist_user_key(username,key)==True):
        user_data_link = f"http://medium.com/feed/{username}"
        info = feed.parse(user_data_link)
        data = info['entries']
        article_dict = {}
        for i,info in enumerate(data):
            article_dict[f'article_{i}'] = info

        # Removing Unecessary things from the feed
        for article in article_dict:
            article_dict[article].pop('title_detail')
            if(article_dict[article].has_key('summary_detail')):
                article_dict[article].pop('summary_detail')
            article_dict[article].pop('links')
            article_dict[article].pop('guidislink')
            article_dict[article].pop('published_parsed')
            article_dict[article].pop('authors')
            article_dict[article].pop('author_detail')
            article_dict[article].pop('updated_parsed')

        # Converting link from rss to normal
        for article in article_dict:
            temp = str(article_dict[article]['link'])
            article_dict[article]['link'] = temp.split('?',1)[0]
        all_images = get_all_images(article_dict,"tag",image_value = "all")
        thumbnails =  get_all_images(article_dict,"tag",image_value = "thumbnail")
        
        for article in article_dict:
            article_dict[article]['image_links'] = all_images[article]
            article_dict[article]['thumbnail'] = thumbnails[article]
        return article_dict
    
    else:
        return "Invalid Registration Please Get your api key or Register."


    
        

if __name__=='__main__':
    uvicorn.run(app, host = '0.0.0.0', port = '8000')