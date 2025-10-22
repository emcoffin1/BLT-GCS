from PyQt6.QtWidgets import (QApplication, QMainWindow, QMessageBox, QHBoxLayout)
from main_access_wrappers import LabJack
from mainwindowpanels import *
from util_func import *



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        global labjack, timer
        labjack = LabJack()
        labjack.connect_labjack()

        # Window title and size
        self.setWindowTitle("BLT-GCS")
        self.showFullScreen()
        self.setStyleSheet("background-color: darkgrey;"
                           "color: white;")

        self.left_panel = LeftPanel()
        self.right_panel = RightPanel(left_panel=self.left_panel, labjack=labjack)

        # Layout
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.addWidget(self.left_panel)
        layout.addWidget(self.right_panel)
        self.left_panel.setFixedWidth(int(self.width()*0.05))

        self.setLayout(layout)


        self.setCentralWidget(container)

        # Trigger events
        labjack.timer.updateTime.connect(self.left_panel.update_time)
        # timer.updateTime.connect(labjack.read_port)
        labjack.updateValues.connect(self.right_panel.update_values)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            msg = QMessageBox()
            msg.setWindowTitle("CONFIRM")
            msg.setText("Are your sure you would like to exit the program?")
            msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            msg.setDefaultButton(QMessageBox.StandardButton.Yes)
            resp = msg.exec()
            if resp == QMessageBox.StandardButton.Yes:
                self.close()
            else:
                pass