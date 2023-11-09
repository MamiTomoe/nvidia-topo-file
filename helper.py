from typing import Tuple, Any, Union, List
from consts import DeviceTypes, DEVICES_LETTER_TYPES, OutputFiles
from models import Connection
from pathlib import Path
import re


def get_output_dict() -> Any:
    full_path = Path().resolve()
    new_path = full_path.parent / (full_path.name + OutputFiles.OUTPUT_DIRECTORY)
    new_path.mkdir(parents=True, exist_ok=True)
    return new_path


def parse_switch_connection(result: Tuple[Any]) -> tuple[int, Any, Union[str, Any], int, Any]:
    source_port, _, device_id, dest_port, port_guid = result
    device_type, node_guid = parse_device_connection(device_id)
    return int(source_port), device_type, node_guid, int(dest_port), port_guid.strip('()')


def parse_device_connection(device_id: str) -> Tuple[Any, str]:
    device_type, node_guid = device_id.split("-")
    node_guid = node_guid.lstrip('0')
    return device_type, f"0x{node_guid}"


def parse_host_connection(result: Tuple[Any]) -> tuple[int, Any, Union[str, Any], int, Any]:
    source_port, port_guid, device_id, dest_port, _ = result
    device_type, node_guid = parse_device_connection(device_id)
    return int(source_port), device_type, node_guid, int(dest_port), port_guid.strip('()')


DEVICE_TO_PARSE = {
    DeviceTypes.SWITCH: parse_switch_connection,
    DeviceTypes.CA: parse_host_connection
}


def find_general_pattern(pattern: str, block: str) -> Union[str, None]:
    result = re.search(pattern, block)
    return result.group().split("=")[-1] if result else ""


def find_device_info(pattern: str, block: str) -> tuple[Union[str, Any], int, str, Any]:
    device_type, num_of_ports, device_guid, device_letter = "", 0, "", ""
    result = re.search(pattern, block)
    if result:
        device_type, num_of_ports, device_guid = result.groups()
        device_letter, device_guid = device_guid.split('-')

    return device_type, int(num_of_ports), f"0x{device_guid.lstrip('0')}", device_letter


def try_parse_current_connection(result: str, device_type: str, deviceguid: str):
    connection = None
    if device_type in DEVICE_TO_PARSE:
        source_port, device_type, node_guid, dest_port, port_guid = DEVICE_TO_PARSE[device_type](result)
        # If we can't find the port guid we will use the device guid some of the ports don't come at ()
        # Split will give only what we want
        port_guid = port_guid or deviceguid.split('(')[0].strip('0x')
        connection = Connection(source_port=source_port,
                                node_guid=node_guid,
                                dest_port=dest_port,
                                device_type=DEVICES_LETTER_TYPES.get(device_type, ''),
                                port_guid=port_guid)
    return connection


def find_all_patterns(pattern: str, block: str) -> List[Any]:
    return re.findall(pattern, block)


def get_device_guid_type(device_type: str) -> str:
    return "switchguid" if device_type == DeviceTypes.SWITCH else "caguid"
