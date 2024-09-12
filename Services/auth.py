import grpc

from protos import Lms_pb2,Lms_pb2_grpc
from Auth.login import login


class AuthService(Lms_pb2_grpc.AuthServicer):
    def studentLogin(self, request, context):
        token,courses,error = login(request.username, request.password,"Student")
        if error:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            return Lms_pb2.LoginResponse(error="Invalid email or password",code="401")
        else:
            return Lms_pb2.LoginResponse(token=token,courses=courses,code="200")

    def facultyLogin(self, request, context):
        try:
            token, courses, error = login(request.username, request.password, "Faculty")
            if error:
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                return Lms_pb2.LoginResponse(error="Invalid email or password", code="401")
            else:
                return Lms_pb2.LoginResponse(token=token, courses=courses, code="200")
        except Exception as e:
            print(e)

