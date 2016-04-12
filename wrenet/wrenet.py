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
    "SOFTWARE Registry을 filename으로 받는다."
    software = Registry.Registry(filename)
    networkcards =  software.open(
        "Microsoft\\Windows NT\\CurrentVersion\\NetworkCards")
    guids = list(map(lambda x: x.value("ServiceName").value(),
                     networkcards.subkeys()))
    return guids


class Interface:
    def __init__(self, data):
        self.data = data

    def printItems(self):
        pass


class StaticInterface(Interface):
    enable_dhcp = False

    def value(self, name):
        value_wrap = Interface.data.value(name)
        if value_wrap.value_type() is 7:
            return value_wrap.value()[0]
        else:
            return value_wrap.value()

    def printItems(self):
        print("IP Address: %s" % self.value("IPAddress"))
        print("Subnet Mask: %s" % self.value("SubnetMask"))
        print("Gateway: %s" % self.value("DefaultGateway"))
        print("Name Server: %s" % self.value("NameServer"))


class DanamicInterface(Interface):
    enable_dhcp = True

    def printItems(self):
        print("IP Adress: DHCP")


class Interfaces:
    def __init__(self, directory):
        self.path = directory
        self.guids = getGUIDs(directory + "/SOFTWARE")

    def values(self):
        system = Registry.Registry(self.path + "/SYSTEM")
        select = system.open("Select")
        current = select.value("Current").value()
        return system.open(
            "ControlSet00%d\Services\Tcpip\Parameters\Interfaces" % (current))

    def getInterface(self, guid):
        interface_data = self.values().subkey(guid)
        if interface_data.value("EnableDHCP").value() is 1:
            return DanamicInterface(interface_data)
        else:
            return StaticInterface(interface_data)

    def printAll(self):
        print()
        for guid in self.guids:
            self.getInterface(guid).printItems()
            print()
