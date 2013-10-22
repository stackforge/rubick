import collections
import paramiko


class TransformedDict(collections.MutableMapping):

    def __init__(self, *args, **kwargs):
        self.store = dict()
        self.update(dict(*args, **kwargs))  # use the free update to set keys

    def __getitem__(self, key):
        return self.store[self.__keytransform__(key)]

    def __setitem__(self, key, value):
        self.store[self.__keytransform__(key)] = value

    def __delitem__(self, key):
        del self.store[self.__keytransform__(key)]

    def __iter__(self):
        return iter(self.store)

    def __len__(self):
        return len(self.store)

    def __keytransform__(self, key):
        return key


class NodesDict(TransformedDict):

    def add(self, element):
        return self.__setitem__(element, element)

    def __keytransform__(self, key):
        try:
            # now uniq for hash is only hwaddr key
            # print 'hwaddr = ' + key['hwaddr']
            return key['hwaddr']
        except KeyError:
            raise


class Node():

    def __init__(self, name, ip):

        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.setHostName(ip)
        self.setName(name)
        self.connected = False

        self.neighbours = NodesDict() 

    def prepare(self):
        self.runCommand(
            "[ ! -x arp-scan ] && sudo apt-get --force-yes install arp-scan")
        # install arp-scan on node
        return True

    def infect(self):
        # infect node
        return True

    def setName(self, name):
        self.name = name

    def setHostName(self, hostname):
        self.hostName = hostname

    def setAccessPort(self, port):
        self.accessPort = port

    def assignCredential(self, user, password, key):
        self.user = user
        self.password = password
        self.key = key

    def setProxyCommand(self, proxyCommand):
        self.proxyCommand = proxyCommand

    def connect(self):
        if self.connected is True:
            raise assertionError(self.connected is True)
        try:
            self.ssh.connect(self.hostName, self.accessPort, self.user,
                             key_filename=self.key)
            self.connected = True
            return True
        except paramiko.BadHostKeyException, e:
            print "Host key could not be verified: ", e
            return False
        except paramiko.AuthenticationException, e:
            print "Error unable to authenticate: ", e
            return False
        except paramiko.SSHException, e:
            print e
            return False

    def runCommand(self, command):
        if (command == ""):
            assertionError(command == "")

        if (self.connected is False):
            self.connect()

        stdin, stdout, stderr = self.ssh.exec_command(command)

        return (stdout.readlines(), stderr.readlines()) 

    def discovery(self):
        self.prepare()

        (self.discovery_data, _) = self.runCommand(
            "ip link | awk -F: '/^[0-9]+?: / {print $2}' |\
            sudo xargs -I% arp-scan -l -I % 2>&1 | grep -E '^[0-9]+?\.'")

        for node in self.discovery_data:
            ( node['ip'], node['hwAddr'] ) = node.split("\t")
        
        return True

          
        # ssh -p2301 -i /home/ryabin/.vagrant.d/insecure_private_key
        # vagrant@127.0.0.1 " link | grep -B1 link/ether | awk -F: '/^[0-9]+?:
        # / {print \$2}' | sudo xargs -I% arp-scan -l -I % 2>&1 | grep -E
        # '^[0-9]+?\.'

n = Node("controller", "127.0.0.1")
n.assignCredential(
    "vagrant", None, "/home/ryabin/.vagrant.d/insecure_private_key")
n.setAccessPort(2301)

n.discovery()
print n.discovery_data
