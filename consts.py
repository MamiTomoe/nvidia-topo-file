from enum import Enum

MAX_MODEL_GROUP = 6


class LoggerFormats:
    PRINT_LOGGER_FORMAT = "%(asctime)s\n%(message)"
    LOGGER_FORMATER = '%(asctime)s - %(levelname)s\n%(message)s'
class Patterns:
    DEVICE_REGEX = '(Switch|Ca)\s+(\d+)\s+"([^"]+)"'
    CONNECTION_REGEX = r'\[(?P<group1>\d+)\]\s*(\([0-9a-zA-Z]+\))?\s*"(?P<group2>[^"]+)"\[(?P<group3>\d+)\](\([0-9a-zA-Z]+\))?'
    VENDID_REGEX = r'vendid=0x[0-9A-Za-z]+'
    DEVID_REGEX = r'devid=0x[0-9A-Za-z]+'
    SYSTEMIMGGUID_REGEX = r"sysimgguid=0x[0-9A-Za-z]+"
    DEVICEGUID_REGEX = r'(switch|ca)guid=0x[0-9A-Za-z]+(\([0-9a-zA-Z]+\))?'



class DeviceTypes(str, Enum):
    SWITCH = "Switch"
    CA = "Ca" # We are referencing to Host Connection (HCA) and not Transfer Connection (TCA)



class OutputFiles:
    OUTPUT_DIRECTORY = "/output"
    FILE_NAME = "models_{current_date}.json"


DEVICES_LETTER_TYPES = {
    'S': "Switch",
    'H': "Host"
}

