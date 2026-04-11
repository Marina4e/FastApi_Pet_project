from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.models import Article, User
from app.auth.schemas import ArticleBase, ArticleOut, UserShort, UserDetail
from app.dependencies import get_db, get_current_user

router = APIRouter(prefix="/articles", tags=["Articles"])


# ✅ CREATE ARTICLE
@router.post("/", response_model=ArticleOut)
def create_article(
        article: ArticleBase,
        db: Session = Depends(get_db),
        user=Depends(get_current_user)
):
    new_article = Article(
        title=article.title,
        content=article.content,
        owner_id=user.id
    )

    db.add(new_article)
    db.commit()
    db.refresh(new_article)

    return new_article


# ✅ GET ALL ARTICLES
@router.get("/", response_model=list[ArticleOut])
def get_articles(
        db: Session = Depends(get_db),
        user=Depends(get_current_user)
):
    return db.query(Article).all()


# ✅ GET USER ARTICLES
@router.get("/user/{user_id}", response_model=list[ArticleOut])
def get_user_articles(
        user_id: int,
        db: Session = Depends(get_db),
        user=Depends(get_current_user)
):
    return db.query(Article).filter(Article.owner_id == user_id).all()


# ✅ GET ARTICLE
@router.get("/{article_id}", response_model=ArticleOut)
def get_article(
        article_id: int,
        db: Session = Depends(get_db),
        user=Depends(get_current_user)
):
    article = db.query(Article).filter(Article.id == article_id).first()

    if not article:
        raise HTTPException(status_code=404, detail="Article not found")

    return article


# ✅ FOLLOW USER
@router.post("/follow/{user_id}")
def follow_user(
        user_id: int,
        db: Session = Depends(get_db),
        current_user=Depends(get_current_user)
):
    user_to_follow = db.query(User).filter(User.id == user_id).first()

    if not user_to_follow:
        raise HTTPException(status_code=404, detail="User not found")

    current_user.following.append(user_to_follow)
    db.commit()

    return {"msg": "Followed"}


# ✅ GET FOLLOWERS
@router.get("/followers/{user_id}", response_model=list[UserShort])
def get_followers(
        user_id: int,
        db: Session = Depends(get_db),
        user=Depends(get_current_user)
):
    user_db = db.query(User).filter(User.id == user_id).first()

    if not user_db:
        raise HTTPException(status_code=404)

    return user_db.followers


# ✅ GET FOLLOWING
@router.get("/following/{user_id}", response_model=list[UserShort])
def get_following(
        user_id: int,
        db: Session = Depends(get_db),
        user=Depends(get_current_user)
):
    user_db = db.query(User).filter(User.id == user_id).first()

    if not user_db:
        raise HTTPException(status_code=404)

    return user_db.following


@router.get("/user-full/{user_id}", response_model=UserDetail)
def get_user_full(
        user_id: int,
        db: Session = Depends(get_db),
        user=Depends(get_current_user)
):
    user_db = db.query(User).filter(User.id == user_id).first()

    if not user_db:
        raise HTTPException(status_code=404, detail="User not found")

    return user_db
