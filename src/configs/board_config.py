"""
Combination board configuration for desktop, pyscript and jupyter notebook platforms.
"""

width = 320
height = 480
rotation = 0
scale = 2.0

_ps = _jn = False
try:
    import pyscript  # type: ignore # noqa: F401
    _ps = True
except ImportError:
    try:
        get_ipython()  # type: ignore # noqa: F821
        _jn = True
    except NameError:
        pass

if _ps:
    from psdisplay import PSDisplay, PSDevices
    from pydevices.devices import Devices, Broker # type: ignore


    display_drv = PSDisplay("display_canvas", width, height)

    broker = Broker()

    touch_drv = PSDevices("display_canvas")

    touch_dev = broker.create_device(
        type=Devices.TOUCH,
        read=touch_drv.get_mouse_pos,
        data=display_drv,
    )
elif _jn:
    from jndisplay import JNDisplay
    from pydevices.devices import Devices, Broker # type: ignore
    from pydevices.timer import get_timer

    broker = Broker()
    
    display_drv = JNDisplay(width, height)
    tim = get_timer(display_drv.show)
else:
    from dtdisplay import DTDisplay, poll # type: ignore
    from pydevices.devices import Devices, Broker # type: ignore
    from pydevices.timer import get_timer
    import sys

    display_drv = DTDisplay(
        width=width,
        height=height,
        rotation=rotation,
        color_depth=16,
        title=f"{sys.implementation.name} on {sys.platform}",
        scale=scale,
    )

    broker = Broker()

    events_dev = broker.create_device(
        type=Devices.QUEUE,
        read=poll,
        data=display_drv,
        # data2=Events.filter,
    )
    tim = get_timer(display_drv.show)

display_drv.fill(0xACED)  # Something other than white or black to show display is working
