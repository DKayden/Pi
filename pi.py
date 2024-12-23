from modbus_client import ModbusClient
from config import (HOST_MODBUS_TCP, PORT_MODBUS_TCP, TYPE_MODBUS, INFORMATION_UPPER,
                    INFORMATION_LOWER, LOWER_CONVEYOR, UPPER_CONVEYOR, PI_DESTINATION_HOST, PI_DESTINATION_PORT,
                    LINE_ACTION, LOCATION, DESTINATION, POSITION_CHECK)
import requests

client_modbus = ModbusClient(host=HOST_MODBUS_TCP, port=PORT_MODBUS_TCP, type=TYPE_MODBUS)

def control_conveyor(string) -> str:
    try:
        string = string.lower()
        if string =="l":
            client_modbus.write_register(LOWER_CONVEYOR, 1)
            return("Lower conveyor đang quay")
        elif string == "u":
            client_modbus.write_register(UPPER_CONVEYOR, 1)
            return("Upper conveyor đang quay")
        else:
            return("Lệnh quay conveyor không hợp lệ")
    except Exception as e:
        return(f"Lỗi khi thực hiện điều khiển conveyor: {e}")
    
def get_information_machine(string):
    if string.lower() == "upper":
        return client_modbus.read_holding_registers(INFORMATION_UPPER, 1)
    elif string.lower() == "lower":
        return client_modbus.read_holding_registers(INFORMATION_LOWER, 1)
    else:
        return {"message": "Vị trí không hợp lệ"}

def check_status_machine():
    try:
        status_destination = requests.get(f"http://{PI_DESTINATION_HOST}:{PI_DESTINATION_PORT}/information?position={POSITION_CHECK}")
        status_machine = get_information_machine(POSITION_CHECK)
        if status_machine == "1" and status_destination == "0":
            return {"type" : LINE_ACTION, "location" : LOCATION, "destination" : DESTINATION}
        else:
            return None
    except Exception as e:
        return(f"Lỗi khi kiểm tra trạng thái: {e}")
