from modbus_client import ModbusClient
from config import HOST_MODBUS_TCP, PORT_MODBUS_TCP, TYPE_MODBUS, INFORMATION_UPPER, INFORMATION_LOWER, LOWER_CONVEYOR, UPPER_CONVEYOR

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



