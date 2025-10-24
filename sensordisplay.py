from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QComboBox, QStackedWidget, QFormLayout, QLabel, QHBoxLayout, \
    QScrollArea, QSizePolicy
import pyqtgraph as pg

from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QComboBox, QStackedWidget, QFormLayout, QLabel,
    QScrollArea, QSizePolicy
)
import pyqtgraph as pg

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

        # === Combo Box ===
        self.table_list = self.labjack.config["tableLists"]
        self.selector = QComboBox()
        self.selector.addItems(self.table_list)
        self.selector.setFixedHeight(22)
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
            }
        """)
        layout.addWidget(self.selector)

        # === Scrollable Area ===
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("border:none;")
        layout.addWidget(self.scroll_area)

        # === Scroll content ===
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_content.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.stacked = QStackedWidget()
        self.stacked.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.value_labels = {}
        self.forms = {}
        for form_name, sensor_name in self.table_list.items():
            form_widget = QWidget()
            form_layout = QFormLayout(form_widget)
            form_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

            self.value_labels[form_name] = {}

            for name in sensor_name:
                sensor = self.labjack.sensor_lookup.get(name)
                if not sensor:
                    continue

                font = QFont("Consolas", 20)
                font.setBold(True)
                name_label = QLabel(f"{sensor.name}: ")
                name_label.setFont(font)
                value_label = QLabel(f"{sensor.y:.2f}")
                value_label.setFont(font)
                value_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

                form_layout.addRow(name_label, value_label)

                self.value_labels[form_name][sensor.name] = value_label

            self.stacked.addWidget(form_widget)
            self.forms[form_name] = form_widget

        scroll_layout.addWidget(self.stacked)
        scroll_content.setStyleSheet("border: 1px solid black;")
        self.scroll_area.setWidget(scroll_content)
        # === Initial State ===
        self.selector.setCurrentIndex(0)

        # === Connections ===
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
            half_width = self.parent().width() // 3
            half_height = self.parent().height() // 2
            self.setFixedWidth(half_width)
            self.setMaximumHeight(half_height)
        super().resizeEvent(event)


class GraphDisplay(QWidget):
    def __init__(self, labjack, combo):
        super().__init__()

        self.labjack = labjack
        self.combo = combo

        # Layout
        layout = QHBoxLayout()
        self.setLayout(layout)

        # Widget
        self.plot_widget = pg.PlotWidget()
        layout.addWidget(self.plot_widget)

        # Plot layout
        self.plot_widget.addLegend()
        self.plot_widget.setLabel('left', 'PSI', units='-')
        self.plot_widget.setLabel('bottom', units='-')
        self.plot_widget.showGrid(x=True, y=True)



        self.update_graph()
        self.combo.selector.currentIndexChanged.connect(self.update_graph)
        self.labjack.timer.updateValues.connect(self.refresh_graph)

    def update_graph(self):
        self.plot_widget.clear()  # fine to clear here, user just switched
        selected = self.combo.selector.currentText()
        table = self.labjack.config["tableLists"][selected]
        colors = ["r", "g", "b", "y", "c", "w", "m"]
        colors = 3 * colors
        self.curves = {}  # store curves by sensor name
        for i, name in enumerate(table):
            pen = pg.mkPen(color=colors[i], width=2)

            curve = self.plot_widget.plot(name=name, pen=pen)
            self.curves[name] = curve

    def refresh_graph(self):
        for name, curve in self.curves.items():
            obj = self.labjack.sensor_lookup[name]
            data = obj.y_history
            curve.setData(data)







