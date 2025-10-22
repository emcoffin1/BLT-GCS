from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QComboBox, QStackedWidget, QFormLayout, QLabel


class SensorDisplayPanel(QWidget):
    def __init__(self, labjack):
        super().__init__()
        widget_master = QWidget()
        self.labjack = labjack

        layout = QVBoxLayout(widget_master)
        self.setLayout(layout)
        self.setStyleSheet("background-color: white;"
                           "padding: 0px;"
                           "border: 0.5px solid black;"
                           "border-radius: 5px;")

        self.table_list = self.labjack.config["tableLists"]
        self.selector = QComboBox()
        self.selector.addItems(self.table_list)
        self.selector.setFixedWidth(100)
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

        self.stacked = QStackedWidget()
        self.value_labels = {}
        self.forms = {}
        for form_name, sensor_name in self.table_list.items():
            form_widget = QWidget()
            form_layout = QFormLayout(form_widget)

            self.value_labels[form_name] = {}

            for name in sensor_name:
                sensor = self.labjack.sensor_lookup.get(name)
                if not sensor:
                    continue

                font = QFont("Helvetica", 24)
                font.setBold(True)
                name_label = QLabel(f"{sensor.name}: ")
                name_label.setFont(font)
                value_label = QLabel(f"{sensor.y:.2f}")
                value_label.setFont(font)

                form_layout.addRow(name_label, value_label)
                self.value_labels[form_name][sensor.name] = value_label

            self.stacked.addWidget(form_widget)
            self.forms[form_name] = form_widget


        layout.addWidget(self.stacked)

        self.selector.setCurrentIndex(0)

        self.selector.currentIndexChanged.connect(self.stacked.setCurrentIndex)
        self.labjack.timer.updateValues.connect(self.update_values)


    def update_values(self):
        for form_name, sensors in self.value_labels.items():
            for name, label in sensors.items():
                sensor = self.labjack.sensor_lookup.get(name)
                if sensor:
                    label.setText(f"{sensor.y:.2f}")

    def resizeEvent(self, event):
        if self.parent():
            half_width = self.parent().width() // 4
            self.setFixedWidth(half_width)
        super().resizeEvent(event)
