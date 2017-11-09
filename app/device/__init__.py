
from .device import Device
from .manager import DeviceManager

# the manager instance
manager = None


async def start():
    global manager

    # create and initialize the device manager
    manager = DeviceManager()
    await manager.start()


async def shutdown():
    global manager

    # stop the manager
    if manager is not None:
        await manager.shutdown()
