# SmartHome
SmartHome is a small app to switch on/off Tuya smart sockets.

![](/images/smarthome.png)

## How to use

- Fill the **Username** and **Password** with the same credentials for the SmartLife app (the username is usually the phone number)
- For the **CountryCode** use the *International calling code* from [here](https://en.wikipedia.org/wiki/List_of_mobile_telephone_prefixes_by_country)
- Click **Connect**
- Use the **On/Off** button to switch on or off the selected socket

> To correctly visualize the statistics (power, ampere, volts) you have to allow the app through the Windows firewall (device discovery is done using udp broadcast)

## Build

You can find a binary build for Windows in the release page.

If you want to run from sources:

1. Create a python virtual env [optional] `python -m venv pyenv`
2. Install the following requirements:
    - `pip install pycryptodome`
    - `pip install pytuya`
    - `pip install tuyapower`
    - `pip install requests`
    - `pip install PyQt5`
4. Run `python .\MainWindow.py`

To build a self contained executable use [pyinstaller](https://www.pyinstaller.org/):

- `pip install pyinstaller`
- `pyinstaller --name="SmartHome" --windowed --onefile .\MainWindow.py`

## Credits

- tuyaha: https://github.com/PaulAnnekov/tuyaha
- pytuya: https://github.com/clach04/python-tuya
- tuyapower: https://github.com/jasonacox/tuyapower