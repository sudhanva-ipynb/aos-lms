from Importers.common_imports import *
from Importers.common_methods import *
from Config.key_manager import sessionManager
from Database.methods import *


def upload(course_name,data,term,filename):
    try:
        path = os.path.join(os.getcwd(),"Resources",term,course_name)
        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)
        with open(os.path.join(path, filename), 'wb') as f:
            f.write(data)
    except Exception as e:
        return e
