# CHANGELOG

All notable changes to this project will be documented in this file.
This project adheres to [Semantic Versioning](http://semver.org/) and [Keep a Changelog](http://keepachangelog.com/).



## Unreleased
---

### New

### Changes

### Fixes

### Breaks


## 0.1.3 (2023-06-18)
---

### New
send_email.py and send_email.sh created.


## 0.1.2 (2023-06-17)
---

### New
CHANGELOG.md file created.
"hostname_mac-example.txt" and "hostname_mac.txt" files moved to project root.
pynettools.sh and recycle_hosts_bkp.sh created.
crontab-example.txt created.

### Changes
"get_ip_from_mac_addr.py" renamed to "pynettools_main.py".

### Fix
self.platform.is_mac is a method, not a property.
mac_addr to lower case also when it's linux.
nmap () substitution is also made in linux.
Debug platform print moved to main().


## 0.1.1 (2023-06-16)
---

### New
/etc/hosts file batch update with fresh IPs with -u option (update_from_input_entries, populate_input_entries).


## 0.1.0 (2023-06-15)
---

### New
Initital development of a simple program to get the IP address from a MAC address (get_ip_from_mac_addr.py), then converted to the project PyNetTools.
Get the IP address from a MAC address using the "arp -a" command (get_ip_from_mac).
Run "nmap" command to discover all network devices, prior to run "arp -a" (run_nmap, get_start_ip).
Get the current host IP address (get_local_ip).
List all hostname, MAC and IP addresses with -l option (list_input_entries).
Parse command line arguments and command help (init_parser).
Hostfile management class.
Platform management class.
