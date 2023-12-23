from fastapi import FastAPI

from . import models
from .database import engine
from .routers import post,user,auth,vote
from .config import settings
from fastapi.middleware.cors import CORSMiddleware

# models.Base.metadata.create_all(bind=engine)

app=FastAPI()

origins=['https://www.google.com']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)
# print(settings.path)



# my_posts=[{'title':'who are you','content':'explain who the hell are you','id':1},
#           {'title':'what is it','content':'explain what exactly is it','id':2}]

@app.get('/')
def root():
    return {'message':'This is the homepage'}

# def find_post(id):
#     for p in my_posts:
#         if p['id']==id:
#             return p
        
# def find_post_index(id):
#     for i,p in enumerate(my_posts):
#         if p['id']==id:
#             return i
        

# @app.get('/posts')
# def get_posts():
#     cursor.execute('''SELECT * FROM posts ''')
#     my_posts=cursor.fetchall()
#     print(my_posts)
#     return my_posts
        
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)





