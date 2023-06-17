import datetime
from shutil import copyfile
from src.Platform import Platform


# Reference:
# https://github.com/qszhuan/hostsman


class Host:
    def __init__(self, keepingHistory=True):
        platform = Platform()
        self.platform = platform
        if platform.is_linux() or platform.is_mac():
            self.hostFile = "/etc/hosts"
        elif platform.is_windows():
            self.hostFile = 'c:\\windows\\system32\\drivers\\etc\\hosts'
        else:
            self.hostFile = '/etc/hosts'
        self.keepingHistory = keepingHistory

    def list(self):
        with open(self.hostFile, 'r') as f:
            return [line.strip() for line in f]

    def _should_split_row(self, hostnames):
        return self.platform.is_windows() and len(hostnames) >= 9

    def update(self, mappings: dict):
        mappings = {k: {'new': True, **v} for (k, v) in mappings.items()}
        backupfile = self._keep_history()
        lines = self._get_host_file_lines()
        with open(self.hostFile, 'w') as output:
            for line in lines:
                if line.startswith('#') or line == '\n':
                    output.write(line.strip() + '\n')
                    continue
                segment = line.split()
                leave_as_is = True
                if segment[1] in mappings:
                    if not mappings[segment[1]]['error']:
                        leave_as_is = False
                        mappings[segment[1]]['new'] = False
                        output.write(mappings[segment[1]]['ip'])
                        output.write('\t')
                        output.write(' '.join(segment[1:]))
                        output.write('\n')
                    else:
                        print(f"Could not add host '{segment[1]}' " +
                              f"because: {mappings[segment[1]]['error_msg']}")
                if leave_as_is:
                    output.write(segment[0])
                    output.write('\t')
                    output.write(' '.join(segment[1:]))
                    output.write('\n')

            def add_new_hosts(item):
                if item['new']:
                    if not item['error']:
                        output.write(item['ip'])
                        output.write('\t')
                        output.write(item['hostname'])
                        output.write('\n')
                        return "Entry created: " + \
                               f"{item['ip']} {item['hostname']}"
                    else:
                        return "Entry has an error: " + \
                               f"{item['ip']} {item['hostname']} " + \
                               f"-> {item['error_msg']}"
                return f"Entry exist: {item['ip']} {item['hostname']}"

            value = list(map(lambda x: add_new_hosts(x[1]), mappings.items()))
            print(value)

        return True, backupfile

    def add(self, hostname, ip='127.0.0.1'):
        if self.exists(hostname, ip):
            return False, None
        added = False
        backupfile = self._keep_history()
        lines = self._get_host_file_lines()
        with open(self.hostFile, 'w') as output:
            for line in lines:
                if line.startswith('#') or line == '\n':
                    output.write(line.strip() + '\n')
                else:
                    segment = line.split()
                    if ip == segment[0] and \
                       not self._should_split_row(segment[1:]) and \
                       not added:
                        segment.append(hostname)
                        added = True
                    output.write(segment[0])
                    output.write('\t')
                    output.write(' '.join(segment[1:]))
                    output.write('\n')
            if not added:
                output.write(ip)
                output.write('\t')
                output.write(hostname)
                output.write('\n')
        return True, backupfile

    def remove(self, hostname):
        if not self.exists(hostname):
            return False, None
        backup_file = self._keep_history()
        found = False
        lines = self._get_host_file_lines()
        with open(self.hostFile, 'w') as output:
            for line in lines:
                segment = line.split()
                if line.startswith('#') or line == '\n':
                    output.write(line)
                elif len(segment) == 2 and hostname == segment[1]:
                    found = True
                    continue
                elif len(segment) >= 2 and hostname in segment[1:]:
                    found = True
                    segment.remove(hostname)
                    output.write(segment[0])
                    output.write('\t')
                    output.write(' '.join(segment[1:]))
                    output.write('\n')
                else:
                    output.write(line)
        return found, backup_file

    def exists(self, hostname, ip=None):
        with open(self.hostFile, 'r') as f:
            for line in list(f):
                segment = line.split()
                if line.startswith('#') or line == '\n':
                    continue
                if hostname in segment[1:] and \
                   (ip is None or ip == segment[0]):
                    return True
            else:
                return False

    def _get_host_file_lines(self):
        with open(self.hostFile, 'r') as input:
            lines = input.readlines()
            return lines

    def check(self, *host_names):
        result = []
        with open(self.hostFile, 'r') as f:
            for line in list(f):
                if line.startswith('#') or line == '\n':
                    continue
                if len([x for x in line.split()[1:] if x in host_names]):
                    result.append(line.strip())

            return result

    def location(self):
        return self.hostFile

    def _keep_history(self):
        if self.keepingHistory:
            now = datetime.datetime.now()
            backup_file = self.hostFile + now.strftime("-%Y.%m.%d_%H-%M-%S-%f")
            copyfile(self.hostFile, backup_file)
            return backup_file
        return None
