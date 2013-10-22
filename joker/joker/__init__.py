from nodes import NodesDict,Node
#from os import remove
import os

PETYA_ENV_KEY = "-----BEGIN RSA PRIVATE KEY-----\n\
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

#TMP_PATH="/tmp/%s"

class Joker():

    def __init__(self, key = PETYA_ENV_KEY, *args, **kwargs):
         
        self.default_key = key

        self.nodes = NodesDict()
        self.keyPath = None
        self.name = "EntryPoint"
        #self.setKey()  

    

#    def __del__(self):
#        if (self.keyPath): 
#            # look at this.
#            # epic security hole oneliner
#            print "os.remove(self.keyPath)"

    def addNode(self, name, host, port, user):
        self.entryPoint = Node(name, host, port);
        self.entryPoint.assignCredential(user, self.default_key, None) 
        return

    def genStub(self, hostname, ip, port, user, key, proxycommand):
        return {"name": hostname, "ip": ip, "user": user,
                "key": key, "port": port, 
                "proxy_command": proxycommand
                } 

    def discover(self):
        result = []
        discoveryData = self.entryPoint.discovery() 


        for node in discoveryData:
            result.append(self.genStub(discoveryData[node], discoveryData[node], self.default_key , "vagrant", None, "ssh -i " + "%%PATH_TO_KEY%%" + " -p " + str(self.entryPoint.accessPort) + "  -q " + self.entryPoint.user  + "@" + self.entryPoint.hostName + " nc -q0 " + discoveryData[node] + " 22")) 

        return result

joker = Joker(PETYA_ENV_KEY) 
joker.addNode("controller1", "172.18.66.112", 2301, "vagrant");
print joker.discover() 
