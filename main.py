import datetime as _dt
import fastapi as _fastapi
from typing import List
import fastapi.security as _security
import fastapi.exceptions as _exceptions
import sqlalchemy.orm as _orm
import services as _services,schemas as _schemas
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import SQLAlchemyError
import models 
import passlib.hash as _hash
from fastapi import File, UploadFile
import os
app=_fastapi.FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.post("/api/token")
async def generate_token(
    data: dict,
    db: _orm.Session = _fastapi.Depends(_services.get_db),
):
    email = data.get("email")
    password = data.get("password")
    user = await _services.authenticate_user(email, password, db)

    if not user:
        raise _fastapi.HTTPException(status_code=401, detail="Invalid Credentials")

    return await _services.create_token(user)
@app.post("/api/token")
async def generate_token(
    form_data: _security.OAuth2PasswordRequestForm = _fastapi.Depends(),
    db: _orm.Session = _fastapi.Depends(_services.get_db),
):
    user = await _services.authenticate_user(form_data.username, form_data.password, db)

    if not user:
        raise _fastapi.HTTPException(status_code=401, detail="Invalid Credentials")

    return await _services.create_token(user)
@app.get("/api/users/me", response_model=_schemas.User)
async def get_user(user: _schemas.User = _fastapi.Depends(_services.get_current_user)):
    return user

@app.post("/upload")
async def upload(file: UploadFile = File(...),user: _schemas.User = _fastapi.Depends(_services.get_current_user),db: _orm.Session = _fastapi.Depends(_services.get_db)):
    try:
        print(os.getcwd())
        contents = file.file.read()
        with open("./files/"+file.filename, 'wb') as f:
            f.write(contents)
        file_name = os.getcwd()+"/files/"+file.filename.replace(" ", "-")
        db_file = models.File(url=file_name, user_id=user.id)
        db.add(db_file)
        db.commit()
    except Exception:
        print(Exception)
        return {"message": "There was an error uploading the file"}
    finally:
        file.file.close()
    return {"message": f"Successfully uploaded {file_name}"}
@app.post("/history")
async def create_history(history:_schemas.HistoryCreate, db: _orm.Session = _fastapi.Depends(_services.get_db),user: _schemas.User = _fastapi.Depends(_services.get_current_user)):
    new_history = models.History(output=history.output)
    db.add(new_history)
    db.commit()
    db.refresh(new_history)
    return {"message": "History created successfully", "history": new_history}

@app.delete("/history")
async def delete_history(history: _schemas.HistoryDelete, db: _orm.Session = _fastapi.Depends(_services.get_db),user: _schemas.User = _fastapi.Depends(_services.get_current_user)):
    history_to_delete = db.query(models.History).filter(models.History.id == history.id).first()
    if not history_to_delete:
        raise _fastapi.HTTPException(status_code=404, detail="History not found")
    db.delete(history_to_delete)
    db.commit()
    return {"message": "History deleted successfully"}

@app.get("/history")
def get_history_ids(user: _schemas.User = _fastapi.Depends(_services.get_current_user), db: _orm.Session = _fastapi.Depends(_services.get_db)):
    
    histories = db.query(_schemas.ListHistory.id_history).filter_by(user_id=user.id).all()
    response = [_schemas.HistoryResponse(id=history[0]) for history in histories]
    return response
    # except SQLAlchemyError:
    #     raise _fastapi.HTTPException(status_code=500, detail="Database error")
    # except:
    #     raise _fastapi.HTTPException(status_code=400, detail="Bad request")