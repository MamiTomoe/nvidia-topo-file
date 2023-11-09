import logging

from consts import OutputFiles, LoggerFormats
from models import Model
from typing import List, Dict, Any
from helper import get_output_dict, get_device_guid_type
import time
import json

logging.basicConfig(level=logging.INFO,
                    format=LoggerFormats.PRINT_LOGGER_FORMAT)

logger = logging.getLogger(__name__)


# We don't want to create every time new class to read or write thats why it's functions


def create_models_files(models: List[Model]):
    directory_path = get_output_dict()
    serialized_models = serialize_model_to_json(models)
    new_path = get_new_file_name(directory_path)

    with open(new_path, "w") as f:
        json.dump(serialized_models, indent=2, fp=f)


def serialize_model_to_json(models: List[Model]) -> List[Dict[str, Any]]:
    serialized_models = [model.model_dump(mode="json") for model in models]
    return serialized_models


def get_new_file_name(directory_path: Any) -> str:
    new_file_name = OutputFiles.FILE_NAME.format(current_date=time.time())
    return rf'{directory_path}/{new_file_name}'


def print_parsed_models(models: List[Model]) -> None:
    for model in models:
        device_type_guid = get_device_guid_type(model.device.device_type)
        for connection in model.connections:
            # https://docs.oracle.com/cd/E19654-01/820-7752-12/z400014c1567844.html for reference
            logger.info(f"{connection.device_type}:\n"
                  f"sysimgguid: {connection.node_guid}\n"
                  f"Port_id: {connection.port_guid}\n"
                  f"Conncted to: {model.device.device_type}: {device_type_guid}={model.deviceguid}, port={connection.source_port}")
