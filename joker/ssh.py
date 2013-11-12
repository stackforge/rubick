import subprocess
import shlex
from os import environ

class JokerSecureShell():

    def __init__(self, hostName):
        self.tempDir = "/tmp"

        # TODO implement password authentication scheme
        self.credentials = {
            "user": None,
            "host": None,
            "port": 22,
            "key": None,
        }

        self.options = {
            "proxyCommand": None,
            "StrictHostKeyChecking": "no"
        }


        self.haveMasterSocket = False
        self.masterSocketPid = None


    # FIXME use inspect.stack()[0][3] ?
    @property
    def host(self):
        print "called host getter"
        return self.credentials['host']

    @host.setter
    def host(self, value):
        print "called host setter"
        self.credentials['host'] = value

    @property
    def user(self):
        return self.credentials['user'] if (self.credentials['user']) else environ['USER']

    @user.setter
    def user(self, value):
        self.credentials.user = value

    @property
    def key(self):
        assert self.credentials['key'] is not None, "Keyfile for %s@%s:%d not present" % (self.user, self.host, self.port)
        return self.credentials['key']

    @key.setter
    def key(self, value):
        self.credentials['key'] = value

    @property
    def port(self):
        return self.credentials['port']

    @port.setter
    def port(self, value):
        self.credentials.port = value

    @property
    def proxyCommand(self):
        return self.credentials.proxyCommand

    @proxyCommand.setter
    def proxyCommand(self, value):
        self.credentials.proxyCommand = value

    @property
    def masterSocketPath(self):
        return "%s/%s:%d" % (self.tempDir, self.host, self.port)

    @property
    def sshOptions(self):
        r = ""

        # compile ssh options in one string

        for i in self.options:
            if self.options[i] is not None:
                r = r + ( '-o %s=%s' % (i, self.options[i]) )

        return r;

    def createMasterSocket(self):
        self.haveMasterSocket = True

        # XXX we support only keys without password encryption
        cmd = "ssh -i %s -p %d %s -M -S %s %s@%s" % (self.key, self.port, self.sshOptions, self.masterSocketPath, self.user, self.host)

        #subprocess.Popen(shlex.split(cmd))


    def call(self, destinationCmd):
        if (not self.haveMasterSocket):
            self.createMasterSocket()

        #cmd = "ssh %s %s" % (self.host, destinationCmd)

       #stdout = stderr = None

        #exitCode = subprocess.call(shlex.split(destinationCmd), stdout = stdout, stderr = stderr)



js = JokerSecureShell(None)

js.host = "XFDSFSDFFFF"
print js.host


#js.user = "vagrant"
#js.port = 2222
#js.key = "/home/ryabin/.ssh/petya_env"

#js.call("id")

#js.call("ssh test echo ok")
#js.call("ssh test id")
