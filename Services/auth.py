from protos import Lms_pb2,Lms_pb2_grpc
from Auth.login import login


class AuthService(Lms_pb2_grpc.AuthServicer):
    def studentLogin(self, request, context):
        result = login(request.username, request.password)
        if not result:
            return Lms_pb2.LoginResponse(error="Invalid email or password",code="401")
        else:
            return Lms_pb2.LoginResponse(token=result,code="200")

