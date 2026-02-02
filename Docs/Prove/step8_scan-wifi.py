# maurizio.conti@fablabromagna.org
# Vibe coding 2026
#

import wifi

for n in wifi.radio.start_scanning_networks():
    try:
        print(n.ssid, n.channel, n.rssi, n.authmode)
    except Exception as e:
        print("err", e)

wifi.radio.stop_scanning_networks()
