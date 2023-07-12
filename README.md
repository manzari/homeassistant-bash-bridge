# Homeassistant Bash Bridge
This script can run in the background while publishing stats to homeassistant as well as executing preconfigured commands

## Install
```bash
pip install -r requirements.txt
mv config.ini.sample config.ini
nano config.ini
python main.py
```

### As a service
Create a service definition `/etc/systemd/system/hass-bash-bridge.service`
```
[Unit]
Description=Homeassistant Bash Bridge

[Service]
Type=simple
ExecStart=python /home/user/main.py
```
