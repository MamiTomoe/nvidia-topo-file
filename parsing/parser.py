import logging
from input_and_output.input import get_block
from typing import Any, List, Optional
from helper import try_parse_current_connection, find_general_pattern, find_device_info, find_all_patterns
from models import Connection, Model, Device
from consts import MAX_MODEL_GROUP, Patterns


class Parser:
    def __init__(self, file_name: str, logger: logging.Logger, max_model_group: int = MAX_MODEL_GROUP):
        self.logger = logger
        self.file_name = file_name

        # In order to do efficiency and won't wait to model to stop being processed
        # We are splitting the models into groups to be written in one file
        # So we can load it into memory anc still keep file short
        self.max_model_group = max_model_group

    def get_models(self) -> Optional[List[Model]]:
        models = []
        counter = 0
        for block in get_block(self.file_name):
            model = self.parse_blocks(block)
            models.append(model)
            if counter == self.max_model_group:
                yield models
                models = []
                counter = 0
            else:
                counter += 1

    def parse_blocks(self, block: str) -> Model:
        model = self.parse_general_info(block)
        device = self.parse_device_info(block)
        connections = self.get_connections(block, device.device_type, model.deviceguid)
        model.device = device
        model.connections = connections
        return model

    def parse_general_info(self, block: str) -> Model:
        self.logger.debug("Parsing general information on device")
        vendid = find_general_pattern(Patterns.VENDID_REGEX, block)
        devid = find_general_pattern(Patterns.DEVID_REGEX, block)
        sysimgguid = find_general_pattern(Patterns.SYSTEMIMGGUID_REGEX, block)
        deviceguid = find_general_pattern(Patterns.DEVICEGUID_REGEX, block)

        return Model(vendid=vendid,
                     devid=devid,
                     sysimmguid=sysimgguid,
                     deviceguid=deviceguid,
                     device=None,
                     connections=[])

    def parse_device_info(self, block: str) -> Device:
        self.logger.debug("Parsing the current device info")
        device_type, num_of_ports, device_guid, device_letter = find_device_info(Patterns.DEVICE_REGEX, block)
        return Device(device_type=device_type,
                      num_of_ports=int(num_of_ports),
                      device_guid=device_guid,
                      device_letter=device_letter)

    def get_connections(self, block: str, device_type: str, deviceguid: str) -> Optional[List[Connection]]:
        self.logger.debug("Parsing the device connections.")
        found_connections = find_all_patterns(Patterns.CONNECTION_REGEX, block)
        connections = self.__try_parse_connections(found_connections, device_type, deviceguid)
        return connections

    def __try_parse_connections(self, found_connections: List[Any],
                                device_type: str,
                                deviceguid: str) -> Optional[List[Connection]]:
        connections = []
        for current_connection in found_connections:
            try:
                connection = try_parse_current_connection(current_connection, device_type, deviceguid)
                if connection:
                    connections.append(connection)
            except Exception as e:
                self.logger.warning(f"Could not parse the current connection because of: {e}")

        return connections
