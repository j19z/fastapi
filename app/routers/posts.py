from typing import Optional, List

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from sqlalchemy import func

from .. import models, oauth2, schemas
from ..database import get_db

router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)

@router.get('/', response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), 
              current_user: int = Depends(oauth2.get_current_user), 
              limit: int = 10, 
              skip: int = 0,
              search: Optional[str] = ''):


    #results = db.query(models.Post, func.count(models.Vote.post_id).label('Votes')).join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True).group_by(models.Post.id).all()
    #results = list ( map (lambda x : x._mapping, results) )
    
    results = (db.query(models.Post, func.count(models.Vote.post_id).label('votes'))
                 .join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True)
                 .group_by(models.Post.id)
                 .filter(models.Post.title.contains(search))
                 .limit(limit)
                 .offset(skip)
                 .all())
    # Use this below if you only want to grab posts from the logged user. 
    # posts = db.query(models.Post).filter(models.Post.user_id == current_user.id).all()
    return results


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, 
                db: Session = Depends(get_db), 
                current_user: int = Depends(oauth2.get_current_user)):
    new_post = models.Post(user_id = current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get('/{id}', response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post = (db.query(models.Post, func.count(models.Vote.post_id).label('votes'))
              .join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True)
              .group_by(models.Post.id)
              .filter(models.Post.id == id)
              .first())
    
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Post with id: {id} does not exist.',
        )
    # Use this below if you only want to grab the post form the current user
    # if post.user_id != current_user.id:
    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN,
    #         detail='Not Authorized to perform requested action')
    return post


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_to_delete = db.query(models.Post).filter(models.Post.id == id)
    if post_to_delete.first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'post with id: {id} does not exist.',
        )

    if post_to_delete.first().user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Not Authorized to perform requested action')

    post_to_delete.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put('/{id}', response_model=schemas.Post)
def update_post(id: int, post: schemas.PostUpdate, 
                db: Session = Depends(get_db), 
                current_user: int = Depends(oauth2.get_current_user)):
    post_to_update = db.query(models.Post).filter(models.Post.id == id)
    if post_to_update.first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Post with id: {id} does not exist.',
        )

    if post_to_update.first().user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Not Authorized to perform requested action')

    post_to_update.update(post.model_dump(), synchronize_session=False)
    db.commit()
    return post_to_update.first()


