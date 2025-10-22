from PyQt6.QtCore import QObject, QTimer, pyqtSignal
from labjack import ljm
from util_func import *
import json
from random import randint
import numpy as np

class LabJack(QObject):
    updateValues = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.config = None
        self.sensors = None
        self.get_config()

        self.timer = Timer(config=self.config)


        self.handle = None
        self.info = None
        self.connection_type = None
        self.ip_add = None
        self.port = None
        self.sens = None
        self.read = False

        self.timer.updateValues.connect(self.emit_values)


    def connect_labjack(self):
        """
        Connects to labjack
        """
        # self.handle = ljm.openS(deviceType=self.config["boardInfo"]["version"],
        #                         connectionType=self.config["boardInfo"]["connectionType"],
        #                         identifier=self.config["boardInfo"]["identifier"])
        #
        # self.info = ljm.getHandleInfo(self.handle)
        # self.connection_type = self.info[1]
        # self.ip_add = ljm.numberToIP(self.info[3])
        # self.port = self.info[4]
        # self.read = True

    def close_labjack(self):
        """
        Closes labjack connection
        """
        ljm.close(self.handle)

    def write(self):
        # Temporary no functionality
        # Currently no output control
        pass

    def read_port(self, channel, c):
        """
        Reads given analog channel
        :param channel: Channel
        :param c: Calibration equation for that sensor
        :return:
        """
        try:
            value = ljm.eReadName(self.handle, channel)
            value = calibration(c=c, x=value)
            return value

        except Exception as e:
            log_error(e)
            return None

    def emit_values(self):
        update = {}
        for i, j in self.config["inputChannels"].items():
            if self.read:
                x = self.read_port(channel=j["PORT"], c=j["CALIBRATION"])
                if x is not None or np.inf or np.isnan(x):
                    self.sensors[i].append(x)
                else:
                    self.sensors[i].append(0)
            else:
                # print(1)
                x = self.fake_values(range=int(j["MAX VALUE"]))
                self.sensors[i].append(x)
        # print(3)
        # Check for the size of each list compared to sample size
        for s,v in self.sensors.items():
            if len(v) > self.config["inputChannels"][s]["SAMPLE"]:
                v.pop(0)

            # Get average values and apply to update
            update[s] = sum(v) / len(v)

        self.updateValues.emit(update)

    def reconnect_labjack(self):
        """
        Cycles the connection to the labjack
        """
        self.close_labjack()
        self.connect_labjack()

    def fake_values(self, range: int):
        try:
            x = randint(0, range)
            return x
        except Exception as e:
            return -1

    def get_config(self):
        """Initializes config file"""
        with open('config.json', 'r') as config_file:
            self.config = json.load(config_file)

        sensors = self.config["inputChannels"]
        self.sensors = {s: [] for s in sensors}
