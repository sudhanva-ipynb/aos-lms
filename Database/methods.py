import json


def validate_user(email,password,role):
    with open("lms_db.json", "r") as f:
        data = json.load(f)
        user = data.get(role)
        _index = user["_index"].get(f"{email}")
        try:
            if user["_data"][_index].get("password") == password:
                return True,user["_data"][_index].get("courses",[]),user["_data"][_index].get("id")
            else:
                return False,None,None
        except Exception as e:
            return False,None,None




