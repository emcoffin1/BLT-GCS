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
        # self.setGeometry(10,10, 1080, 720)
        self.setStyleSheet("background-color: darkgrey;"
                           "color: white;")

        self.left_panel = LeftPanel(labjack=labjack)
        self.right_panel = RightPanel(left_panel=self.left_panel, labjack=labjack)
        self.top = InfoStrip(labjack=labjack)

        # Outer Layout
        container = QWidget()
        o_layout = QVBoxLayout(container)
        o_layout.addWidget(self.top)


        # Inner Layout
        layout = QHBoxLayout()
        layout.addWidget(self.left_panel)
        layout.addWidget(self.right_panel)
        self.left_panel.setFixedWidth(int(self.width()*0.05))

        o_layout.addLayout(layout)
        self.setLayout(o_layout)


        self.setCentralWidget(container)

        # Trigger events
        # labjack.timer.updateTime.connect(self.left_panel.update_time)

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