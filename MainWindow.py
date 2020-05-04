import sys
import tuyapower
import tuyaha.tuyaapi
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from DeviceScanner import DeviceScanner
from SmartSocket import SmartSocket


class MainWindow(object):
    def __init__(self):
        super().__init__()
        self._app = QApplication([])
        self._window = QWidget()
        self._api = tuyaha.TuyaApi()
        self._selectedSmartSocket = None
        self._scanDeviceThread = None
        self._initLayout()

    def _initLayout(self):
        self._userNameWidget = QLineEdit('')
        self._passwordWidget = QLineEdit('')
        self._passwordWidget.setEchoMode(QLineEdit.Password)
        self._countryCode = QLineEdit('39')

        self._connectButton = QPushButton('Connect')
        self._connectButton.clicked.connect(self._connect)
        self._connectButton.setFixedSize(120, 30)

        grid = QGridLayout()
        grid.addWidget(QLabel('Username'), 0, 0)
        grid.addWidget(self._userNameWidget, 0, 1)

        grid.addWidget(QLabel('Password'), 0, 2)
        grid.addWidget(self._passwordWidget, 0, 3)

        grid.addWidget(QLabel('CountryCode'), 0, 4)
        grid.addWidget(self._countryCode, 0, 5)

        grid.addWidget(self._connectButton, 1, 0, 1, 6, alignment=Qt.AlignCenter)

        self._deviceList = QListView()
        self._deviceListModel = QStandardItemModel(self._deviceList)
        self._deviceList.setModel(self._deviceListModel)
        self._deviceList.clicked[QModelIndex].connect(self._onItemClicked)

        grid.addWidget(self._deviceList, 2, 0, 2, 5)

        self._NameLabel = QLabel('')
        self._StateLabel = QLabel('')
        self._WattLabel = QLabel('')
        self._AmpereLabel = QLabel('')
        self._VoltLabel = QLabel('')
        onOffButton = QPushButton('On / Off')
        onOffButton.clicked.connect(self._onOff)
        onOffButton.setFixedSize(120, 30)

        statBox = QVBoxLayout()
        statBox.addWidget(self._NameLabel)
        statBox.addWidget(self._StateLabel)
        statBox.addWidget(self._WattLabel)
        statBox.addWidget(self._AmpereLabel)
        statBox.addWidget(self._VoltLabel)

        grid.addLayout(statBox, 2, 5, alignment=Qt.AlignTop | Qt.AlignLeft)
        grid.addWidget(onOffButton, 3, 5)

        self._window.setWindowTitle('SmartHome')
        self._window.setLayout(grid)

    def _initUpdate(self):
        self._scanDeviceThread = DeviceScanner(self._handleScanDeviceResult)
        self._scanDeviceThread.start()
        self._timer = QTimer()
        self._timer.timeout.connect(self._updatePowerInfo)
        self._timer.start(1000)

    def _updatePowerInfo(self):
        if self._selectedSmartSocket is None:
            return

        self._NameLabel.setText(f'Name: {self._selectedSmartSocket.name}')
        self._StateLabel.setText(f'State: {"on" if self._selectedSmartSocket.state else "off"}')

        if self._selectedSmartSocket.key is None:
            self._WattLabel.setText('Watts: updating...')
            self._AmpereLabel.setText('mA: updating...')
            self._VoltLabel.setText('Volts: updating...')
            return

        (state, W, mA, V, err) = tuyapower.deviceInfo(
            self._selectedSmartSocket.id,
            self._selectedSmartSocket.ip,
            self._selectedSmartSocket.key,
            self._selectedSmartSocket.version)

        self._selectedSmartSocket.state = state
        self._selectedSmartSocket.W = W
        self._selectedSmartSocket.mA = mA
        self._selectedSmartSocket.V = V

        self._WattLabel.setText(f'Watts: {self._selectedSmartSocket.W}')
        self._AmpereLabel.setText(f'mA: {self._selectedSmartSocket.mA}')
        self._VoltLabel.setText(f'Volts: {self._selectedSmartSocket.V}')

    def _handleScanDeviceResult(self, result):
        if result is None:
            self._scanDeviceThread = None
            self._connectButton.setText('Connect')
            self._connectButton.setEnabled(True)
            return

        (id, ip, key, version) = result
        for index in range(self._deviceListModel.rowCount()):
            smartSocket = self._deviceListModel.item(index).data()
            if smartSocket.id == id:
                smartSocket.ip = ip
                smartSocket.key = key
                smartSocket.version = version
                break

    def _connect(self):
        try:
            username = self._userNameWidget.text()
            password = self._passwordWidget.text()
            countryCode = self._countryCode.text()

            if len(username) == 0 or len(password) == 0 or len(countryCode) == 0:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setText("Please insert login data")
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec_()
                return

            self._api.init(username, password, countryCode, 'smart_life')

            devices = self._api.discover_devices()

            self._deviceListModel.clear()

            for device in devices:
                smartSocket = SmartSocket(
                    device['id'], device['name'], device['data']['online'], device['data']['state'])
                item = QStandardItem(
                    f'[{"Online" if smartSocket.online else "Offline":7}] {smartSocket.name}')
                item.setFont(QFont('Consolas'))
                item.setData(smartSocket)
                self._deviceListModel.appendRow(item)
            
            self._connectButton.setText('Scanning...')
            self._connectButton.setEnabled(False)
            self._initUpdate()
        except Exception as e:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("An error occurred: " + e.args[0])
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()

    def _onItemClicked(self, index):
        item = self._deviceListModel.itemFromIndex(index)
        self._selectedSmartSocket = item.data()
        
    def _onOff(self):
        if self._selectedSmartSocket is None:
            return
        device = self._api.get_device_by_id(self._selectedSmartSocket.id)
        if self._selectedSmartSocket.state:
            device.turn_off()
        else:
            device.turn_on()
        self._selectedSmartSocket.state = not self._selectedSmartSocket.state

    def show(self):
        self._window.show()
        self._app.exec_()

if __name__ == "__main__":
    mainWindow = MainWindow()
    mainWindow.show()
