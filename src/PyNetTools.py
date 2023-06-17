import sys
import platform
import socket
import subprocess

from src.Platform import Platform
from src.Host import Host
from src.init_parser import init_parser


class PyNetTools:

    def __init__(self, keepingHistory=True):
        self.platform = Platform()
        self.host = Host(keepingHistory)
        self.parser = init_parser(self.host.hostFile)
        self.args = self.parser.parse_args()
        self.input_file = self.args.input
        self.debug = self.args.debug == '1'
        self.mappings = {}

    def std_response(self):
        return {
            'error': False,
            'error_msg': '',
            'output': '',
        }

    def cmd_execution(self, cmd):
        response = self.std_response()
        if self.debug:
            print(f'Running command: {cmd} ...')
        try:
            response['output'] = subprocess.check_output(
                (cmd),
                shell=True,
                stderr=subprocess.STDOUT
            )
        except Exception as err:
            response['error'] = True
            response['error_msg'] = str(err)
        return response

    def get_start_ip(self, ip):
        ip_split = ip.split('.')
        return f'{ip_split[0]}.{ip_split[1]}.{ip_split[2]}.0'

    def get_local_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            # doesn't even have to be reachable
            s.connect(('192.255.255.255', 1))
            ip = s.getsockname()[0]
        except Exception:
            ip = '127.0.0.1'
        finally:
            s.close()
        return ip

    def run_nmap(self):
        response = self.std_response()
        local_ip = self.get_local_ip()
        if self.debug:
            print(f'Platform: {self.platform.name()}')
            print(F'Own IP: {local_ip}')
        start_ip_for_nmap = self.get_start_ip(local_ip)
        cmd = f'nmap -v -sn {start_ip_for_nmap}/24'
        cmd_response = self.cmd_execution(cmd)
        if cmd_response['error']:
            response['error'] = True
            response['error_msg'] = f"ERROR: {cmd_response['error_msg']}"
        else:
            response['output'] = cmd_response['output']
        return response

    def get_ip_from_mac(self, mac_addr):
        response = self.std_response()
        if not mac_addr:
            response['error'] = True
            response['error_msg'] = "ERROR: mac address must be specified"
            return response

        cmd = f'arp -a | grep "{mac_addr}" '
        if self.platform.is_mac():
            mac_addr = mac_addr.replace(':0', ":").lower()
            cmd = f'arp -a | grep "{mac_addr}" '
        cmd_response = self.cmd_execution(cmd)
        if cmd_response['error']:
            response['error'] = True
            response['error_msg'] = f"ERROR: {cmd_response['error_msg']}"
            return response

        returned_output = cmd_response['output']
        if self.debug:
            print(returned_output)

        parse = str(returned_output).split(' ', 1)
        if self.platform.is_mac():
            ip = parse[1].split('(')[1].split(')')[0]
            result = ip
        else:
            ip = parse[1].split(' ')
            result = ip[1]

        if result:
            response['output'] = result
        else:
            response['error'] = True
            response['error_msg'] = f'MAC address {mac_addr} does not exist'
        return response

    def _get_input_file_lines(self):
        try:
            with open(self.input_file, 'r') as input:
                lines = input.readlines()
                return lines
        except Exception as err:
            print(f'ERROR: could not read file: {self.input_file}')
            print(str(err))
            return None

    def populate_input_entries(self):
        lines = self._get_input_file_lines()
        if not lines:
            print(f'Cannot read file {self.input_file}')
            return

        if self.args.run_nmap == '1':
            nmap_result = self.run_nmap()
            if nmap_result['error']:
                print(nmap_result['error_msg'])
                return

        for line in lines:
            segment = line.split()
            if line.startswith('#') or line == '\n':
                continue
            if len(segment) != 2:
                continue
            mac_addr = segment[0]
            hostname = segment[1]
            ip_response = self.get_ip_from_mac(mac_addr)
            error = False
            error_msg = None
            ip = ip_response['output']
            if ip_response['error']:
                error = True
                error_msg = ip_response['error_msg']
            self.mappings[hostname] = {
                'hostname': hostname,
                'mac_addr': mac_addr,
                'ip': ip,
                'error': error,
                'error_msg': error_msg,
            }
            if self.debug:
                print(
                    f'Host: {hostname}, MAC address: {mac_addr}, ' +
                    f'ERROR: {error_msg}' if error
                    else f'IP: {ip}'
                )
        return

    def print_all(*a_list):
        for each in a_list:
            print(each)

    def list_input_entries(self):
        if len(self.mappings) == 0:
            self.populate_input_entries()
        for hostname, item in self.mappings.items():
            print(
                f"Host: {hostname}, " +
                f"MAC address: {item['mac_addr']}, " +
                (f"{item['error_msg']}" if item['error']
                 else f"IP: {item['ip']}")
            )

    def update_from_input_entries(self):
        if len(self.mappings) == 0:
            self.populate_input_entries()
        self.host.update(self.mappings)

    def main(self):
        if self.args.list:
            self.list_input_entries()
        elif self.args.update:
            self.update_from_input_entries()
        elif self.args.show:
            content = self.host.list()
            self.print_all(*content)
        elif self.args.check:
            self.print_all('# Search result:')
            result = self.host.check(*self.args.check)
            self.print_all(*result)
        elif self.args.insert:
            self.print_all('# Insert mapping:')
            for each in self.args.insert:
                arg = each.split(':')
                result = self.host.add(*arg)
                if result[0]:
                    self.print_all(
                        '> inserted ' + each + ', backup file: ' + result[1]
                    )
                else:
                    self.print_all('> failed to insert ' + each)
        elif self.args.remove:
            self.print_all('# Remove mapping:')
            for each in self.args.remove:
                result = self.host.remove(each)
                if result[0]:
                    self.print_all('## removed ' + each + ', backup file: ' + result[1])
                else:
                    self.print_all('## Not found ' + each)
        else:
            self.parser.print_help()
