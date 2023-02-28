from database import *
import sqlalchemy.orm as _orm
from models import *
from schemas import *
import passlib.hash as _hash
def create_database():
    return Base.metadata.create_all(bind=engine)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
async def get_user_by_email(email:str,db:_orm.Session):
    return db.query(User).filter(User.email==email).first()
async def creat_user(user: UserCreate,db:_orm.Session):
    # user_obj = User(email=user.email, hashed_password=_hash.bcrypt.hash(user.hashed_password))
    # db.add(user_obj)
    # db.commit()
    # db.refresh(user_obj)
    db_user = User(email=user.email, hashed_password=_hash.bcrypt.hash(user.hashed_password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user