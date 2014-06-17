# Copyright (c) 2014 Mirantis Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and#
# limitations under the License.
from nodes import Node
import os

TMP_PATH = "/tmp/joker_%s_%d"


class Joker():

    def __init__(self, default_key, *args, **kwargs):

        self.useKey = False

        self.discoverQueue = []
        self.discoveryResult = []
        self.cleanUp = []
        self.name = "EntryPoint"
        self.seenNodes = {}
        self.default_key = None

        if (default_key):
            try:
                with open(default_key) as f:
                    self.default_key = f.read()
            except Exception:
                self.default_key = default_key

            self.useKey = True

    # keys temporary files

    def __del__(self):
        for filePath in self.cleanUp:
            if os.path.exists(filePath):
                os.remove(filePath)

    def addNode(self, name, host, port=22, user='root', password=None):

        node = Node(name, host, port)
        node.assignCredential(user, self.default_key, password)

        self.discoverQueue.append(node)

        if (self.useKey):
            self.cleanUp.append(node.keyPath)

        return node

    def addResult(self, hostname, ip, user, key, proxyCommand=None, port=22):
        return self.discoveryResult.append(
            self.dkOutput(hostname, ip, user, key, proxyCommand, port))

    def dkOutput(self, hostname, ip, user, key, proxyCommand=None, port=22):
        return {
            "name": hostname,
            "ip": ip,
            "user": user,
            "key": key,
            "port": port,
            "proxy_command": proxyCommand
        }

    def discover(self):

        while self.discoverQueue:
            point = self.discoverQueue.pop()

            nodes = point.discover()

            # this host can't be discovered by ssh method
            if nodes is None:
                continue

            self.addResult(
                hostname=point.hostName, ip=point.hostName, user=point.user,
                key=point.origKey, proxyCommand=point.proxyCommandTxt,
                port=point.accessPort)

            # merge already seen nodes with new discovered nodes
            self.seenNodes = dict(self.seenNodes.items() + point.link.items())

            for node in nodes:
                if node['hwAddr'] not in self.seenNodes:
                    # add to discovering queue
                    newNode = self.addNode(
                        name=node['ip'],
                        host=node['ip'],
                        user=point.user)

                    # new node connection channel working through master node
                    newNode.setProxyCommand(
                        point.hostName,
                        point.accessPort,
                        point.user,
                        point.keyPath
                    )

        return self.discoveryResult
