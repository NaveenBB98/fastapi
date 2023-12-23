from fastapi import Response, status, HTTPException, Depends, APIRouter
from typing import List
from random import randrange
from .. import oauth2
from typing import Optional

import time
from .. import models,schemas
from ..database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import func

router=APIRouter(prefix='/posts',tags=['Posts'])

# @router.get('/',response_model=List[schemas.Post])
# def get_posts(db:Session=Depends(get_db),current_user: int=Depends(oauth2.get_current_user),limit:int=10,skip:int=0,search:Optional[str]=""):
#     # my_posts=db.query(models.Post).filter(models.Post.owner_id==current_user.id).all()
#     my_posts=db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    
#     return my_posts

@router.get('/',response_model=List[schemas.PostOut])
def get_posts(db:Session=Depends(get_db),current_user: int=Depends(oauth2.get_current_user),limit:int=10,skip:int=0,search:Optional[str]=""):
    # my_posts=db.query(models.Post).filter(models.Post.owner_id==current_user.id).all()
    # my_posts=db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    results=db.query(models.Post,func.count(models.Vote.post_id).label('votes')).join(models.Vote,models.Vote.post_id==models.Post.id,isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    return results

# @app.post('/createposts')
# def create_posts(payload: dict=Body(...)):
#     print(payload)
#     return {'new_post': f"title {payload['title']} content {payload['content']}"}

# @app.post('/posts', status_code=status.HTTP_201_CREATED)
# def create_posts(post:Post):
#     post_dict=post.dict()
#     post_dict['id']=randrange(1,10000)
#     my_posts.append(post_dict)
#     print(post.rating)
#     return {'data':post_dict}

@router.post('/', status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_posts(post:schemas.PostCreate,db:Session=Depends(get_db),current_user: int=Depends(oauth2.get_current_user)):
    # cursor.execute('''INSERT INTO posts(title,content,published) VALUES(%s,%s,%s) RETURNING *''',(post.title,post.content,post.published))
    # new_post=cursor.fetchone()
    # conn.commit()
    # new_post=models.Post(title=post.title,content=post.content,published=post.published)
    #instead of the above line
    print(current_user.email)
    new_post=models.Post(owner_id=current_user.id,**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

# @app.get('/posts/{id}')
# def get_post(id: int, response: Response):
#     print(type(id))
#     post=find_post(id)
#     if not post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='post not found')
#         response.status_code=status.HTTP_404_NOT_FOUND
#         return {'message':'post not found'}
#     return {'data':post}

@router.get('/{id}',response_model=schemas.Post)
def get_post(id: int, response: Response,db:Session=Depends(get_db),current_user: int=Depends(oauth2.get_current_user)):
    # cursor.execute('''SELECT * FROM posts WHERE id=%s''',(str(id)))
    # post=cursor.fetchone()
    post=db.query(models.Post).filter(models.Post.id==id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='post not found')
        response.status_code=status.HTTP_404_NOT_FOUND
        return {'message':'post not found'}
    if post.owner_id!=current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="This user is not allowed to delete")
    return post

# @app.delete('/posts/{id}',status_code=status.HTTP_204_NO_CONTENT)
# def delete_post(id: int):
#     index=find_post_index(id)
#     if index==None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Id doesn't exist")
#     my_posts.pop(index)
#     return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.delete('/{id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db:Session=Depends(get_db),current_user: int=Depends(oauth2.get_current_user)):
    # cursor.execute('''DELETE FROM posts WHERE id=%s RETURNING *''',(str(id)))
    # post=cursor.fetchone()
    # conn.commit()
    post_query=db.query(models.Post).filter(models.Post.id==id)
    post=post_query.first()
    
    if post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Id doesn't exist")
    if post.owner_id!=current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="This user is not allowed to delete")
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# @app.put('/posts/{id}')
# def get_post(id: int, post:Post):
#     index=find_post_index(id)
#     if index==None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Id doesn't exist")
#     post_dict=post.dict()
#     post_dict['id']=id
#     my_posts[index]=post_dict
#     return {'updated data':post_dict}


@router.put('/{id}',response_model=schemas.Post)
def get_post(id: int, updated_post:schemas.PostCreate, db:Session=Depends(get_db),current_user: int=Depends(oauth2.get_current_user)):
    # cursor.execute('''UPDATE posts SET title=%s,content=%s,published=%s WHERE id=%s RETURNING *''',(post.title,post.content,post.published,str(id)))
    # conn.commit()
    # updated_post=cursor.fetchone()
    post_query=db.query(models.Post).filter(models.Post.id==id)
    post=post_query.first()

    
    if post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Id doesn't exist")
    if post.owner_id!=current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="This user is not allowed to delete")
    post_query.update(updated_post.dict(),synchronize_session=False)

    db.commit()
    
    return post_query.first()