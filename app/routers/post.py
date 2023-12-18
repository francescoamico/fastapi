from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from .. import models, schemas
from ..oauth2 import get_current_user
from ..database import get_db

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session=Depends(get_db), current_user: int=Depends(get_current_user), limit: int=10, offset: int=0, search: Optional[str]=""):
    #cursor.execute("""SELECT * FROM posts""")
    #posts = cursor.fetchall()
    
    #left join by default
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).outerjoin(
        models.Vote, models.Vote.post_id==models.Post.id).group_by(models.Post.id).filter(
        models.Post.title.contains(search)).limit(limit).offset(offset).all()
    
    return posts

@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session=Depends(get_db), current_user: int=Depends(get_current_user)):
    #cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),))
    #post = cursor.fetchone()
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).outerjoin(
        models.Vote, models.Vote.post_id==models.Post.id).group_by(models.Post.id).filter(models.Post.id == id).first()
    
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"post {id} was not found")
    
    return post

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session=Depends(get_db), current_user: int=Depends(get_current_user)):
    #instead of using f'string we use %s to avoid SQL injection
    #cursor.execute("""INSERT INTO posts (title, content, published) VALUES(%s, %s, %s) RETURNING *""",
    #               (post.title, post.content, post.published))
    #new_post = cursor.fetchone()
    #conn.commit() #to update the db
    new_post = models.Post(**post.model_dump(), owner_id=current_user.id)
    
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

@router.delete("/{id}")
def delete_post(id: int, db: Session=Depends(get_db), current_user: int=Depends(get_current_user)):
    #cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    #deleted_post = cursor.fetchone()
    #conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"post {id} was not found")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                        detail="not authorized to perform request action")
    
    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session=Depends(get_db), current_user: int=Depends(get_current_user)):
    #cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
    #                (post.title,post.content,post.published, str(id)))
    #updated_post = cursor.fetchone()
    #conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"post {id} was not found")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                        detail="not authorized to perform request action")
    
    post_query.update(updated_post.model_dump(), synchronize_session=False)
    db.commit()

    return post_query.first()