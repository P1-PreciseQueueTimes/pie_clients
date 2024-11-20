#This module finds the ip link thing. your wlcome, yours truly, Aborn.
import subprocess
def find_ip():
    out = subprocess.check_output(["ip","link"])
    txt = str(out)

    start_index = txt.index("WLAN1")
    end_index = txt.index(":",start_index)

    #print(txt[start_index:end_index])
    return txt[start_index:end_index]