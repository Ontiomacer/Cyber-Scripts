#!/usr/bin/env python
import subprocess
import optparse
import re


def get_args():
    parser = optparse.OptionParser()

    parser.add_option("-i", "--interface", dest="interface", help="Interface to change it's mac address")
    parser.add_option("-m", "--MAC", dest="new_mac", help="New mac address")

    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[-] Please specify an interface , use --help for help")
    elif not options.new_mac:
        parser.error("[-] Please specify a mac, use --help for help")

    return options


def modif_mac(interface, new_mac):
    print("[+] Changing MAC Address for " + interface + " to " + new_mac)
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])
    subprocess.call("ifconfig")


def mac_result(interface):
    output_ifconfig = subprocess.check_output(["ifconfig", interface]).decode('utf-8')
    mac_address_search_result = re.search(r"(\w\w:\w\w:\w\w:\w\w:\w\w:\w\w)", output_ifconfig)
    if mac_address_search_result:
        return mac_address_search_result.group(0)
    else:
        print("[-] Are you sure this interface has a MAC..!!")


options = get_args()
current_mac = mac_result(options.interface)
print("Current Mac = " + str(current_mac))

modif_mac(options.interface, options.new_mac)
current_mac = mac_result(options.interface)
if current_mac == options.new_mac:
    print("[+] Your new mac is > " + current_mac)
else:
    print("[-] Sorry mac didn't change")
