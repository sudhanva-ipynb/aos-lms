from importlib.metadata import metadata

from Importers.common_imports import *
from Importers.common_methods import *
from Database.methods import *

def add_file(path,filename,name,data):
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)
        with open(os.path.join(path, "metadata.json"), 'wb') as f:
            metadata = {
                "_index": [],
                "_data": {}
            }
            f.write(json.dumps(metadata).encode('utf-8'))
    with open(os.path.join(path, "metadata.json"), 'r') as f:
        metadata = json.load(f)
    if name in metadata["_index"]:
        return "Material Already Exists"
    try:
        with open(os.path.join(path, f"{filename}_new"), 'wb') as f:
            f.write(data)
        metadata["_data"][name] = filename
        metadata["_index"].append(name)
        os.rename(os.path.join(path, f"{filename}_new"), os.path.join(path, f"{filename}"))
        with open(os.path.join(path, "metadata.json"), 'wb') as f:
            f.write(json.dumps(metadata).encode('utf-8'))
    except:
        if os.path.exists(os.path.join(path, f"{filename}_new")):
            os.remove(os.path.join(path, f"{filename}_new"))





def upload(course_name,data,term,filename,name):
    try:
        path = os.path.join(os.getcwd(),"Resources",term,course_name)
        if  os.path.exists(os.path.join(path,filename)):
            return "File already exists"
        error  = add_file(path,filename,name,data)
        if error:
            return error
    except Exception as e:
        return e

def get_material(name,path):
    buffer = None
    if not os.path.exists(path):
        return None,None, "Material Not Found"
    with open(os.path.join(path, "metadata.json"), 'r') as f:
        metadata = json.load(f)
    if name not in metadata["_index"]:
        return None,None, "Material Not Found"
    filename = metadata["_data"][name]
    if os.path.exists(os.path.join(path,filename)):
        buffer = BytesIO()
        with open(os.path.join(path,filename), "rb") as f:
            buffer.write(f.read())
            buffer.seek(0)

    return buffer,filename,None

def get_required_material(course_name,term,name):
    try:
        path = os.path.join(os.getcwd(),"Resources",term,course_name)
        return get_material(name,path)

    except Exception as e:
        return e

def get_course_contents(course_name,term):
    path = os.path.join(os.getcwd(), "Resources", term, course_name)
    if not os.path.exists(path):
        return None,"Course Not Found"
    with open(os.path.join(path, "metadata.json"), 'r') as f:
        metadata = json.load(f)
    return metadata["_index"],None

