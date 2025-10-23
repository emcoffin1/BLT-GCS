from PyQt6.QtCore import QObject, Qt
from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel, QPushButton, QDial, QSlider, QProgressBar

from sensordisplay import SensorDisplayPanel, GraphDisplay


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

        sensorGraph = GraphDisplay(labjack=self.labjack, combo=sensorTable)
        layout.addWidget(sensorGraph,2,0,1,2)


    # def update_values(self):
    #     # iterate over all sensor objects []
    #     for i in self.labjack.sensors:
    #         # if the objects name (object.name) is in pt_list
    #         # adjust the text to the appropriate value
    #         if i in self.pt_list.keys():
    #             self.pt_list[i].setText(str(i.y))





