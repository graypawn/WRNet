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


import sys
from Registry import Registry

def usage():
    return "  USAGE: \n\t%s <Windows Mount Point>" % sys.argv[0]


def rec(path):
    registry = Registry.Registry(path)
    select = registry.open("Select")
    current = select.value("Current").value()
    services = registry.open("ControlSet00%d\Services" % (current))
    interfaces = services.find_key("Tcpip\Parameters\Interfaces")
    for interface in interfaces.subkeys():
        try:
            ip_address = interface.value("IPAddress").value()[0]
        except:
            ip_address = "???"

        try:
            subnet_mask = interface.value("SubnetMask").value()[0]
        except:
            subnet_mask = "???"

        try:
            gateway = interface.value("DefaultGateway").value()
        except:
            gateway = "???"

        try:
            gateway = interface.value("DefaultGateway").value()
        except:
            gateway = "???"

        try:
            name_server = interface.value("NameServer").value()
        except:
            name_server = "???"

        print("""
    IP Address %s
    Subnet Mask %s
    Gateway %s
    Name Server %s
    """ % (ip_address, subnet_mask, gateway, name_server))


def main():
    system_path = "/Windows/System32/config/SYSTEM"
    if len(sys.argv) != 2:
        print(usage())
        sys.exit(-1)
    rec(sys.argv[1] + system_path)


if __name__ == "__main__":
    main()
