#!/home/robot/roboliga/bin/python
from ev3dev2.sensor.lego import ColorSensor

from ev3dev2.button import Button
from ev3dev2.sensor import INPUT_1
from time import sleep

SENSOR_COLOR_PORT = INPUT_1


def init_sensor_color(port: str) -> ColorSensor:
    """
    Preveri, ali je tipalo za barvo priklopljeno na katerikoli vhod. 
    Vrne objekt za tipalo.
    """
    sensor = ColorSensor(port)
    while not sensor.address:
        print('\nPriklopi tipalo na izhod ' + port +
              ' in pritisni ter spusti gumb DOL.')
        wait_for_button('down')
        sensor = ColorSensor(port)
    return sensor

def wait_for_button(btn_name: str = 'down'):
    """
    Čakaj v zanki dokler ni gumb z imenom `btn_name` pritisnjen in nato sproščen.
    """
    while not getattr(btn, btn_name):
        pass
    flag = False
    while getattr(btn, btn_name):
        if not flag:
            flag = True


print('Priprava tipal ... ', end='', flush=True)
btn = Button()
sensor_color = init_sensor_color(SENSOR_COLOR_PORT)
print('OK!')

sensor_color.mode = sensor_color.MODE_COL_COLOR

while True:
    print(sensor_color.color_name)

    sleep(0.1)