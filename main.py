import keyboard as kb
from stateMachine import *
from time import sleep
import serial
import time


arduino = serial.Serial(port='COM2', baudrate=9600, timeout=.1)
def write_cmd(string):
    arduino.write(bytes(string+"\n", 'utf-8'))
def read_cmd():
    data = arduino.readline()
    return data


################################################################################
# State Actions
def ready():
    print("This is the ready loop")
def started():
    print("This is the started loop")
def red():
    print("Lowering flag")
    write_cmd("#LOWER")
def green():
    print("Raising flag")
    write_cmd("#RAISE")
def get_encoder():
    while arduino.in_waiting:
        buffer = read_cmd()
        if buffer.startswith(b"#PULSE_CNT:"):
            pulse_count = int(buffer[11:])
            print("Pulse Count: "+ str(pulse_count))
# def raise_flag():
# def lower_flag():

################################################################################
# State = State("Name",loopFunction,enterFunction,leaveFunction)
Ready = State("Ready",None,ready,None)
Started = State("Started",get_encoder,started,None)
Red = State("Red",get_encoder,red,None)
Green = State("Green",get_encoder,green,None)

statesList = [
    Ready,
    Started,
    Red,
    Green,
]
################################################################################
# Trigger Functions
def trig_start_key():
    if kb.is_pressed('s'):
        sleep(0.25)
        return True
def trig_red():
    if kb.is_pressed('r'):
        sleep(0.25)
        return True
def trig_green():
    if kb.is_pressed('g'):
        sleep(0.25)
        return True
def trig_err():
    if kb.is_pressed('e'):
        sleep(0.25)
        return True
    
################################################################################
# NAME = Transition(
#     triggerFunction
#     [SourceStates]
#     [TargetStates]
# )
START_KEY = Transition(
    "Start Key Pressed",
    trig_start_key,
    [Ready],
    [Started])
IM_IS_RED = Transition(
    "Red Detected",
    trig_red,
    [Started,Green],
    [Red,Red])
IM_IS_GREEN = Transition(
    "Green Detected",
    trig_green,
    [Started,Red],
    [Green,Green])
IM_ERR = Transition(
    "Error Detected",
    trig_err,
    [Started,Red,Green],
    [Ready,Ready,Ready])

transitionsList = [
    START_KEY,
    IM_IS_RED,
    IM_IS_GREEN,
    IM_ERR,
]

sm = StateMachine(statesList,transitionsList,"Ready")
pulse_count = 0

while True:
    sm.checkTransitions()
    sm.run()
