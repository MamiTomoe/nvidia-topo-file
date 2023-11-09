from typing import List, Optional
from pydantic import BaseModel


# In order to parse it well and easier I decided to use pydantic to show off the models
# Pydantic have easier way to convert into dict and json alike .
# It also have validation
class Connection(BaseModel):
    source_port: int
    node_guid: str
    dest_port: int
    device_type: str
    port_guid: Optional[str]


class Device(BaseModel):
    device_type: str
    num_of_ports: int
    device_guid: str
    device_letter: str

class Model(BaseModel):
    vendid: str
    devid: str
    sysimmguid: str
    deviceguid: str
    device: Optional[Device]
    connections: Optional[List[Connection]]
