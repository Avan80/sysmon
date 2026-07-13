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

wget https://s3.amazonaws.com/amazoncloudwatch-agent/ubuntu/amd64/latest/amazon-cloudwatch-agent.deb
dpkg -i -E ./amazon-cloudwatch-agent.deb

mkdir -p /opt/aws/amazon-cloudwatch-agent/etc
cp /opt/sysmon-repo/amazon-cloudwatch-agent.json /opt/aws/amazon-cloudwatch-agent/etc/amazon-cloudwatch-agent.json

/opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl -a fetch-config -m ec2 -c file:/opt/aws/amazon-cloudwatch-agent/etc/amazon-cloudwatch-agent.json -s

cp /opt/sysmon-repo/sysmon.service /etc/systemd/system/sysmon.service

systemctl daemon-reload
systemctl enable sysmon
systemctl start sysmon