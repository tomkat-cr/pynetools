# PyNetTools

<p align="center"><img src="https://socialify.git.ci/tomkat-cr/pynettools/image?description=0&amp;font=Inter&amp;language=1&amp;name=1&amp;owner=1&amp;pattern=Plus&amp;stargazers=0&amp;theme=Light" alt="project-image"></p>

## Overview

This is a simple networking tool in python that allows users to read from an input file with hostname and MAC address and update the system's host file accordingly. It was built to discover, map and maintain IP-Hostname mapping in a local network.

## Functionality

1. Discover all the 256 devices in the current network segment: List all hostname, MAC and IP addresses for items in the input file.
2. List all hostname, MAC and IP addresses for items in the input file.
3. Update the content of the host file from gathered IPs in the input file.
4. Update the host file from gathered IPs in the input file.
5. Show the content of the host file.
6. Check if the host name exists in the host file.
7. Insert HOSTNAME[:IP] mappings into the host file.
8. Remove mapping for HOSTNAME from host file.

## Project Organisation

Here is a tree view of the files in the repository:

```
.
├─ src
│   ├── Platform.py
│   ├── PyNetTools.py
│   ├── Host.py
│   ├── pynettools_main.py
│   ├── send_email.py
│   └── init_parser.py
├─ recycle_hosts_bkp.sh
├─ pymenttools.sh
├─ send_email.sh
├─ crontab-example.txt
├─ hostname_mac-example.txt
├─ LICENSE
├─ CHANGELOG.md
├─ .gitignore
├─ .env-example
└─ README.md

```

## Scripts

1. recycle_hosts_bkp.sh: This is a shell script to clean /etc/hosts backup files.
2. send_email.sh: This is a shell script to send emails through the SMTP server.
3. pynettools.sh: This is a shell script that executes the PyNetTools main function with necessary parameters.

## Input file example

The input file in the format `hostname_mac.txt` should look like this:

```
MAC_ADDRESS1 HOSTNAME1
MAC_ADDRESS2 HOSTNAME2
```

The provided `hostname_mac-example.txt` template file can be used to generate it:

```bash
cp hostname_mac-example.txt hostname_mac.txt
vi hostname_mac.txt
```

## Testing & Execution

To test and run this repository, follow the below steps:

1. Install Python3.

2. Generate the `.env` file to send Email notifications:

```bash
cp .env-example .env
vi .env
```

Specifiy these parameters:

```bash
# To send emails, set these parameters:
SMTP_SERVER=SMTP_SERVER_value
SMTP_PORT=SMTP_PORT_value
SMTP_USER=SMTP_USER_value
SMTP_PASSWORD=SMTP_PASSWORD_value
SMTP_DEFAULT_SENDER=SMTP_DEFAULT_SENDER_value
# Recycle files older than: ${PAR_MTIME} days.
PAR_MTIME=5
# Exclude filenames having ${EXCLUDE_FILENAMES_WITH} in it.
EXCLUDE_FILENAMES_WITH=ocrcorp
```

3. Run the desired functions via Python CLI or execute the shell scripts.

```bash
# PyNetTools /etc/host file update
sh pynettools.sh -u

# PyNetTools /etc/host backup recycler
sh recycle_hosts_bkp.sh
```

4. Include it in the crontab to refresh the host file constantly

```bash
crontab -e
```

Add the instructions in the `crontab-example.txt` file.


## Contributions

Feel free to submit pull requests, create issues or spread the word.

## License

MIT
