"""" Waveshare Round Display for XIAO GC9A01 240x240 display on ESP32-S3-Touch-LCD-1.28"""

from spibus import SPIBus
from gc9a01 import GC9A01
from machine import Pin, I2C
from cst8xx import CST8XX
from eventsys import devices

display_bus = SPIBus(
    dc=8,
    cs=9,
    mosi=11,
    miso=12,
    sck=10,
    id=1,
    baudrate=80_000_000
)

display_drv = GC9A01(
    display_bus,
    width=240,
    height=240,
    colstart=0,
    rowstart=0,
    rotation=0,
    mirrored=False,
    color_depth=16,
    bgr=True,
    reverse_bytes_in_word=True,
    invert=True,
    brightness=1.0,
    backlight_pin=2,
    backlight_on_high=True,
    reset_pin=14,
    reset_high=False,
    power_pin=None,
    power_on_high=True,
)

i2c = I2C(0, sda=Pin(6), scl=Pin(7), freq=400_000)
touch_drv = CST8XX(i2c, irq_pin=5, rst_pin=13)
touch_read_func = touch_drv.get_positions
touch_rotation_table = (0, 5, 6, 3)

broker = devices.Broker()

touch_dev = broker.create_device(
    type=Devices.TOUCH,
    read=touch_read_func,
    data=display_drv,
    data2=touch_rotation_table,
)