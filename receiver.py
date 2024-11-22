import pyshark
import time
import os
import requests
import socket


wifi_interface = "wlan1" 
sender_mac = "dc:a6:32:54:ac:c5"
channel = 13
user = ""
url = "https://washington-removed-explore-designer.trycloudflare.com/post/testing/receiver"

old_mac = ""
old_time = 0

host_name = socket.gethostname() 


capture = pyshark.LiveCapture(interface=wifi_interface)


def print_info(packet):
    global old_mac, old_time
    current_time = time.time_ns()
    try:
        if not packet["WLAN.MGT"] or not packet["WLAN"] or not packet["WLAN_RADIO"]:
            return
        if not packet["WLAN"].ta:
            return
        
        if packet["WLAN"].fc_type_subtype == "0x0004":
            if old_mac == packet["WLAN"].ta or (current_time - old_time) / 1000000.0 < 5000.0:
                return

            if packet["WLAN"].ta == sender_mac: 
                

                out_obj = {"host_name":host_name,"internal_time":current_time}

                requests.post(url,json=out_obj)

                old_time = current_time

            old_mac = packet["WLAN"].ta
    except Exception :
        pass

out_str = f'airmon-ng start "{wifi_interface}" {channel} >/dev/null 2>&1'
os.system("echo %s|sudo -S %s" % (user, out_str))

capture.apply_on_packets(print_info, packet_count=10000)#, timeout=50)
