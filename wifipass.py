#!/usr/bin/env python
import subprocess
import re

def get_passwd(wifi):
    cmd = "netsh wlan show profile " + wifi + " key=clear"
    wifi_info = subprocess.check_output(cmd, shell=True)
    wifi_info=wifi_info.decode('utf-8')
    wifi_pass = re.search("(?:Key Content\s*:\s)(.*)", wifi_info)
    return wifi_pass

def wifi_harvester():
    cmd = "netsh wlan show profile"
    network = subprocess.check_output(cmd, shell=True)
    network = network.decode('utf-8')
    net_names = re.findall("(?:Profile\s*:\s)(.*)", network)
    result = {}
    for wifi in net_names:
        cmd = "netsh wlan show profile " + wifi
        net_profile = subprocess.check_output(cmd, shell=True)
        net_profile = net_profile.decode('utf-8')
        if not "no such wireless interface" in net_profile:
            wifi_pass = get_passwd(wifi)
            if wifi_pass:
                result[wifi] = wifi_pass.group(1)
    return result

credentials = wifi_harvester()
message = ""
for wifi in credentials:
    message = message + wifi.rstrip() +  " ----> " + credentials[wifi].rstrip() + "\n"
print(message)