#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Copyright 2016 graypawn <choi.pawn@gmail.com>
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

from Registry import Registry


def getGUIDs(filename):
    """
    Args:
    - filename (string): software registry of Windows OS.
    Returns:
    - list of string: a list of Network Adapter GUIDs.
    """
    software = Registry.Registry(filename)
    networkcards =  software.open(
        "Microsoft\\Windows NT\\CurrentVersion\\NetworkCards")
    guids = [x.value("ServiceName").value() for x in networkcards.subkeys()]
    return guids


class Interface:
    """
    a class for network interface.
    Args:
    - data: a RegistryKey as a subkey of interfaces.
    """
    def __init__(self, data):
        self.data = data

    def printItems(self):
        """
        Print a interface.
        """
        pass


class InterfaceValue:
    """
    A class for values of Interface.
    Args:
    - value: a interface value as a RegistryValue.
    """
    def __init__(self, value):
        self._value = value

    def __str__(self):
        return ", ".join(filter(lambda x: x, self._value.value()))


class StaticInterface(Interface):
    """
    A class for static network interface.
    """
    enable_dhcp = False

    def value(self, name):
        """
        Return a value with a given name as a InterfaceValue.
        """
        value_wrap = self.data.value(name)
        if value_wrap.value_type() is 7:
            return InterfaceValue(value_wrap)
        else:
            return value_wrap.value()

    def printItems(self):
        print("IP Address: %s" % self.value("IPAddress"))
        print("Subnet Mask: %s" % self.value("SubnetMask"))
        print("Gateway: %s" % self.value("DefaultGateway"))
        print("Name Server: %s" % self.value("NameServer"))


class DanamicInterface(Interface):
    """
    A class for DHCP network interface.
    """
    enable_dhcp = True

    def printItems(self):
        print("IP Adress: DHCP")


class Interfaces:
    """
    A class for a network interfaces.
    Args:
    - directory(string): the directory path included Windows registrys.
    """
    def __init__(self, directory):
        self.path = directory
        self.guids = getGUIDs(directory + "/SOFTWARE")

    def _values(self):
        """
        Return a RegistryKey of interfaces.
        """
        system = Registry.Registry(self.path + "/SYSTEM")
        select = system.open("Select")
        current = select.value("Current").value()
        return system.open(
            "ControlSet00%d\Services\Tcpip\Parameters\Interfaces" % (current))

    def getInterface(self, guid):
        """
        Return a Interface with a given GUID.
        You can get a GUID from the self.guids.
        """
        interface_data = self.values().subkey(guid)
        if interface_data.value("EnableDHCP").value() is 1:
            return DanamicInterface(interface_data)
        else:
            return StaticInterface(interface_data)

    def printAll(self):
        """
        Print All Interfaces.
        """
        print()
        for guid in self.guids:
            self.getInterface(guid).printItems()
            print()
