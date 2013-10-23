import collections
import paramiko

from paramiko.rsakey import RSAKey
from StringIO import StringIO


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

    def __init__(self, name, ip, port):

        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.setHostName(ip)
        self.setName(name)
        self.setAccessPort(port)
        self.connected = False

        #self.neighbours = NodesDict()
        self.neighbours = {}
        self.debug = True

        self.hwAddr = None

    def discoveryHwAddr(self):
        try:
            (stdout, stderr) = self.runCommand("ip link | grep -m1 -A1 "
                                               "BROADCAST,MULTICAST,UP,"
                                               "LOWER_UP | awk -F\" \" "
                                               "'/link/ {print $2}'");
        except:
            raise()
        return stdout[0].strip()

    def setUniqData(self):
        self.hwAddr = self.discoveryHwAddr()

    def getUniqData(self):
        return self.hwAddr

    def debugLog(self, debugData):
        if self.debug is True:
            print debugData

    def prepare(self):
        # install arp-scan on node
        self.runCommand(
            "which arp-scan || sudo apt-get --force-yes -y install arp-scan")
        self.setUniqData()
        self.debugLog("Unit data is " + self.getUniqData())
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

    def assignCredential(self, user, key, password = None):
        self.user = user
        self.password = password

        # from paramiko?
        self.origKey = key

        self._pkey = RSAKey.from_private_key(StringIO(self.origKey))

#        try:
#            self._pkey = RSAKey.from_private_key(StringIO(self.origKey))
#        except SSHException:
#           try:
#                self._pkey = DSSKey.from_private_key(StringIO(self.origKey))
#           except SSHException:
#                raise "Unknown private key format"

    def setProxyCommand(self, proxyCommand):
        self.proxyCommand = proxyCommand

    def connect(self):
        if self.connected is True:
            raise AssertionError(self.connected is True)
        try:
            print self.hostName, " ", self.accessPort, " ",  self.user, " "
            self.ssh.connect(self.hostName, self.accessPort, self.user,
                             pkey=self._pkey)
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
            AssertionError(command == "")

        if (self.connected is False):
            self.connect()
        self.debugLog("---> " + self.hostName + " " + command)
        stdin, stdout, stderr = self.ssh.exec_command(command)
        self.debugLog("OK   " + self.hostName + " " + command)

        return (stdout.readlines(), stderr.readlines())

    def __discovery__(self):

        # tuesday discovery
        (self.discovery_data, _) = self.runCommand(
            "ip link | awk -F: '/^[0-9]+?: eth/ {print $2}' |\
            sudo xargs -I% arp-scan -l -I % 2>&1 | grep -E '^[0-9]+?\.' | grep"
            " -E '192.168.(28|30)'.101")

    def discovery(self):
        self.prepare()
        node = {}

        self.__discovery__()
        for n in self.discovery_data:
            (node['ip'], node['hwaddr'], _) = n.split("\t")
            self.neighbours[node['hwaddr']] = node['ip']

        self.neighbours[self.getUniqData()] = self.hostName

        return self.neighbours
