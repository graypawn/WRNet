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
        self.check = (True if self.data.values() else False)

        if self.check:
            if self.data.value("EnableDHCP").value() is 1:
                self.enable_dhcp = True
            else:
                self.enable_dhcp = False

    def value(self, name):
        if self.check:
            if not self.enable_dhcp:
                value_wrap = self.data.value(name)
                if value_wrap.value_type() is 7:
                    return value_wrap.value()[0]
                else:
                    return value_wrap.value()
            else:
                return None
        else:
            return None

    def printItems(self):
        if self.enable_dhcp:
            print("IPAdress: DHCP")
        else:
            print("IPAddress: %s" % self.value("IPAddress"))
            print("Subnet Mask: %s" % self.value("SubnetMask"))
            print("Gateway: %s" % self.value("DefaultGateway"))
            print("Name Server: %s" % self.value("NameServer"))


class Interfaces:
    def __init__(self, directory):
        system = Registry.Registry(directory + "/SYSTEM")
        select = system.open("Select")
        current = select.value("Current").value()
        self.path = directory
        self.interfaces = system.open(
            "ControlSet00%d\Services\Tcpip\Parameters\Interfaces" % (current))
        self.guids = getGUIDs(directory + "/SOFTWARE")

    def getInterface(self, guid):
        return Interface(self.interfaces.subkey(guid))

    def printAll(self):
        print()
        for guid in self.guids:
            self.getInterface(guid).printItems()
            print()
