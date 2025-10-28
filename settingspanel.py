from PyQt6.QtCore import pyqtSignal, QTimer
from PyQt6.QtGui import QFont
import json
from PyQt6.QtWidgets import QWidget, QGridLayout, QPushButton, QDialog, QPlainTextEdit, QFileDialog, QLineEdit, \
    QMessageBox, QComboBox, QVBoxLayout, QFrame
from util_func import log_error


class SettingsPanel(QWidget):
    def __init__(self, labjack):
        super().__init__()
        self.labjack = labjack

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
        json_conf_btn = QPushButton("EDIT FULL JSON")
        layout.addWidget(json_conf_btn, 0, 0, 1, 1)
        json_conf_btn.clicked.connect(self.launch_config_editor)

        self.calibration_edt = CalibrationEditor(labjack=self.labjack)

        layout.addWidget(self.calibration_edt, 0,1,1,1)


    def launch_config_editor(self):
        self.editor = ConfigEditor(labjack=self.labjack)
        self.editor.show()


class CalibrationEditor(QWidget):
    def __init__(self, labjack):
        super().__init__()
        self.labjack = labjack
        width = 200

        # Frame setup
        outer_layout = QVBoxLayout(self)
        frame = QFrame()
        frame.setFrameShape(QFrame.Shape.Box)
        frame.setFixedWidth(width+20)
        frame.setFixedHeight(width+40)
        frame.setContentsMargins(0,0,0,0)
        frame.setLineWidth(2)
        frame.setStyleSheet("""
                QFrame {
                    color: white;
                    background-color:black;
                    border: 2px solid black;
                    border-radius: 10px;
                    padding: 0;
                }
            """)


        # Normal Layout
        layout = QVBoxLayout(frame)
        self.setLayout(layout)

        # Combo box port selector
        self.selector = QComboBox()
        self.selector.addItems(i.name for i in self.labjack.sensors)
        self.selector.setFixedWidth(width)
        self.selector.setFixedHeight(20)
        self.selector.setContentsMargins(0, 0, 0, 0)
        self.selector.setStyleSheet("""
                                            QComboBox {
                                                color: black;
                                                background-color: white;
                                                padding: 1px;
                                                border: 1px solid grey;
                                                border-radius: 5px;
                                                text-align: center;
                                            }
                                            QComboBox::drop-down {
                                                border: none;
                                                text-align: center;
                                            }
                                                """)
        layout.addWidget(self.selector)

        self.editor = QPlainTextEdit()
        self.editor.setContentsMargins(0, 0, 0, 0)
        self.editor.setFixedWidth(width)
        self.editor.setFixedHeight(width)
        self.editor.setStyleSheet("""
            QPlainTextEdit {
                color: white;
                padding: 0;
            }
            """)
        layout.addWidget(self.editor)
        self.path = "config.json"

        # Autosave Timer
        self.autosave_timer = QTimer()
        self.autosave_timer.setSingleShot(True)
        self.autosave_timer.timeout.connect(self.autosave)
        self.editor.textChanged.connect(self.schedule_autosave)

        outer_layout.addWidget(frame)
        self.selector.currentIndexChanged.connect(self.change_text)

    def change_text(self):
        name = self.selector.currentText()
        try:
            with open(self.path, 'r', encoding='utf-8') as f:
                full_text = json.load(f)
            section = full_text["inputChannels"][name]

            # Block signals, load, unblock signals
            self.editor.blockSignals(True)
            self.editor.setPlainText(json.dumps(section, indent=3))
            self.editor.blockSignals(False)

        except Exception as e:
            log_error(e)
            self.editor.setPlainText("SENSOR NOT FOUND")

    def autosave(self):
        name = self.selector.currentText()
        new_text = self.editor.toPlainText()

        try:
            with open(self.path, 'r', encoding='utf-8') as f:
                full_text = json.load(f)

            # Parse edited sections
            new_data = json.loads(new_text)
            full_text["inputChannels"][name] = new_data

            # Write back
            with open(self.path, 'w', encoding='utf-8') as f:
                json.dump(full_text, f, indent=3)

            # Update Config
            self.labjack.get_config()

        except Exception as e:
            log_error(e)

    def schedule_autosave(self):
        print(1)
        self.autosave_timer.start(1500)


class ConfigEditor(QWidget):

    def __init__(self, labjack):
        super().__init__()
        self.setWindowTitle("Config Editor")
        self.labjack = labjack
        self.setGeometry(300, 300, 750, 750)

        layout = QGridLayout()
        self.setLayout(layout)

        self.editor = QPlainTextEdit()
        self.path = "config.json"

        btn_save = QPushButton("SAVE")
        btn_close = QPushButton("CLOSE")

        layout.addWidget(self.editor, 0,0,1,2)
        layout.addWidget(btn_save,1,0,1,1)
        layout.addWidget(btn_close,1,1,1,1)

        self.open_file()
        btn_close.clicked.connect(self.close)
        btn_save.clicked.connect(self.save_file)

    def open_file(self):
        try:
            with open(self.path, "r", encoding='utf-8') as f:
                text = f.read()
            font = QFont("Consolar", 16)
            self.editor.setPlainText(text)
            self.editor.setFont(font)
        except Exception as e:
            log_error(e)


    def save_file(self):
        with open(self.path, 'w', encoding='utf-8') as f:
            f.write(self.editor.toPlainText())
        self.labjack.get_config()


