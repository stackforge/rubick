import collections
import paramiko

from StringIO import StringIO
from paramiko.rsakey import RSAKey
from paramiko.dsskey import DSSKey
import stat
import os

TMP_KEY_PATH = "/tmp/joker_%s_%d"


class Node():

    def __init__(self, name, ip, port):

        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.setHostName(ip)
        self.setName(name)
        self.setAccessPort(port)
        self.connected = False

        self.neighbours = []
        self.debug = True

        self.proxyCommandTxt = self.proxyCommand = None
        self.link = None

        self.origKey = self._pkey = None
        self.keyPath = TMP_KEY_PATH % (name, os.getpid())

    def dumpKey(self, path, key):
        if (key): 
            f = open(path, "w", stat.S_IRUSR | stat.S_IWUSR)
            f.write(key)
            f.close()

#    def __del__(self):
#        print "Del %s" % self.keyPath
#        if os.path.exists(self.keyPath):
#            print "Remove %s" % self.keyPath
#            os.remove(self.keyPath)

    def proxyCommandGen(self, masterHost, masterPort, masterUser,
                        masterKeyfile):
        return "ssh -i %s -o StrictHostChecking=no -p%d %s@%s nc -q0 %s %d" % (
            masterKeyfile, masterPort, masterUser, masterHost,
            self.hostName, self.accessPort)

    def discoverHwAddr(self):
        try:
            (stdout, stderr) = self.runCommand(
                "ip addr | grep -A2 BROADCAST,MULTICAST,UP,LOWER_UP | "
                "awk '/link\/ether/ {ether=$2} /inet/ {print $2 \" \" ether}'")

        except:
            raise()

        macDict = {}

        for line in stdout:
            (ip, hwAddr) = line.strip().split(" ")
            macDict[hwAddr] = ip

        return macDict

    def setUniqData(self):
        self.link = self.discoverHwAddr()

    def getUniqData(self):
        return self.link

    def debugLog(self, debugData):
        if self.debug is True:
            print debugData

    def prepare(self):
        # install arp-scan on node
        try:
            self.runCommand(
                "[ ! -x arp-scan ] && sudo apt-get --force-yes -y install arp-scan")
        except:
            raise()
        self.setUniqData()

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

    def assignKey(self, key): 
        self.origKey = key
        # dump key to file
        self.dumpKey(self.keyPath, self.origKey)

        try:
            self._pkey = RSAKey.from_private_key(StringIO(self.origKey))
        except paramiko.SSHException:
            try:
                self._pkey = DSSKey.from_private_key(StringIO(self.origKey))
            except paramiko.SSHException:
                raise "Unknown private key format"
        

    def assignCredential(self, user, key, password=None):
        self.user = user
        self.password = password

        if (key):
            self.assignKey(key) 




    def setProxyCommand(self, masterHost, masterPort, masterUser, masterKeyfile):
        self.proxyCommandTxt = self.proxyCommandGen(
            masterHost, masterPort, masterUser, masterKeyfile)
        self.proxyCommand = paramiko.ProxyCommand(self.proxyCommandTxt)

    def connect(self):

        if self.connected is True:
            raise assertionError(self.connected is True)

        try:

            self.ssh.connect(self.hostName, self.accessPort, self.user,
                             pkey=self._pkey, sock=self.proxyCommand,
                             timeout=5, password = self.password)

            self.connected = True
            return True

        except paramiko.BadHostKeyException, e:
            print "Host key could not be verified: ", e
            return False
        except paramiko.AuthenticationException, e:
            print "Error unable to authenticate: ", e
            return False
        except paramiko.SSHException, e:
            return False
        except EOFError, e:
            return False

    def runCommand(self, command):
        if (command == ""):
            assertionError(command == "")

        if self.connected is False:
            self.connect()

        self.debugLog("---> " + self.hostName + " " + command)
        stdin, stdout, stderr = self.ssh.exec_command(command)
        self.debugLog("OK   " + self.hostName + " " + command)

        return (stdout.readlines(), stderr.readlines())

    def __discover__(self):
        
        (data, _) = self.runCommand(
            "(test -x arp-scan && ip link | awk -F: '/^[0-9]+?: eth/ {print $2}' |\
            sudo xargs -I% arp-scan -l -I % 2>&1 | grep -E '^[0-9]+?\.';\
            arp -an | awk -F\" \" '{ gsub(\"[^0-9\\.]\", \"\", $2); printf(\"%s\\t%s\\t%s\\n\", $2, $4, $7)}'\
            )")
        
        for line in data:
            (ip, hwAddr, _) = line.strip().split("\t")
            self.neighbours.append({"hwAddr": hwAddr, "ip": ip})
            self.debugLog("%s -> %s" % (self.hostName, ip))  


        

        return self.neighbours

    def discover(self):

        if self.connect() is False:
            return None

        self.prepare()

        return self.__discover__()
