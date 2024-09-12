from Importers.common_imports import *
from protos import Lms_pb2,Lms_pb2_grpc

from Materials.upload_course_material import upload
from Config.decorators import access_token_required
# message UploadCourseMaterialRequest{
#     string course = 1;
#     string term = 2;
#     string filename = 3;
#     bytes data = 4;
#     string created = 5;
#     string token = 6;
#     }

class MaterialsService(Lms_pb2_grpc.MaterialsServicer):
    @access_token_required
    def courseMaterialUpload(self, request_iterator, context):
        data = b""
        course=None
        term = None
        filename= None
        for request in request_iterator:
            data += request.data
            course = request.course
            term = request.term
            filename = request.filename
        result = upload(course, data,term,filename)
        if result:
            return Lms_pb2.UploadCourseMaterialResponse(error=f"{result}",code="400")
        else:
            return Lms_pb2.UploadCourseMaterialResponse(size=str(sys.getsizeof(data)),code="200")

