from PyQt6.QtCore import pyqtSignal, Qt, QTimer, QTime
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QStackedWidget, QFormLayout, QHBoxLayout

from rightpanelwidgets import MainPanel
from settingspanel import SettingsPanel


class LeftPanel(QWidget):
    changeWindow = pyqtSignal(int)

    def __init__(self, labjack):
        super().__init__()
        self.labjack = labjack

        # Layout
        layout = QVBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        self.setLayout(layout)

        # Style sheet
        self.setStyleSheet("color: black;"
                           "padding: 0px;"
                           )

        # Text
        self.label = QLabel("BLT\nGCS")
        font = QFont("Helvetica", 24)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setContentsMargins(0, 0, 0, 0)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet("padding: 0px;"
                        "color: black;")
        layout.addWidget(self.label)

        # Buttons
        self.main_but = QPushButton("Main")
        layout.addWidget(self.main_but)
        self.log_but = QPushButton("Log")
        layout.addWidget(self.log_but)
        self.settings_but = QPushButton("Settings")
        layout.addWidget(self.settings_but)

        # Add a space
        layout.addStretch(1)

        # Add time
        self.time = QLabel("")
        font = QFont("Helvetica", 12)
        self.time.setFont(font)
        self.time.setContentsMargins(0, 0, 0, 0)
        self.time.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.time.setStyleSheet("padding: 0px;"
                                "color: black;")
        layout.addWidget(self.time)

        # Format text and buttons
        self.buts = [self.main_but, self.log_but, self.settings_but, self.time]
        for i in self.buts:
            font = QFont("Helvetica", 12)
            i.setFont(font)
            i.setStyleSheet("""
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
            i.setCursor(Qt.CursorShape.PointingHandCursor)

        f = self.main_but.font()
        f.setBold(True)
        self.main_but.setFont(f)

        # Connect buttons
        self.main_but.clicked.connect(lambda: self.changeWindow.emit(0))
        self.log_but.clicked.connect(lambda: self.changeWindow.emit(1))
        self.settings_but.clicked.connect(lambda: self.changeWindow.emit(2))

        self.labjack.timer.updateTime.connect(self.update_time)
        self.changeWindow.connect(self.highlight_button)

    def highlight_button(self, index):
        for idx, btn in enumerate(self.buts):
            f = btn.font()
            f.setBold(idx == index)
            btn.setFont(f)

    def update_time(self, time):
        self.time.setText(time)



class RightPanel(QWidget):
    def __init__(self, left_panel, labjack):
        super().__init__()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        self.setStyleSheet("background-color: #d4d4d4;"
                           "color: black;"
                           "padding: 20px;")

        # Stacked Widget Layout
        self.stacked = QStackedWidget()

        # All page options
        self.main = MainPanel(labjack=labjack)
        self.testing = QWidget()
        self.settings = SettingsPanel(labjack=labjack)

        self.stacked.addWidget(self.main)
        self.stacked.addWidget(self.testing)
        self.stacked.addWidget(self.settings)
        self.stacked.setCurrentIndex(0)

        layout.addWidget(self.stacked)

        left_panel.changeWindow.connect(self.switch_pages)

    def switch_pages(self, index:int):
        self.stacked.setCurrentIndex(index)


class InfoStrip(QWidget):
    def __init__(self, labjack):
        super().__init__()
        self.labjack = labjack


        # Layout
        layout = QHBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        self.setLayout(layout)
        self.setStyleSheet("""
            QWidget {
                color:black;
                padding: 0;
                
            }
            QLabel {
                font-family: Consolas;
                font-size: 11pt;
                padding: 2px;
            }
        """)

        # Forms
        form1 = QFormLayout()
        form1.addRow(QLabel("DAQ: "), QLabel(self.labjack.config["boardInfo"]["version"]))

        form2 = QFormLayout()
        form2.addRow(QLabel(""), QLabel(""))

        form3 = QFormLayout()
        form3.addRow(QLabel("READING: "), QLabel(str(self.labjack.read)))


        # Make format
        layout.addStretch(1)
        layout.addLayout(form1)
        layout.addStretch(1)
        layout.addLayout(form2)
        layout.addStretch(1)
        layout.addLayout(form3)
        layout.addStretch(1)


