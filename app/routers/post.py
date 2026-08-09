from .. import schemas, models, oauth2
from fastapi import FastAPI, Response,status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db 
from typing import Optional, List
from sqlalchemy import func

router = APIRouter(
    prefix="/posts",
    tags=['posts']
)


# @router.get("/", response_model=List[schemas.Post])

@router.get("/", response_model=List[schemas.PostOut])

def get_posts(db: Session = Depends(get_db),  
                 current_user: int = Depends(oauth2.get_current_user),
                 limit: int = 10, skip : int = 2,
                 search: Optional[str] = ""):
    # print(limit)
    # cursor.execute(
    
    #     """
    #     SELECT * from posts
    #     """
    # )
    # posts = cursor.fetchall()
  
    #posts = db.query(models.Post).filter(models.Post.owner_d == current_user.id ).all() --. prvate posts of current users
    #posts = db.query(models.Post).all() ---- all parameters for query parameter
    #posts = db.query(models.Post).limit(limit).offset(skip).all()
    
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, 
                                         isouter= True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    return posts

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post : schemas.PostCreate, db: Session = Depends(get_db), 
                 current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute(""" 
                   
    #                INSERT INTO posts (title, content, published) VALUES(%s, %s, %s) 
    #                RETURNING * """, (post.title, post.content, post.published))
   
    # conn.commit()
    # new_post = cursor.fetchone()
    #print(post.model_dump())
    # sql alchemy creat record 
    #new_post = models.Post(title = post.title, content = post.content, published = post.published)
    #print(current_user.id)
    new_post = models.Post(owner_d=current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

#@router.get("/{id}", response_model=schemas.Post) ---- with out sql joins
@router.get("/{id}", response_model=schemas.PostOut) # with joins
def get_post(id: int, db: Session = Depends(get_db), 
             current_user: int = Depends(oauth2.get_current_user)): 
    
    # cursor.execute(""" SELECT * from posts where id = %s
    #                """, (str(id),))
    # post = cursor.fetchone()
    #post  = db.query(models.Post).filter(models.Post.id == id).first()
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, 
                                         isouter= True).group_by(models.Post.id).filter(models.Post.id == id).first()
    if not post :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id : {id } was not found")
        
    if post.Post.owner_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                                detail=f"Not autherized to perform requested action.")
            
    
   # print(post)
    return post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id : int, db: Session = Depends(get_db), 
                 current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute(
    #     """     DELETE FROM posts WHERE id = %s RETURNING *
    #                """, (str(id),))
    # delete_post = cursor.fetchone()
    # conn.commit()
    
    # if delete_post is None:
    #     raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    
    post_query  = db.query(models.Post).filter(models.Post.id == id)
    
    post = post_query.first()
    
    if post is None:
            raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
        
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail=f"Not autherized to perform requested action.")
        
    post_query.delete(synchronize_session=False)
    db.commit()
    
    
    return Response(status_code = status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post:schemas.PostCreate, db: Session = Depends(get_db), 
                 current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""
    #                UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s
    #                RETURNING * """, (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    
    # if updated_post is None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id : {id} doe not exist")
   
    # return {'data': updated_post}
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id : {id} doe not exist")
    # post_query.update({'title':'this is updated title for the post one: Welcome to the stage', 
    #                    'content':'this is my updated content for post of that id'}, synchronize_session=False)
    
    if post.owner_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                                detail=f"Not autherized to perform requested action.")
    
    post_query.update(updated_post.model_dump(), synchronize_session=False)
    db.commit()
    return post_query.first()


