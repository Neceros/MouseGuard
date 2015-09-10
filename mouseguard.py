"""
When run, waits [5] seconds for user to let go of mouse, then locks computer if mouse
pointer is moved afterwards.
Author: Billy Barnes <neceros@gmail.com>
"""

from ctypes import windll, Structure, c_ulong, byref
import ctypes
from time import sleep
from datetime import datetime
import logging
import sys

__author__ = '@neceros'
__version__ = '0.0.1'

PAUSE_DUR = 5

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

fh = logging.FileHandler('mouseguard.log')
fh.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
fh.setFormatter(formatter)
log.addHandler(ch)
log.addHandler(fh)


class POINT(Structure):
        _fields_ = [("x", c_ulong), ("y", c_ulong)]

def queryMousePosition():
    pt = POINT()
    windll.user32.GetCursorPos(byref(pt))
    return {"x": pt.x, "y": pt.y}

def protect_mouse():
    log.info('MouseGuard protection beginning at {}'.format(datetime.now()))
    while True:
        pos1 = queryMousePosition()
        sleep(1)
        pos2 = queryMousePosition()
        if pos1 != pos2:
            log.info('The mouse was moved at {} and was locked. End run.'
                     .format(datetime.now()))
            ctypes.windll.user32.LockWorkStation()
            sys.exit(0)


if __name__ == "__main__":
    log.info('MouseGuard initiated. Waiting {} seconds until capturing mouse activity...'
             .format(PAUSE_DUR))
    sleep(PAUSE_DUR)
    protect_mouse()
