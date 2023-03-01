import datetime as _dt

import pydantic as _pydantic


class _UserBase(_pydantic.BaseModel):
    email: str


class UserCreate(_UserBase):
    first_name: str
    last_name: str
    hashed_password: str


    class Config:
        orm_mode = True


class User(_UserBase):
    id: int
    first_name: str
    last_name: str

    class Config:
        orm_mode = True


class _FileBase(_pydantic.BaseModel):
    url: str
    user_id: int


class FileCreate(_FileBase):
    pass

class File(_FileBase):
    id: int
    
    class Config:
        orm_mode = True




class HistoryCreate(_pydantic.BaseModel):
    output: str

class HistoryDelete(_pydantic.BaseModel):
    id: int
class HistoryResponse(_pydantic.BaseModel):
    id: int
class ListHistory(_pydantic.BaseModel):
    pass