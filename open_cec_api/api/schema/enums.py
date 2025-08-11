from enum import Enum


class StatusEnum(str, Enum):
    active = "active"
    suspended = "suspended"
    expired = "expired"


class AttributeTypeEnum(str, Enum):
    string = "string"
    number = "number"
    boolean = "boolean"
    enum = "enum"
