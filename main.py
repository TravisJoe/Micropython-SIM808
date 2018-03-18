

from pyb import UART
from pyb import Pin

import utime

sim_com = UART(1, 115200)
sim_com.init(115200, bits=8, parity=None, stop=1, timeout=100)

key_pin = Pin('C5', Pin.OUT)


def setup_module():
    if sync_serial():
        key_on(the_pin=key_pin)
        set_echo(echo=False)
    else:
        print('Failed to sync')


def sync_serial(serial, attempts=5):
    count = 0
    synced = False
    while count<attempts:
        send_command('AT')
        if get_response(expected='OK'):
            synced = True
            break
        else:
            count += 1
            utime.sleep_ms(250)

    return synced


def key_on(the_pin):
    utime.sleep_ms(500)
    the_pin.value(False)
    utime.sleep_ms(500)
    the_pin.value(True)
    utime.sleep_ms(1500)
    the_pin.value(False)
    utime.sleep_ms(500)

def setup_gps():
    send_command('AT+CGNSPWR')
    get_response(expected='sdjdsjkhdskjhs')


def set_echo(echo=False):
    command = 'AT+ATE' + str(int(echo))
    send_command(command)


def send_command(cmd_string):
    sim_com.write(cmd_string + '\r')


def get_response(expected=False):
    response = sim_com.read()

    if response is not None:
        # Clean up response
        response = response.lstrip()
        response = response.rstrip()
        response = response.decode()

        if expected is not False:
            if response == expected:
                return (True, response)
            else:
                return (False, response)
        else:
            return (False, response)

    else:
        return (False, None)
