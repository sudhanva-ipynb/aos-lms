import json


def validate_user(email,password):
    with open("lms_db.json", "r") as f:
        data = json.load(f)
        student = data.get("Student")
        _index = student["_index"].get(f"{email}")
        try:
            if student["_data"][_index].get("password") == password:
                return True
            else:
                return False
        except Exception as e:
            return False




