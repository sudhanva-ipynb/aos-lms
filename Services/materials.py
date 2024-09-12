from Importers.common_imports import *
from protos import Lms_pb2,Lms_pb2_grpc

from Materials.course_materials import upload, get_course_contents, get_required_material
from Config.decorators import faculty_access_token_required,any_access_token_required



def generate_data(name, filename, data, error=None):
    chunk_size = 2 * 1024
    while chunk := data.read(chunk_size):
        yield Lms_pb2.GetCourseMaterialResponse(name=name, filename=filename, data=chunk)


class MaterialsService(Lms_pb2_grpc.MaterialsServicer):
    @faculty_access_token_required
    def courseMaterialUpload(self, request_iterator, context):
        data = b""
        course=None
        term = None
        filename= None
        name = None
        req_count = 0
        for request in request_iterator:
            req_count += 1
            data += request.data
            course = request.course
            term = request.term
            filename = request.filename
            name = request.name
        if req_count == 0:
            return Lms_pb2.UploadCourseMaterialResponse(size="0", code="200")
        result = upload(course, data,term,filename,name)
        if result:
            return Lms_pb2.UploadCourseMaterialResponse(error=f"{result}",code="400")
        else:
            return Lms_pb2.UploadCourseMaterialResponse(size=str(sys.getsizeof(data)),code="200")


    @any_access_token_required
    def getCourseContents(self, request, context):
        course = request.course
        term = "20241"
        list_materials,error= get_course_contents(course, term)
        if error:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            return Lms_pb2.GetCourseContentsResponse(course=course,term=term,error=error)
        else:
            return Lms_pb2.GetCourseContentsResponse(course=course,term=term,data=",".join(list_materials))

    @any_access_token_required
    def getCourseMaterial(self, request, context):
        course = request.course
        name = request.name
        term = "20241"
        data, filename, error = get_required_material(course, term, name)
        if error:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            return Lms_pb2.GetCourseMaterialResponse(name=name, filename=filename, error=error)
        else:
            for res in generate_data(name, filename, data):
                yield res




