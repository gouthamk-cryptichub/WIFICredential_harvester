#!/usr/bin/env python
import subprocess
import re

cmd = "netsh wlan show profile"
network = subprocess.check_output(cmd, shell=True)
network = network.decode('utf-8')
net_names = re.findall("(?:Profile\s*:\s)(.*)", network)

result = {}
for wifi in net_names:
    cmd = "netsh wlan show profile " + wifi
    net_profile = subprocess.check_output(cmd, shell=True)
    net_profile =net_profile.decode('utf-8')
    if not "no such wireless interface" in net_profile:
        cmd = "netsh wlan show profile " + wifi + " key=clear"
        wifi_info = subprocess.check_output(cmd, shell=True)
        wifi_info = wifi_info.decode('utf-8')
        wifi_pass = re.search("(?:Key Content\s*:\s)(.*)", wifi_info)
        if wifi_pass:
            result[wifi] = wifi_pass.group(1)
print(result)