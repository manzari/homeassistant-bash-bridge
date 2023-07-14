# Homeassistant Bash Bridge
This script can run in the background while publishing stats to homeassistant as well as executing preconfigured commands

## Install
```bash
python -m venv env
source env/bin/activate
pip install -r requirements.txt
mv config.ini.sample config.ini
nano config.ini
python main.py
```

### As a service
```bash
chmod +x run.sh
nano /etc/systemd/system/homeassistant-bash-bridge.service
```
```
[Unit]
Description=Homeassistant Bash Bridge

[Service]
Type=simple
ExecStart=/root/homeassistant-bash-bridge/run.sh

[Install]
WantedBy=multi-user.target
```
```bash
systemctl daemon-reload
systemctl enable homeassistant-bash-bridge.service
systemctl start homeassistant-bash-bridge.service
systemctl status homeassistant-bash-bridge.service
```
