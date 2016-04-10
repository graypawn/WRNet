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

class Interface:
    def __init__(self, directory):
        software = Registry.Registry(directory + "/SOFTWARE")
        networkcards =  software.open(
            "Microsoft\\Windows NT\\CurrentVersion\\NetworkCards")

        ## Warring : networkcard가 한 개라 가정해고 있다.
        guid = networkcards.subkeys()[0].value("ServiceName").value()

        system = Registry.Registry(directory + "/SYSTEM")
        select = system.open("Select")
        current = select.value("Current").value()
        self.__subkeys = system.open(
            "ControlSet00%d\Services\Tcpip\Parameters\Interfaces\%s"
            % (current, guid))

    def value(self, name):
        try:
            return self.__subkeys.value(name).value()[0]
        except IndexError:
            return self.__subkeys.value(name).value()
        except Registry.RegistryValueNotFoundException:
            pass
        except Registry.RegistryParse.RegistryStructureDoesNotExist:
            pass

    def print_all(self):
        print("IPAddress: %s" % self.value("IPAddress"))
        print("Subnet Mask: %s" % self.value("SubnetMask"))
        print("Gateway: %s" % self.value("DefaultGateway"))
        print("Name Server: %s" % self.value("NameServer"))
