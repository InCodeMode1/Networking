
class Subnet:
    """ Finds Network, Broadcast Address, Subnet and Wildcard mask, and usable host range, possible subnets and range"""
    def __init__(self, ip, cidr):
        self.ip = ip.split('.')
        self.cidr = cidr

        if int(self.ip[0]) in range(128):
            self.ip_class = 'A'
        elif int(self.ip[0]) in range(128, 192):
            self.ip_class = 'B'
        elif int(self.ip[0]) in range(192, 224):
            self.ip_class = 'C'

    def set_new_ip(self, ip, cidr):
        self.ip = ip.split('.')
        self.cidr = cidr

    def find_network_address(self):
        address = ''
        for index, octet in enumerate(self.ip):
            address += str(int(octet) & int(self.__cidr_to_bin__()[index], 2)) + '.'
        return address[:-1]

    def __cidr_to_bin__(self, cidr=-1, inverted=False):
        if cidr < 0:
            cidr = self.cidr
        ddn = []
        if not inverted:
            while cidr // 8 != 0:
                cidr -= 8
                ddn.append('1' * 8)
            if cidr > 0:
                ddn.append((cidr * '1') + (abs(cidr - 8) * '0'))
            while len(ddn) < 4:
                ddn.append('0' * 8)
        else:
            cidr = 32 - cidr
            while cidr // 8 != 0:
                cidr -= 8
                ddn.insert(0, ('1' * 8))
            if cidr > 0:
                ddn.insert(0, ((8 - cidr) * '0') + (cidr * '1'))
            while len(ddn) < 4:
                ddn.insert(0, ('0' * 8))
        return ddn

    def usable_hosts(self):
        return pow(2, (32 - self.cidr)) - 2

    def possible_subnets(self):
        if self.ip_class == 'A':
            return pow(2, abs(8 - self.cidr))
        elif self.ip_class == 'B':
            return pow(2, abs(16 - self.cidr))
        elif self.ip_class == 'C':
            return pow(2, abs(24 - self.cidr))

    # Bugged, works only for Class C addresses
    def possible_subnet_range(self):
        ip = Subnet('.'.join(self.ip), self.cidr)
        for _current in range(self.possible_subnets()):
            print('=' * 25)
            print('Network Address: ' + ip.find_network_address())
            print(ip.usable_host_range())
            print('Broadcast Address: ' + ip.find_broadcast())
            ip.ip[3] = str(int(ip.ip[3]) + ip.usable_hosts() + 2)

    def find_broadcast(self):
        address = ''
        for index, octet in enumerate(self.__cidr_to_bin__(self.cidr, True)):
            address += str(int(octet, 2) | int(self.find_network_address().split('.')[index])) + '.'
        return address[:-1]

    def usable_host_range(self):
        network = self.find_network_address().split('.')
        broadcast = self.find_broadcast().split('.')
        network[3] = str(int(network[3]) + 1)
        broadcast[3] = str(int(broadcast[3]) - 1)
        return 'Usable Host range: ' + '.'.join(network) + ' - ' + '.'.join(broadcast) if self.cidr < 31 else \
            'No usable host range'

    def subnet_mask(self):
        return '.'.join(str(int(octet, 2)) for octet in self.__cidr_to_bin__())

    def wild_card_mask(self):
        return '.'.join(str(int(octet, 2)) for octet in self.__cidr_to_bin__(self.cidr, True))

    def show_all(self):
        print('IP Address: ' + '.'.join(self.ip) + '/' + str(self.cidr))
        print('Class: ' + self.ip_class)
        print("Network Address: " + self.find_network_address())
        print('Broadcast Address: ' + self.find_broadcast())
        print(self.usable_host_range())
        print("No. of Usable Hosts: " + str(self.usable_hosts()))
        print("No. of possible subnets: " + str(self.possible_subnets()))
        print("Subnet Mask: " + self.subnet_mask())
        print("Wildcard Mask: " + self.wild_card_mask())
        # self.possible_subnet_range()
