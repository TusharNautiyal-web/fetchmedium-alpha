![logo-small](https://user-images.githubusercontent.com/74553737/179428806-ee2cb9c3-2ba5-47d6-abc4-5baf4d57019a.png)
![AppVeyor](https://img.shields.io/appveyor/build/tushar/fetchmedium)


# fetchmedium - API - V 0.0.1 - alpha

This repository contains the documentation for fetchmedium API 
```
@ Created By Tushar Natuiyal
@ version - alpha 0.0.1

```
# Read Complete Documentation
You can also start trying out the api by going to the docs clicking here.
<a href = 'https://fetchmediumapi.herokuapp.com/docs' target = "_blank">READ DOCS</a>
```api
 
 GET https://fetchmediumapi.herokuapp.com/docs

```


# Description
fetchmedium api lets u fetch your medium articles based on username , tags , publisher id etc it provides you with updated recent articles and also basic user data read documentation to know more. Please Understand this that its still in alpha phase and will be getting updates where more endpoints and features will be avalible.
Its free of cost api unlike the original medium api which requires a subscription here you can get the some basic benifits of medium for free.
<a href = 'https://fetchmediumapi.herokuapp.com/docs'>**Read Documentation**</a>

This api is completely free to use and feel free to clone the repo and contribute toward this.  
Please Configure you mongodb in .env files by creating a new .env file.

![docs](https://user-images.githubusercontent.com/74553737/179427603-ccf8a3eb-4249-45f3-9a16-f25c656a207f.png)

# For New Users
You will first need to create a api key. Following GET command does that but it will only work if you or the username you want blog data for is never registered. This is only for new users.

``` api

GET https://fetchmediumapi.herokuapp.com/generate/<your-username>/<your-email>/key

```

# Register Page For Username Exist
If the medium username is already taken or registered you can create your key and get the info for that user blog as this api only serves public data and can be used for education purpose only.
![register-page](https://user-images.githubusercontent.com/74553737/179427604-e3ec5e82-ba0d-44f8-8002-1bab844e1639.jpg)

```api

GET https://fetchmediumapi.herokuapp.com/register

```

```api

POST https://fetchmediumapi.herokuapp.com/process_form

```


# Local Configuiration and Contribution

This Api is created using fast api and uses pymonogo to connect to mongodb atlas cluster.
If you want to use the code for learning purposes you can clone my repo and modify code as per you like. 

You need to specify you MongoDB Url and you need to build a database.

Remember to give acess to your ip then create .env file and Store variable

```.env

MONGODB_URL = "<your-url>" 

```

## MongoDB SCHEMA
<table>
    <tr>
     <td>Username</td>
     <td>Email</td>
    <td>Key</tr></td>
    <td>String</td>
    <td>String</td>
    <td>String</td>
</table>



Install Requirements in requirements.txt to start the project this project is using fastapi-jinja for rendering html static page.
After installation of requirements and completed above steps you can deploy it with this command 

```python
uvicorn app:app --reload
```

If you like this repository and if this api was usefull for you please follow me on github, youtube or linkeding from above links. Thank you

