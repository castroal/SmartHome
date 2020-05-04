import tuyapower
from PyQt5.QtCore import QThread, pyqtSignal

class DeviceScanner(QThread):
    _signal = pyqtSignal(object)

    def __init__(self, callback, parent=None):
        super().__init__(parent=parent)
        self._signal.connect(callback)

    def run(self):
        devices = tuyapower.deviceScan(True)
        for ip in devices:
            id = devices[ip]['gwId']
            self._signal.emit(
                (id, ip, devices[ip]['productKey'],  devices[ip]['version']))
        self._signal.emit(None)