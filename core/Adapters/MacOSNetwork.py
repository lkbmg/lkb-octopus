#!/usr/bin/env python3
'''
common.py
Written by pollardm
Written: 11/11/24
Description: Base Classes for macOS Local Settings
'''

from core.MacOSExecutor import Executor

class NetworkSetup:
    def __init__(self):
        """Initialize Executor with the default binary path for networksetup."""
        self.networksetup = Executor('/usr/sbin/networksetup')

    def list_network_service_order(self, debug=False):
        """Displays a list of network services"""
        output = self.networksetup.execute("-listnetworkserviceorder", debug=debug)
        return output.decode('utf-8').strip()

    def list_all_network_services(self, debug=False):
        """Displays a list of all the network services"""
        output = self.networksetup.execute("-listallnetworkservices", debug=debug)
        return output.decode('utf-8').strip()
    
    def list_all_hardware_reports(self, debug=False):
        """Displays list of hardware ports"""
        output = self.networksetup.execute("-listallhardwareports", debug=debug)
        return output.decode('utf-8').strip()

    def detect_new_hardware(self, debug=False):
        """Detects new network hardware and creates a default network service"""
        output = self.networksetup.execute("-detectnewhardware", debug=debug)
        return output.decode('utf-8').strip()
    
    def get_mac_address(self, hardware_port, debug=False):
        """Retrieves MAC address for a specific hardware port"""
        output = self.networksetup.execute("-getmacaddress", hardware_port, debug=debug)
        return output.decode('utf-8').strip()

    def get_dns_servers(self, network_service, debug=False):
        """Gets DNS servers for a network service"""
        output = self.networksetup.execute("-getdnsservers", network_service, debug=debug)
        return output.decode('utf-8').strip()

    def set_dns_servers(self, network_service, *dns_servers, debug=False):
        """Sets DNS servers for a network service"""
        output = self.networksetup.execute("-setdnsservers", network_service, *dns_servers, debug=debug)
        return output.decode('utf-8').strip()

    def get_search_domains(self, network_service, debug=False):
        """Gets search domains for a network service"""
        output = self.networksetup.execute("-getsearchdomains", network_service, debug=debug)
        return output.decode('utf-8').strip()

    def set_search_domains(self, network_service, *domains, debug=False):
        """Sets search domains for a network service"""
        output = self.networksetup.execute("-setsearchdomains", network_service, *domains, debug=debug)
        return output.decode('utf-8').strip()

    def get_network_service_enabled(self, network_service, debug=False):
        """Checks if a network service is enabled"""
        output = self.networksetup.execute("-getnetworkserviceenabled", network_service, debug=debug)
        return output.decode('utf-8').strip()

    def set_network_service_enabled(self, network_service, enable=True, debug=False):
        """Enables or disables a network service"""
        state = "on" if enable else "off"
        output = self.networksetup.execute("-setnetworkserviceenabled", network_service, state, debug=debug)
        return output.decode('utf-8').strip()

    def get_current_location(self, debug=False):
        """Gets the current network location"""
        output = self.networksetup.execute("-getcurrentlocation", debug=debug)
        return output.decode('utf-8').strip()

    def create_location(self, location, debug=False):
        """Switches to a specified network location"""
        output = self.networksetup.execute("-createlocation", location, debug=debug)
        return output.decode('utf-8').strip()

    def switch_to_location(self, location, debug=False):
        """Switches to a specified network location"""
        output = self.networksetup.execute("-switchtolocation", location, debug=debug)
        return output.decode('utf-8').strip()

    def get_mtu(self, hardware_port, debug=False):
        """Gets the MTU for a specified hardware port"""
        output = self.networksetup.execute("-getMTU", hardware_port, debug=debug)
        return output.decode('utf-8').strip()

    def set_mtu(self, hardware_port, value, debug=False):
        """Sets the MTU for a specified hardware port"""
        output = self.networksetup.execute("-setMTU", hardware_port, value, debug=debug)
        return output.decode('utf-8').strip()

    def list_valid_mtu_range(self, hardware_port, debug=False):
        """Lists the valid MTU range for a specified hardware port"""
        output = self.networksetup.execute("-listvalidMTUrange", hardware_port, debug=debug)
        return output.decode('utf-8').strip()
 