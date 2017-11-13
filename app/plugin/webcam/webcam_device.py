
import os

import app.device


class WebcamDevice(app.device.Device):

    def __init__(self):
        this_path = os.path.dirname(__file__)
        json_file = os.path.join(this_path, "webcam_device.json")
        super(WebcamDevice, self).__init__(json_file=json_file)
