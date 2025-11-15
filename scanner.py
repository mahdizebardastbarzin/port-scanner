# ------------------------------------------------------------
# English Comment:
# Professional TCP/UDP Port Scanner with JSON + HTML reporting
# Author: Mahdi Zebardast Barzin
# ------------------------------------------------------------

"""
------------------------------------------------------------
توضیح فارسی:
این فایل ماژول اصلی اسکن پورت است.
پروژه شامل:
- اسکن TCP
- اسکن UDP
- ساخت گزارش JSON
- ارسال داده‌ها برای ساخت گزارش HTML

نویسنده: مهدی زبردست برزین
------------------------------------------------------------
"""

import socket
import json
import threading
from report_builder import generate_html_report

open_ports = []

def scan_tcp(target, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.3)
        result = sock.connect_ex((target, port))
        if result == 0:
            open_ports.append({"port": port, "type": "TCP"})
        sock.close()
    except:
        pass

def scan_udp(target, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(0.3)
        sock.sendto(b"Hello", (target, port))
        sock.recvfrom(1024)
        open_ports.append({"port": port, "type": "UDP"})
    except socket.timeout:
        pass
    except:
        pass

def run_scan(target, ports):
    threads = []

    for port in ports:
        t1 = threading.Thread(target=scan_tcp, args=(target, port))
        t2 = threading.Thread(target=scan_udp, args=(target, port))

        threads.append(t1)
        threads.append(t2)

        t1.start()
        t2.start()

    for t in threads:
        t.join()

    # ذخیره JSON
    with open("results/result.json", "w", encoding="utf-8") as f:
        json.dump(open_ports, f, indent=4, ensure_ascii=False)

    # ساخت HTML
    generate_html_report(open_ports)

    print("✔ اسکن کامل شد! گزارش‌ها در پوشه results ذخیره شد.")
    return open_ports


if __name__ == "__main__":
    target_ip = input("Enter Target IP: ")
    port_range = range(1, 200)  # کم کن یا زیاد کن

    print("Scanning... Please wait...")
    run_scan(target_ip, port_range)
