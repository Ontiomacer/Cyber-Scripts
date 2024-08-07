#!/usr/bin/env python
import kamene.all as scapy
import argparse


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", dest="target", help="Target IP/IP Range", required=True)
    options = parser.parse_args()
    return options


def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    client_list = []

    for i in answered_list:
        client_dict = {"ip": i[1].psrc, "mac": i[1].hwsrc}
        client_list.append(client_dict)
    return client_list


def result(output_data):
    print("IP\t\t\t\t MAC Address\n--------------------------------------------------")
    for i in output_data:
        print(f"{i['ip']}\t\t{i['mac']}")


options = get_args()
scan_output = scan(options.target)
result(scan_output)
