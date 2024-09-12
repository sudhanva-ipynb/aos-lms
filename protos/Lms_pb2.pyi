from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class LoginRequest(_message.Message):
    __slots__ = ("username", "password")
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    username: str
    password: str
    def __init__(self, username: _Optional[str] = ..., password: _Optional[str] = ...) -> None: ...

class LoginResponse(_message.Message):
    __slots__ = ("error", "token", "courses", "code")
    ERROR_FIELD_NUMBER: _ClassVar[int]
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    COURSES_FIELD_NUMBER: _ClassVar[int]
    CODE_FIELD_NUMBER: _ClassVar[int]
    error: str
    token: str
    courses: str
    code: str
    def __init__(self, error: _Optional[str] = ..., token: _Optional[str] = ..., courses: _Optional[str] = ..., code: _Optional[str] = ...) -> None: ...

class UploadCourseMaterialRequest(_message.Message):
    __slots__ = ("course", "name", "term", "filename", "data", "created")
    COURSE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    TERM_FIELD_NUMBER: _ClassVar[int]
    FILENAME_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    CREATED_FIELD_NUMBER: _ClassVar[int]
    course: str
    name: str
    term: str
    filename: str
    data: bytes
    created: str
    def __init__(self, course: _Optional[str] = ..., name: _Optional[str] = ..., term: _Optional[str] = ..., filename: _Optional[str] = ..., data: _Optional[bytes] = ..., created: _Optional[str] = ...) -> None: ...

class GetCourseContentsRequest(_message.Message):
    __slots__ = ("course", "term")
    COURSE_FIELD_NUMBER: _ClassVar[int]
    TERM_FIELD_NUMBER: _ClassVar[int]
    course: str
    term: str
    def __init__(self, course: _Optional[str] = ..., term: _Optional[str] = ...) -> None: ...

class GetCourseContentsResponse(_message.Message):
    __slots__ = ("course", "term", "data", "error")
    COURSE_FIELD_NUMBER: _ClassVar[int]
    TERM_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    course: str
    term: str
    data: str
    error: str
    def __init__(self, course: _Optional[str] = ..., term: _Optional[str] = ..., data: _Optional[str] = ..., error: _Optional[str] = ...) -> None: ...

class UploadCourseMaterialResponse(_message.Message):
    __slots__ = ("error", "size", "code")
    ERROR_FIELD_NUMBER: _ClassVar[int]
    SIZE_FIELD_NUMBER: _ClassVar[int]
    CODE_FIELD_NUMBER: _ClassVar[int]
    error: str
    size: str
    code: str
    def __init__(self, error: _Optional[str] = ..., size: _Optional[str] = ..., code: _Optional[str] = ...) -> None: ...

class GetCourseMaterialRequest(_message.Message):
    __slots__ = ("course", "name", "term")
    COURSE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    TERM_FIELD_NUMBER: _ClassVar[int]
    course: str
    name: str
    term: str
    def __init__(self, course: _Optional[str] = ..., name: _Optional[str] = ..., term: _Optional[str] = ...) -> None: ...

class GetCourseMaterialResponse(_message.Message):
    __slots__ = ("name", "filename", "data", "error")
    NAME_FIELD_NUMBER: _ClassVar[int]
    FILENAME_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    name: str
    filename: str
    data: str
    error: str
    def __init__(self, name: _Optional[str] = ..., filename: _Optional[str] = ..., data: _Optional[str] = ..., error: _Optional[str] = ...) -> None: ...
