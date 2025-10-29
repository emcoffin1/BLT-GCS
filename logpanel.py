from PyQt6.QtWidgets import (QVBoxLayout, QWidget, QPlainTextEdit, QPushButton, QHBoxLayout, QTableWidgetItem,
                             QTableWidget, QSplitter)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
import pandas as pd

class LogPanel(QWidget):
    def __init__(self, labjack):
        super().__init__()
        self.labjack = labjack

        v_layout = QVBoxLayout()
        self.setLayout(v_layout)
        self.setStyleSheet("""
            QPlainTextEdit {
                background-color: black;
                color: white;
            }
            QTableWidget {
                background-color: black;
                color: white;
            }
            QPushButton {
                border-radius: 5px;
                border: 1px solid black;
                background-color: grey;}
                color: white;
                padding: 0;
            QPushButton::Hover {
                border-radius: 5px;
                border: 1px solid black;
                background-color: white;}
                color: white;
                padding: 0;
            }
            """)

        h_layout = QSplitter(Qt.Orientation.Horizontal)
        self.log_view = QTableWidget()
        self.err_view = QPlainTextEdit()
        h_layout.addWidget(self.log_view)
        h_layout.addWidget(self.err_view)

        btn_layout = QHBoxLayout()

        font = QFont("Helvetica", 16)

        save_btn = QPushButton("SAVE")
        save_btn.setFixedHeight(50)
        save_btn.setFixedWidth(150)
        save_btn.setFont(font)

        delete_btn = QPushButton("CLEAR DATA")
        delete_btn.setFixedHeight(50)
        delete_btn.setFixedWidth(150)
        delete_btn.setFont(font)
        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(delete_btn)

        v_layout.addWidget(h_layout)
        v_layout.addLayout(btn_layout)

        save_btn.clicked.connect(self.start_record)
        self.labjack.updateLog.connect(self.update_file)


    def update_file(self):
        try:
            df = pd.read_csv(self.labjack._filename)
            last_row = df.tail(1).reset_index(drop=True)

            if self.log_view.rowCount() == 0:
                self.log_view.setColumnCount(len(df.columns))
                self.log_view.setHorizontalHeaderLabels(df.columns)

            current_rows = self.log_view.rowCount()
            self.log_view.insertRow(current_rows)

            for j, value in enumerate(last_row.iloc[0]):
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.log_view.setItem(current_rows, j, item)

            self.log_view.scrollToBottom()

        except Exception as e:
            pass

    def clear_data_log(self):
        pass

    def start_record(self):
        self.labjack.start_recording()

