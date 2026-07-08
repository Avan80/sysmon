#!/bin/bash
set -euo pipefail

apt-get update
apt-get install -y python3 python3-pip git

useradd --system --no-create-home --shell /usr/sbin/nologin sysmon || true 

mkdir -p /var/log/sysmon
chown sysmon:sysmon /var/log/sysmon

git clone https://github.com/Avan80/sysmon.git /opt/sysmon-repo

mkdir -p /opt/sysmon
cp /opt/sysmon-repo/systems_monitor.py /opt/sysmon/systems_monitor.py


chown root:root /opt/sysmon/systems_monitor.py
chmod 644 /opt/sysmon/systems_monitor.py

pip3 install psutil --break-system-packages

echo "sysmon ALL=(root) NOPASSWD: /usr/bin/python3 /opt/sysmon/systems_monitor.py" > /etc/sudoers.d/sysmon
chmod 440 /etc/sudoers.d/sysmon

cp /opt/sysmon-repo/sysmon.service /etc/systemd/system/sysmon.service

systemctl daemon-reload
systemctl enable sysmon
systemctl start sysmon
