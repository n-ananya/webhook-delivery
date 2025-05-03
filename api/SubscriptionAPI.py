import logging
import uuid

from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from database.database import get_db
from entities.Subscription import Subscription
from models.SubscriptionDto import SubscriptionDto

logger = logging.getLogger(__name__)

sub_router = APIRouter()


@sub_router.post("/subscription")
def create_subscription(subscriptiondto: SubscriptionDto, db: Session = Depends(get_db)):
    try:
        print("Request: " + str(subscriptiondto))
        sub = create_sub_entity_from_dto(subscriptiondto)
        db.add(sub)
        db.commit()
        print(sub)
        return SubscriptionDto.from_orm(sub)
    except IntegrityError as e:
        print('Duplicate Data Found: ' + str(e))
        raise HTTPException(status_code=400, detail="Same Detail ALready Exists")
    except BaseException as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal server error")

@sub_router.get("/subscription/{id}")
def get_subscription(id: str, db: Session = Depends(get_db)):
    sub = db.query(Subscription).filter(Subscription.id == id).first()
    if sub is None:
        return HTTPException(status_code=404, detail="User Not Found")
    return SubscriptionDto.from_orm(sub)

@sub_router.put("/subscription")
def update_subscription(subscriptiondto: SubscriptionDto, db: Session = Depends(get_db)):
    sub = db.query(Subscription).filter(Subscription.id == subscriptiondto.id)
    if sub is None:
        return HTTPException(status_code=404, detail="User Not Found")
    update_sub_entity_from_dto(subscriptiondto, sub)
    db.commit()
    return SubscriptionDto.from_orm(sub)

@sub_router.delete("/subscription/{id}")
def delete_sub(id: str, db: Session = Depends(get_db)):
    db.query(Subscription).filter(Subscription.id == id).delte()
    db.commit()
    return "Subscription Deleted"

def create_sub_entity_from_dto(sub_dto: SubscriptionDto):
    now = func.now()
    return Subscription(
        id = str(uuid.uuid4()),
        name = sub_dto.name,
        tier = sub_dto.tier,
        email = sub_dto.email,
        description = sub_dto.description,
        sub_metadata = None,
        is_active = True,
        created_at = now,
        updated_at = None,
        expires_at = now + text("INTERVAL 1 MONTH")
    )

def update_sub_entity_from_dto(sub_dto: SubscriptionDto, sub_existing: Subscription):
    sub_existing.name = sub_dto.name
    sub_existing.tier = sub_dto.tier
    sub_existing.email = sub_dto.email
    sub_existing.description = sub_dto.description
    sub_existing.sub_metadata = None
    sub_existing.updated_at = func.now()
    return sub_existing