from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.depends import get_db, get_current_user
from app.schemas.user_schema import UserOut
from app.schemas.producer_schema import ProducerCreate
from . import router, producer_repo


@router.post("/producers")
async def post_producers(producer: ProducerCreate, db: Session = Depends(get_db),
                         user: UserOut = Depends(get_current_user)):
    try:
        if user.is_moderator or user.is_superuser:
            if producer_repo.get_producer_by_name(db, producer.name):
                raise HTTPException(detail="The producer already exists", status_code=status.HTTP_409_CONFLICT)
            producer_repo.create_producer(db, producer)
            return {"message": f"{producer.name} successful created"}
        raise HTTPException(detail="Only superuser or moderator has access", status_code=status.HTTP_403_FORBIDDEN)
    except Exception as e:
        raise HTTPException(detail=e.__class__.__name__, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
