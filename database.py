import sqlalchemy as _sql
import sqlalchemy.orm as _orm
from models import Base

DATABASE_URL = "sqlite:///./database.db"
engine = _sql.create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = _orm.sessionmaker(autocommit=False, autoflush=False, bind=engine)