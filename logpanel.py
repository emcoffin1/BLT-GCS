from PyQt6.QtWidgets import QVBoxLayout, QWidget, QPlainTextEdit, QPushButton, QHBoxLayout
from datetime import datetime
from PyQt6.QtGui import QFont

class LogPanel(QWidget):
    def __init__(self, labjack):
        super().__init__()
        self.labjack = labjack
        self.record = False

        v_layout = QVBoxLayout()
        self.setLayout(v_layout)
        self.setStyleSheet("""
            QPlainTextEdit {
                background-color: black;
                color: white;
            }
            """)

        h_layout = QHBoxLayout()
        textview = QPlainTextEdit()
        logview = QPlainTextEdit()
        h_layout.addWidget(textview)
        h_layout.addWidget(logview)

        font = QFont("Helvetica", 16)
        save_btn = QPushButton("SAVE")
        save_btn.setStyleSheet("""
            QPushButton {
            border-radius: 5px;
            border: 1px solid black;
            background-color: grey;}
            color: white;
            padding: 0;
        """)
        save_btn.setFixedHeight(50)
        save_btn.setFixedWidth(150)
        save_btn.setFont(font)
        v_layout.addLayout(h_layout)
        v_layout.addWidget(save_btn)


    def update_file(self):
        if self.record:
            time = datetime.now()
            time = time.strftime("%d/%m/%y - %H:%M:%S")

            # with open('log', "w")