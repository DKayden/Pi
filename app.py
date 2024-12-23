from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from modbus_client import ModbusClient
from config import HOST_MODBUS_TCP, PORT_MODBUS_TCP, TYPE_MODBUS, LOCATION, DESTINATION, LINE_ACTION
from pi import control_conveyor, get_information_machine, check_status_machine

client_modbus = ModbusClient(HOST_MODBUS_TCP, PORT_MODBUS_TCP, TYPE_MODBUS)

app = FastAPI(
    title="PI API",
    openapi_url="/openapi.json",
    docs_url="/docs",
    description="PI Swagger"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

class StringModel(BaseModel):
    position: str

@app.post("/conveyor")
async def conveyor_control(content: StringModel):
    response = control_conveyor(content.position)
    return{"message": response}

@app.get("/information")
async def get_information(position: str):
    return get_information_machine(position)[0]

@app.get("/mission")
async def get_mission():
    return check_status_machine()