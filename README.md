
# Downloader

**Version 1.0.0**

A Programm that automatically downloads files from <https://workgroups.helsinki.fi>

Tested and working on Ubuntu 18.04.5 LTS, Windows 10 Home and macOS Big Sur



## Installation 

1. Select and download the correct package for your OS and Chrome-version from [Releases](https://github.com/tobi314/downloader/releases/)

2. Extract the zip-file

&nbsp;&nbsp;&nbsp;**or**

1. Download the source code

2. Install required python modules

```bash
pip install -r requirements.txt
```
3. Make required folder structure
```bash
mkdir lib
```
4. [Download chromedriver](https://sites.google.com/chromium.org/driver/downloads) and extract it into ./lib

5. Compile the app (or just leave it be and execute main.py)
```bash
pyinstaller main.spec
```
## License & copyright

Distributed under the [MIT License](https://choosealicense.com/licenses/mit/)

© Tobias A. Jeltsch


