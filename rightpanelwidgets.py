from PyQt6.QtCore import QObject, Qt
from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel, QPushButton, QDial, QSlider, QProgressBar

from sensordisplay import SensorDisplayPanel


class MainPanel(QWidget):
    def __init__(self, labjack):
        super().__init__()
        self.labjack = labjack

        # Layout
        layout = QGridLayout()
        self.setLayout(layout)
        self.setStyleSheet("background-color: #d4d4d4;"
                           "color: black;"
                           "padding: 20px;")

        # Contents
        label = QLabel("Main")
        layout.addWidget(label)

        sensorTable = SensorDisplayPanel(labjack=self.labjack)
        layout.addWidget(sensorTable, 1, 1, 1, 1)


        # PT Readings
        # self.pt_list = {}
        # for i in self.labjack.sensors:
        #     self.pt_list[i] = QLabel("0")
        #     layout.addWidget(self.pt_list[i])

        # self.labjack.updateValues.connect(self.update_values)

    def update_values(self):
        # iterate over all sensor objects []
        for i in self.labjack.sensors:
            # if the objects name (object.name) is in pt_list
            # adjust the text to the appropriate value
            if i in self.pt_list.keys():
                self.pt_list[i].setText(str(i.y))


class SettingsPanel(QWidget):
    def __init__(self, labjack):
        super().__init__()
        layout = QGridLayout()
        self.setLayout(layout)
        self.setStyleSheet("""
                    QPushButton {
                        background-color: #878787;
                        padding: 5px;
                        border-radius: 15px;
                        }
                    QPushButton:hover {
                        background-color: #8f8f8f;
                    }
                    QPushButton:pressed {
                    background-color: #525252;
                        """)

        # Config JSON button
        json_conf_btn = QPushButton("EDIT JSON")
        layout.addWidget(json_conf_btn, 0, 0, 1, 1)


