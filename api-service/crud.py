from sqlalchemy.orm import Session
import models


# ================================
#  CREATE
# ================================
def create_transaction(db: Session, data):
    transaction = models.Transaction(**data.dict())
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    return transaction


# ================================
#  GET ALL
# ================================
def get_all(db: Session):
    return db.query(models.Transaction).all()


# ================================
#  GET ONE
# ================================
def get_one(db: Session, id: str):
    return db.query(models.Transaction).filter(models.Transaction.id == id).first()


# ================================
#  DELETE
# ================================
def delete_transaction(db: Session, id: str):
    obj = get_one(db, id)
    if obj:
        db.delete(obj)
        db.commit()
    return obj

# ================================
#  UPDATE (NEW)
# ================================
def update_transaction(db: Session, id: str, data):
    obj = get_one(db, id)
    if not obj:
        return None
    obj.user_id = data.user_id
    obj.amount = data.amount
    obj.category = data.category
    obj.status = data.status

    db.commit()
    db.refresh(obj)

    return obj