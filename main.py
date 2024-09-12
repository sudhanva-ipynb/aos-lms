from Importers.common_imports import *
from Services.auth import *
from Config.key_manager import sessionManager
from  Materials.course_materials import *
from Services.materials import MaterialsService

# class Students(BaseModel):
#     emailId : str
#     studentId : str
#     name : str
#     courses : List[str]
#
#
# class Course(BaseModel):
#     Id : str
#     courseName :  str
#     facultyId : str
#
#
#
#
# class Faculty(BaseModel):
#     emailId : str
#     facultyId : str
#     name : str
#     courses : List[str]
#
# def generateKey(payload):
#     return sessionManager.encrypt(payload)
#
#
# def register():
#     students_db = [{
#         "email": "",
#         "studentId": "",
#         "name": "",
#         "courses": ["AOS", "SEM"],
#         "session_id":"",
#         "session_expiry":""
#
#     }]
#     faculty_db = [
#         {
#             "emailId":"",
#             "facultyId":"",
#             "name":"",
#             "courses":["AOS", "SEM"],
#         }
#     ]
#     courses_db = [
#         {
#             "Id":"",
#             "courseName":"",
#             "facultyId":""
#         }
#     ]

# with open("README.md", "rb") as fh:
#     data = fh.read()
# upload("AOS",data,"20241","trial.md")
def serve():
    port = "50051"
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    Lms_pb2_grpc.add_AuthServicer_to_server(AuthService(), server)
    Lms_pb2_grpc.add_MaterialsServicer_to_server(MaterialsService(), server)
    server.add_insecure_port("[::]:" + port)
    server.start()
    print("Server started, listening on " + port)
    server.wait_for_termination()

if __name__ == '__main__':
    serve()