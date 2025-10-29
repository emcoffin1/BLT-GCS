from datetime import datetime

from PyQt6.QtCore import QObject, QTimer, QTime, pyqtSignal


class Timer(QObject):
    updateTime = pyqtSignal(str)
    updateValues = pyqtSignal(str)
    def __init__(self, parent=None):
        QObject.__init__(self, parent)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update)


    def update(self):
        current_time = QTime.currentTime().toString("HH:mm:ss")
        self.updateTime.emit(current_time)
        self.updateValues.emit(current_time)

    def start_timer(self, config):
        self.timer.stop()
        self.timer.start(config["boardInfo"]["sampleRate"])


def log_error(e):
    time = datetime.now()
    time = time.strftime("%d/%m/%y - %H:%M:%S")
    msg = e
    with open('error_log.txt', 'a') as f:
        f.write(str(time) + ': ' + str(msg) + '\n')


def calibration(c: list, x:float):
    """
    Calibration function (c) must be input as list(a, b, c)
    where x is the x value, b is the slope, and c is the offset
    :param c: Calibration equation
    :param x: Uncalibrated value
    :return: x Calibrated value
    """
    a = c[0]
    b = c[1]
    c = c[2]
    y = a*x**2 + b*x + c
    return y

if __name__ == '__main__':
    calibration([1, 4, -5], 5)
    log_error("Eror")

