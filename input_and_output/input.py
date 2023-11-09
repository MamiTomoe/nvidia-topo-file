from typing import List

from consts import LoggerFormats
from models import Model
from helper import get_output_dict
import os
from pydantic import parse_obj_as
import json
import itertools
import logging


logging.basicConfig(level=logging.INFO,
                    format=LoggerFormats.LOGGER_FORMATER)
logger = logging.getLogger(__name__)


def get_block(file_path: str) -> List[str]:
    # In order that I will parse at the best way
    # I decided to split them into blocks    like in the file
    # Every block has its own info and yield it as block
    # The block end when we have only new block

    logger.info(f"Starting to parse: {file_path}")
    with open(file_path, "r") as f:
        current_block = ""
        for line in itertools.islice(f, 4, None):  # Skipping comments lines
            if line == '\n' and current_block != "":
                yield current_block
                current_block = ""
            else:
                current_block += line

    logger.info(f"Finished to parse: {file_path}")


def read_parsed_files():
    path = get_output_dict()
    for entry in os.scandir(path):
        with open(entry.path, "r") as f:
            # Locally TA made me some problems because of the pydantic
            # In order to work I used parse obj as
            yield parse_obj_as(List[Model], json.loads(f.read()))