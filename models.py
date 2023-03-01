import datetime as _dt
import sqlalchemy as _sql
import sqlalchemy.orm as _orm
import passlib.hash as _hash
import database as _database

Base = _orm.declarative_base()

class User(Base):
    __tablename__="users"
    id = _sql.Column(_sql.Integer, primary_key=True,index=True)
    first_name = _sql.Column(_sql.String)
    last_name= _sql.Column(_sql.String)
    email = _sql.Column(_sql.String, unique=True,index=True)
    hashed_password = _sql.Column(_sql.String)

    def verify_password(self,password:str):
        return _hash.bcrypt.verify(password,self.hashed_password)
class History(Base):
    __tablename__ = "historys"
    id = _sql.Column(_sql.Integer, primary_key=True,index=True)
    date_created = _sql.Column(_sql.DateTime, default=_dt.datetime.utcnow)
    output =_sql.Column(_sql.String)
class ListHistory(Base):
    __tablename__ = "listHistory"
    id = _sql.Column(_sql.Integer, primary_key=True,index=True)
    user_id = _sql.Column(_sql.Integer,_sql.ForeignKey("users.id"))
    id_history = _sql.Column(_sql.Integer,_sql.ForeignKey("historys.id"))
class File(Base):
    __tablename__="files"
    id = _sql.Column(_sql.Integer, primary_key=True,index=True)
    url = _sql.Column(_sql.String)
    user_id = _sql.Column(_sql.Integer,_sql.ForeignKey("users.id"))