
from Importers.common_imports import *
from Importers.common_methods import *
from Config.key_manager import sessionManager
from Database.methods import *

def generateExpiry():
    return (datetime.now() + timedelta(hours=2)).strftime("%Y%m%d%H%M%S")

def login(email,password,role):

    isUserValid,courses,id = validate_user(email,password,role)
    if isUserValid:
        token = sessionManager.encrypt(f"{id}|{role}|{generateExpiry()}")
        return token,",".join(courses),None
    else:
        return None,None,"Invalid Credentials"