from database import *
import sqlalchemy.orm as _orm
from models import *
from schemas import *
import fastapi as _fastapi
import fastapi.security as _security
import passlib.hash as _hash
import jwt as _jwt
import  models as _models, schemas as _schemas
import datetime as _dt
oauth2schema = _security.OAuth2PasswordBearer(tokenUrl="/api/token")
JWT_SECRET = "myjwtsecret"
def create_database():
    return _models.Base.metadata.create_all(bind=engine)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
async def get_user_by_email(email:str,db:_orm.Session):
    return db.query(User).filter(User.email==email).first()
async def creat_user(user: UserCreate,db:_orm.Session):
    db_user = User(first_name=user.first_name,last_name=user.last_name,email=user.email,hashed_password=_hash.bcrypt.hash(user.hashed_password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
async def authenticate_user(email: str, password: str, db: _orm.Session):
    user = db.query(_models.User).filter(_models.User.email == email).first()
    if not user:
        return False

    if not user.verify_password(password):
        return False

    return user
async def create_token(user: User):
    user_obj = User.from_orm(user)

    token = _jwt.encode(user_obj.dict(), JWT_SECRET)

    return dict(access_token=token, token_type="bearer")
async def get_current_user(
    db: _orm.Session = _fastapi.Depends(get_db),
    token: str = _fastapi.Depends(oauth2schema),
):
    try:
        payload = _jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        user = db.query(_models.User).get(payload["id"])
    except:
        raise _fastapi.HTTPException(
            status_code=401, detail="Invalid Email or Password"
        )

    return _schemas.User.from_orm(user)
async def save_url_file( file: _schemas.FileCreate,user:_schemas.User,db=_orm.Session):
    print(file)
    file = File(file,user_id=user.id)
    db.add(file)
    db.commit()
    db.refresh(file)
    return _schemas.File.from_orm(file)

# async def addhistory()