from enum import Enum


class TaskType(Enum):
    SHELL = 'shell'
    INFO = 'info'
    PACKAGE = "package"
    SERVICE = "service"
    INT_CONTROL = "integrity_control"
    REMOTE_DIR = "remote_directory"
    FIREWALL = "port_manager"
    FILE_TRANSFER = "file_transfer"
    VNC = "vnc_service"
    OPERATIONS = "operations"
    NOTIFICATION = "notification"
    DEVICE = "device"
    BACKUP = "backup"
    LDAP = "ldap"

    @classmethod
    def choices(cls):
        return tuple((i.value, i.value) for i in cls)
