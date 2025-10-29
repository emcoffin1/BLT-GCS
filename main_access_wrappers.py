from datetime import time
import csv
import os
from PyQt6.QtCore import QObject, QTimer, pyqtSignal
from collections import OrderedDict
from labjack import ljm
from util_func import *
import json
from random import randint
import numpy as np
import pandas as pd

class LabJack(QObject):
    updateValues = pyqtSignal()
    updateLog = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.config = None
        self.sensors = []
        self.sensor_lookup = {}

        self.data_log = pd.DataFrame()
        self.err_log = {}
        self._iter = 0
        self._filename = None
        self.record = False
        # self.init_data_log()

        self.get_config()

        self.timer = Timer()
        self.timer.start_timer(config=self.config)


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

    def _write(self):
        # Temporary no functionality
        # Currently no output control
        pass

    def _read_port(self, channel):
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

    def emit_values(self,timestamp):
        """
        Retrieves data and adds to sensor objects
        :return:
        """
        new_row = {"timestamp": timestamp}

        for i in self.sensors:
            if self.read:
                # Get value
                x = self._read_port(channel=i.port)

                # Filter
                if x is None or np.isinf(x) or np.isnan(x):
                    x = 0
            else:
                x = self._fake_values(range=i.max)

            # Add value to object
            i.add_data(x)
            new_row[i.name] = i.get_value()

        self.data_log.loc[len(self.data_log)] = [
            new_row.get(col, None) for col in self.data_log.columns
        ]

        self.save_to_logs()
        self.updateValues.emit()

        # Double clear the data just in case
        self.data_log = self.data_log.iloc[0:0]

    def reconnect_labjack(self):
        """
        Cycles the connection to the labjack
        """
        self.close_labjack()
        self.connect_labjack()

    def _fake_values(self, range: int):
        try:
            x = randint(0, range)
            return x
        except Exception as e:
            return -1

    def get_config(self):
        """Initializes config file"""

        # == OPEN CONFIG FILE == #

        with open('config.json', 'r') as config_file:
            self.config = json.load(config_file)

        # == END == #

        # == SET FULL LIST OF SENSORS == #

        # Create a list of all sensors within the config file
        self.config = update_table_lists(self.config)

        # Save that list in config
        with open("config.json", 'w') as f:
            json.dump(self.config, f, indent=2)

        # == END == #

        # == CREATE SENSOR LISTS AND ITEMS == #

        sensors = self.config["inputChannels"]
        for i, j in sensors.items():
            self.sensors.append(Sensor(name=i, port=j["PORT"], cal=j["CALIBRATION"], size=j["SAMPLE"], max=j["MAX VALUE"]))

        self.sensor_lookup = {s.name: s for s in self.sensors}

        # == END == #

        # == CREATE VALUE LOG == #

        self.data_log["timestamp"] = []
        for k in self.sensors:
            self.data_log[k.name] = []
        # self.init_data_log()

    def save_to_logs(self):
        # == DONT MOVE ON CONDITIONS == #

        # If not set to record
        if not self.record:
            return

        # Make sure line isn't empty
        if self.data_log.empty:
            return


        # == END == #

        # == BEGIN LOGGING == #

        self.data_log.to_csv(self._filename, mode='a', header=False, index=False)

        # == END == #

        # == CLEAR DATA == #

        self.data_log = self.data_log.iloc[0:0]

        # == END == #

        self._iter = 0
        self.updateLog.emit()

    def init_data_log(self):
        """ Initializes the data logger as a CSV """

        # == INIT FILE NAME == #

        base_name = "dataLog"
        ext = ".csv"
        filename = base_name + ext

        # Check if the file name already exists
        # If it does add a value
        # Iterate until it doesn't exist
        counter = 1
        while os.path.exists(filename):
            filename = f"{base_name}{counter}{ext}"
            counter += 1

        self._filename = filename
        print(f"Recording to: {self._filename}")

        # == END == #

        # == CREATE FILE AND COLUMNS == #
        sensor_names = [s.name for s in self.sensors]
        columns = ["timestamp"] + sensor_names

        self.data_log = pd.DataFrame(columns=columns)
        self.data_log.to_csv(self._filename, index=False)

        # == END == #

        # Ensure we're at 0
        self._iter = 0

    def start_recording(self):
        # == TRIGGER DATA SAVING == #
        if self.record:
            # Already recording
            self.record = False
        else:
            self.record = True
            self.init_data_log()



class Sensor:
    def __init__(self, name, port, cal, size, max):
        self.name = name
        self.port = port
        self.cal = list(cal)
        self.size = int(size)
        self.max = int(max)

        self.values: list = []
        self.y_history = []
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
        self.y_history.append(y_sum)
        if len(self.y_history) > 30:
            self.y_history.pop(0)

    def get_value(self):
        return round(self.y, 2)





def update_table_lists(config):
    full_list = list(config["inputChannels"].keys())

    # Build a new ordered dictionary with FULL LIST first
    ordered = OrderedDict()
    ordered["FULL LIST"] = full_list

    # Add the rest (skipping any existing FULL LIST)
    for key, value in config["tableLists"].items():
        if key != "FULL LIST":
            ordered[key] = value

    config["tableLists"] = ordered
    return config

