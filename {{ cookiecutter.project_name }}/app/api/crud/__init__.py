# All the basic CRUD fuction for a model on crud.py and crud_noupdate.py
# Add the more complex functions on dedicate files

from app.api.crud.crud import CRUDBase
from app.api.crud.crud_noupdate import CRUDBaseNoUpdate

# Exemple :
# from usermanager.api.crud.crud import CRUDBase
# user_crud = CRUDBase[User, UserCreateDb, UserUpdate](User)
