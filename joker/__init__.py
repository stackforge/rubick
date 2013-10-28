from nodes import Node
import os

DEFAULT_KEY = "-----BEGIN RSA PRIVATE KEY-----\n\
MIIEogIBAAKCAQEA6NF8iallvQVp22WDkTkyrtvp9eWW6A8YVr+kz4TjGYe7gHzI\n\
w+niNltGEFHzD8+v1I2YJ6oXevct1YeS0o9HZyN1Q9qgCgzUFtdOKLv6IedplqoP\n\
kcmF0aYet2PkEDo3MlTBckFXPITAMzF8dJSIFo9D8HfdOV0IAdx4O7PtixWKn5y2\n\
hMNG0zQPyUecp4pzC6kivAIhyfHilFR61RGL+GPXQ2MWZWFYbAGjyiYJnAmCP3NO\n\
Td0jMZEnDkbUvxhMmBYSdETk1rRgm+R4LOzFUGaHqHDLKLX+FIPKcF96hrucXzcW\n\
yLbIbEgE98OHlnVYCzRdK8jlqm8tehUc9c9WhQIBIwKCAQEA4iqWPJXtzZA68mKd\n\
ELs4jJsdyky+ewdZeNds5tjcnHU5zUYE25K+ffJED9qUWICcLZDc81TGWjHyAqD1\n\
Bw7XpgUwFgeUJwUlzQurAv+/ySnxiwuaGJfhFM1CaQHzfXphgVml+fZUvnJUTvzf\n\
TK2Lg6EdbUE9TarUlBf/xPfuEhMSlIE5keb/Zz3/LUlRg8yDqz5w+QWVJ4utnKnK\n\
iqwZN0mwpwU7YSyJhlT4YV1F3n4YjLswM5wJs2oqm0jssQu/BT0tyEXNDYBLEF4A\n\
sClaWuSJ2kjq7KhrrYXzagqhnSei9ODYFShJu8UWVec3Ihb5ZXlzO6vdNQ1J9Xsf\n\
4m+2ywKBgQD6qFxx/Rv9CNN96l/4rb14HKirC2o/orApiHmHDsURs5rUKDx0f9iP\n\
cXN7S1uePXuJRK/5hsubaOCx3Owd2u9gD6Oq0CsMkE4CUSiJcYrMANtx54cGH7Rk\n\
EjFZxK8xAv1ldELEyxrFqkbE4BKd8QOt414qjvTGyAK+OLD3M2QdCQKBgQDtx8pN\n\
CAxR7yhHbIWT1AH66+XWN8bXq7l3RO/ukeaci98JfkbkxURZhtxV/HHuvUhnPLdX\n\
3TwygPBYZFNo4pzVEhzWoTtnEtrFueKxyc3+LjZpuo+mBlQ6ORtfgkr9gBVphXZG\n\
YEzkCD3lVdl8L4cw9BVpKrJCs1c5taGjDgdInQKBgHm/fVvv96bJxc9x1tffXAcj\n\
3OVdUN0UgXNCSaf/3A/phbeBQe9xS+3mpc4r6qvx+iy69mNBeNZ0xOitIjpjBo2+\n\
dBEjSBwLk5q5tJqHmy/jKMJL4n9ROlx93XS+njxgibTvU6Fp9w+NOFD/HvxB3Tcz\n\
6+jJF85D5BNAG3DBMKBjAoGBAOAxZvgsKN+JuENXsST7F89Tck2iTcQIT8g5rwWC\n\
P9Vt74yboe2kDT531w8+egz7nAmRBKNM751U/95P9t88EDacDI/Z2OwnuFQHCPDF\n\
llYOUI+SpLJ6/vURRbHSnnn8a/XG+nzedGH5JGqEJNQsz+xT2axM0/W/CRknmGaJ\n\
kda/AoGANWrLCz708y7VYgAtW2Uf1DPOIYMdvo6fxIB5i9ZfISgcJ/bbCUkFrhoH\n\
+vq/5CIWxCPp0f85R4qxxQ5ihxJ0YDQT9Jpx4TMss4PSavPaBH3RXow5Ohe+bYoQ\n\
NE5OgEXk2wVfZczCZpigBKbKZHNYcelXtTt/nP3rsCuGcM4h53s=\n\
-----END RSA PRIVATE KEY-----"

TMP_PATH = "/tmp/joker_%s_%d"


class Joker():

    def __init__(self, key=DEFAULT_KEY, *args, **kwargs):

        self.default_key = key

        self.discoverQueue = []
        self.discoveryResult = []
        self.cleanUp = []
        self.name = "EntryPoint"
        self.seenNodes = {}

        # keys temporary files

    def __del__(self):
        for filePath in self.cleanUp:
            if os.path.exists(filePath):
                os.remove(filePath)

    def addNode(self, name, host, user, port=22):

        node = Node(name, host, port)
        node.assignCredential(user, self.default_key, None)

        self.discoverQueue.append(node)

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
        result = {}

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
