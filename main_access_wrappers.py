from PyQt6.QtCore import QObject, QTimer, pyqtSignal
from labjack import ljm
from util_func import *
import json
from random import randint
import numpy as np

class LabJack(QObject):
    updateValues = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.config = None
        self.sensors = []
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

    def read_port(self, channel):
        """
        Reads given analog channel
        :param channel: Channel number
        :return:
        """
        try:
            value = ljm.eReadName(self.handle, channel)
            return value

        except Exception as e:
            log_error(e)
            return None

    def emit_values(self):
        """
        Retrieves data and adds to sensor objects
        :return:
        """
        for i in self.sensors:
            if self.read:
                # Get value
                x = self.read_port(channel=i.port)

                # Filter
                if x is None or np.inf or np.isnan(x):
                    x = 0
            else:
                x = self.fake_values(range=i.max)

            # Add value to object
            i.add_data(x)

        self.updateValues.emit()

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
        for i, j in sensors.items():
            self.sensors.append(Sensor(name=i, port=j["PORT"], cal=j["CALIBRATION"], size=j["SAMPLE"], max=j["MAX VALUE"]))


class Sensor:
    def __init__(self, name, port, cal, size, max):
        self.name = name
        self.port = port
        self.cal = list(cal)
        self.size = int(size)
        self.max = int(max)

        self.values: list = []
        self.y: float = 0

    def calibration(self, x):
        y = self.cal[0]*x**2 + self.cal[1]*x + self.cal[2]
        return y

    def add_data(self, x):
        y_cal = self.calibration(x)
        self.values.append(y_cal)
        if len(self.values) > self.size:
            self.values.pop(0)

        y_sum = sum(self.values)/len(self.values)
        self.y = y_sum

    def get_value(self):
        return self.y



