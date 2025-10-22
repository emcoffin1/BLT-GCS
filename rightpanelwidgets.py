from PyQt6.QtCore import QObject
from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel, QPushButton


class MainPanel(QWidget):
    def __init__(self, labjack):
        super().__init__()

        # Layout
        layout = QGridLayout()
        self.setLayout(layout)
        self.setStyleSheet("background-color: #d4d4d4;"
                           "color: black;"
                           "padding: 20px;")

        # Contents
        label = QLabel("Main")
        layout.addWidget(label)

        # PT Readings
        self.pt_list = {}
        for i in labjack.config["inputChannels"]:
            self.pt_list[i] = QLabel("0")
            layout.addWidget(self.pt_list[i])

        labjack.updateValues.connect(self.update_values)


    def update_values(self, updates):
        for s, v in self.pt_list.items():
            if s in updates.keys():
                updates[s] = round(updates[s], 2)
                v.setText(str(updates[s]))


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


