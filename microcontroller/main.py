import time
import board
from digitalio import DigitalInOut, Direction
 
led = DigitalInOut(board.LED_INVERTED)
led.direction = Direction.OUTPUT
 
pump = DigitalInOut(board.D9)
pump.direction = Direction.OUTPUT
pump_pause = 6*60
pump_interval = 2
pulse_intensity = 0.002
 
atomizer = DigitalInOut(board.D8)
atomizer.direction = Direction.OUTPUT
fog_interval = 60
fog_pause = fog_interval + 60 * 3
 
signal_interval = 10
signal_length = 0.4
 
delays = dict()
workers = dict()
 
def set_interval(delay, callback, key):
    def execute():
        if delays.get(key, 0) <= time.monotonic():
            callback()
            delays[key] = time.monotonic() + delay
 
    workers[key] = execute
 
 
def set_timeout(delay, callback, key):
    delays[key] = time.monotonic() + delay
 
    def execute():
        if not key in delays.keys():
            return
        if delays[key] <= time.monotonic():
            callback()
            del delays[key]
 
    workers[key] = execute
 
 
def turn_pump_on_by_pwm(duration=pump_interval, pulse=pulse_intensity):
    led.value = False
    t_end = time.monotonic() + duration
    while time.monotonic() < t_end:
        pump.value = True
        time.sleep(pulse)
        pump.value = False
        time.sleep(pulse)
    led.value = True
 
 
def turn_atomizer_off():
    atomizer.value = False
 
 
def turn_atomizer_on(duration=fog_interval):
    atomizer.value = True
    set_timeout(duration, turn_atomizer_off, 'FOG_OFF')
 
def send_signal_to_powerbank():
    if not atomizer.value:
        turn_atomizer_on(signal_length)
 
set_interval(pump_pause, turn_pump_on_by_pwm, 'PUMP_ON')
set_interval(fog_pause, turn_atomizer_on, 'FOG_ON')
set_interval(signal_interval, send_signal_to_powerbank, 'SIGNAL')
turn_pump_on_by_pwm(10)
 
while True:
    for execute in workers.values():
        execute()