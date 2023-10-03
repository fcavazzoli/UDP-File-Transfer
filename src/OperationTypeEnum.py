from enum import Enum


class OperationTypeEnum(Enum):
    UPLOAD_FILE = 'upload'
    DOWNLOAD_FILE = 'download'
    CANCEL = 'cancel'
