
from Importers.common_imports import *
from Importers.common_methods import *
from Config.key_manager import sessionManager
from Database.methods import *

def generateExpiry():
    return (datetime.now() + timedelta(hours=2)).strftime("%Y%m%d%H%M%S")

def login(email,password):

    isUserValid = validate_user(email,password)
    if isUserValid:
        token = sessionManager.encrypt(f"{email}|{password}|{generateExpiry()}")
        return token
    else:
        return