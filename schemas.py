import datetime as _dt
import pydantic as _pydantic


class _UserBase(_pydantic.BaseModel):
    email: str

class UserCreate(_UserBase):
    hashed_password: str

class User(_UserBase):
    id: int

    class Config:
        orm_mode = True

class _LeadBase(_pydantic.BaseModel):
    prenom: str
    nom: str
    email: str
    entreprise: str = ""
    note: str = ""

class LeadCreate(_LeadBase):
    pass

class Lead(_LeadBase):
    id: int
    proprietaire_id: int
    date_creation: _dt.datetime
    date_derniere_mise_a_jour: _dt.datetime

    class Config:
        orm_mode = True
