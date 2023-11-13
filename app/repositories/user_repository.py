from sqlalchemy.orm import Session
from app.models.user_model import User
from app.schemas.user_schema import UserRegistration, UserUpdate
from fastapi import HTTPException, status


class UserRepository:
    @staticmethod
    def get_user_by_username(db: Session, username: str):
        return db.query(User).filter(User.username == username)

    @staticmethod
    def get_user_by_email(db: Session, email: str):
        return db.query(User).filter(User.email == email)

    @staticmethod
    def get_user_by_id(db: Session, user_id: int):
        return db.query(User).filter(User.id == user_id)

    @staticmethod
    def create_user(db: Session, user: UserRegistration):
        user_db = User(username=user.username, email=user.email, hashed_password=user.password)
        db.add(user_db)
        db.commit()
        db.refresh(user_db)
        return user_db

    @staticmethod
    def update_user(db: Session, user_id: int, user_update: UserUpdate):
        user_db = db.query(User).filter(User.id == user_id).first()
        if user_db:
            if user_update.email:
                user_db.email = user_update.email
            if user_update.password:
                user_db.hashed_password = user_update.password
            if user_update.username:
                user_db.username = user_update.username
            if user_update.profile_photo:
                user_db.profile_photo = user_update.profile_photo
            db.commit()
            db.refresh(user_db)
            return user_db
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
