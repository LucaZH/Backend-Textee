import fastapi as _fastapi
import fastapi.security as _security

import sqlalchemy.orm as _orm
import services as _services,schemas as _schemas
import models 
import passlib.hash as _hash
app=_fastapi.FastAPI()
@app.post("/api/users")
async def create_user(user:_schemas.UserCreate,db:_orm.Session=_fastapi.Depends(_services.get_db)):
    # db_user =await _services.get_user_by_email(user.email,db)
    # if db_user:
    #     raise _fastapi.HTTPException(status_code=400,detail="Email already in use")
    # return await _services.creat_user(user,db)
    db_user = models.User(email=user.email, hashed_password=_hash.bcrypt.hash(user.hashed_password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user