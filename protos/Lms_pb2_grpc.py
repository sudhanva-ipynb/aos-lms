# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

from protos import Lms_pb2 as protos_dot_Lms__pb2

GRPC_GENERATED_VERSION = '1.66.1'
GRPC_VERSION = grpc.__version__
_version_not_supported = False

try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True

if _version_not_supported:
    raise RuntimeError(
        f'The grpc package installed is at version {GRPC_VERSION},'
        + f' but the generated code in protos/Lms_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
    )


class AuthStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.studentLogin = channel.unary_unary(
                '/Auth/studentLogin',
                request_serializer=protos_dot_Lms__pb2.LoginRequest.SerializeToString,
                response_deserializer=protos_dot_Lms__pb2.LoginResponse.FromString,
                _registered_method=True)
        self.facultyLogin = channel.unary_unary(
                '/Auth/facultyLogin',
                request_serializer=protos_dot_Lms__pb2.LoginRequest.SerializeToString,
                response_deserializer=protos_dot_Lms__pb2.LoginResponse.FromString,
                _registered_method=True)


class AuthServicer(object):
    """Missing associated documentation comment in .proto file."""

    def studentLogin(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def facultyLogin(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_AuthServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'studentLogin': grpc.unary_unary_rpc_method_handler(
                    servicer.studentLogin,
                    request_deserializer=protos_dot_Lms__pb2.LoginRequest.FromString,
                    response_serializer=protos_dot_Lms__pb2.LoginResponse.SerializeToString,
            ),
            'facultyLogin': grpc.unary_unary_rpc_method_handler(
                    servicer.facultyLogin,
                    request_deserializer=protos_dot_Lms__pb2.LoginRequest.FromString,
                    response_serializer=protos_dot_Lms__pb2.LoginResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'Auth', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('Auth', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class Auth(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def studentLogin(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/Auth/studentLogin',
            protos_dot_Lms__pb2.LoginRequest.SerializeToString,
            protos_dot_Lms__pb2.LoginResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def facultyLogin(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/Auth/facultyLogin',
            protos_dot_Lms__pb2.LoginRequest.SerializeToString,
            protos_dot_Lms__pb2.LoginResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)


class MaterialsStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.courseMaterialUpload = channel.stream_unary(
                '/Materials/courseMaterialUpload',
                request_serializer=protos_dot_Lms__pb2.UploadCourseMaterialRequest.SerializeToString,
                response_deserializer=protos_dot_Lms__pb2.UploadCourseMaterialResponse.FromString,
                _registered_method=True)


class MaterialsServicer(object):
    """Missing associated documentation comment in .proto file."""

    def courseMaterialUpload(self, request_iterator, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_MaterialsServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'courseMaterialUpload': grpc.stream_unary_rpc_method_handler(
                    servicer.courseMaterialUpload,
                    request_deserializer=protos_dot_Lms__pb2.UploadCourseMaterialRequest.FromString,
                    response_serializer=protos_dot_Lms__pb2.UploadCourseMaterialResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'Materials', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('Materials', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class Materials(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def courseMaterialUpload(request_iterator,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.stream_unary(
            request_iterator,
            target,
            '/Materials/courseMaterialUpload',
            protos_dot_Lms__pb2.UploadCourseMaterialRequest.SerializeToString,
            protos_dot_Lms__pb2.UploadCourseMaterialResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
