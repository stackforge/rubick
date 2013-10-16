import glob
import os.path
import json

from ostack_validator.common import Error, Version


class Resource(object):
    HOST = 'host'
    FILE = 'file'
    DIRECTORY = 'directory'
    SERVICE = 'service'

    def __init__(self, name):
        super(Resource, self).__init__()
        self.name = name

    def __str__(self):
        return self.name

    def __repr__(self):
        return '<%s name=%s>' % (str(self.__class__).split('.')[-1], self.name)

    def get_contents(self):
        raise Error('Not implemented')


class ResourceLocator(object):

    def find_resource(self, resource_type, name, host=None, **kwargs):
        return None


class HostResource(Resource):

    def __init__(self, name, resource_locator, interfaces=[]):
        super(HostResource, self).__init__(name)
        self.resource_locator = resource_locator
        self.interfaces = interfaces

    def find_resource(self, resource_type, name=None, **kwargs):
        return (
            self.resource_locator.find_resource(
                resource_type,
                name,
                host=self,
                **kwargs)
        )


class DirectoryResource(Resource):

    def __init__(self, name, owner=None, group=None, permissions=None):
        super(DirectoryResource, self).__init__(name)
        self.owner = owner
        self.group = group
        self.permissions = permissions


class FileResource(Resource):

    def __init__(self, name, path, owner=None, group=None, permissions=None):
        super(FileResource, self).__init__(name)
        self.path = path
        self.owner = owner
        self.group = group
        self.permissions = permissions

    def get_contents(self):
        with open(self.path) as f:
            return f.read()


class ServiceResource(Resource):

    def __init__(self, name, version, metadata={}):
        super(ServiceResource, self).__init__(name)
        self.version = Version(version)
        self.metadata = metadata


class FilesystemSnapshot(object):

    def __init__(self, path):
        super(FilesystemSnapshot, self).__init__()
        self.path = path
        self.basedir = os.path.join(os.path.dirname(self.path), 'root')
        self._parse_snapshot()

    def get_resource(self, path):
        if path in self._resources:
            return self._resources[path]

        return None

    def _parse_snapshot(self):
        self._resources = {}
        if not os.path.isfile(self.path):
            return
        with open(self.path) as f:
            for line in f.readlines():
                line = line.lstrip()
                if line == '' or line.startswith('#'):
                    continue

                resource_type = line.split('|')[0]
                if resource_type == 'dir':
                    source_path, owner, group, permissions = line.split(
                        '|')[1:]
                    self._resources[source_path] = DirectoryResource(
                        source_path,
                        owner=owner,
                        group=group,
                        permissions=permissions)
                elif resource_type == 'file':
                    source_path, local_path, owner, group, permissions = line.split(
                        '|')[1:]
                    self._resources[source_path] = FileResource(
                        os.path.basename(source_path),
                        path=os.path.join(self.basedir,
                                          local_path),
                        owner=owner,
                        group=group,
                        permissions=permissions)
                else:
                    self.logger.warn(
                        'Unknown resource "%s" in line "%s"' %
                        (resource_type, line))


class ConfigSnapshotResourceLocator(object):

    def __init__(self, basedir):
        super(ConfigSnapshotResourceLocator, self).__init__()
        self.basedir = basedir
        if not os.path.isdir(self.basedir):
            raise Error('Invalid argument: base directory does not exist')
        self._services = None
        self._filesystem_snapshots = {}

    def find_resource(self, resource_type, name=None, host=None, **kwargs):
        if resource_type == Resource.HOST:
            if name:
                host_path = os.path.join(self.basedir, name)
                if not os.path.isdir(host_path):
                    return None
                return HostResource(name, self)
            else:
                return (
                    [HostResource(os.path.basename(host_path), self)
                     for host_path in glob.glob(os.path.join(self.basedir, '*')) if os.path.isdir(host_path)]
                )
        if resource_type == Resource.FILE:
            if not host:
                raise Error('Invalid argument: "host" need to be specified')

            if isinstance(host, HostResource):
                host = host.name

            if name:
                return self._get_filesystem_snapshot(host).get_resource(name)
            else:
                return []
        elif resource_type == Resource.SERVICE:
            if not host:
                raise Error('Invalid argument: "host" need to be specified')

            if isinstance(host, HostResource):
                host = host.name

            self._ensure_services_loaded()

            if name:
                if name in self._services:
                    return self._services[host][name]
                else:
                    return None
            else:
                return self._services[host].values()
        else:
            return None

    def _ensure_services_loaded(self):
        if self._services:
            return

        self._services = {}
        for host_path in glob.glob(os.path.join(self.basedir, '*')):
            if not os.path.isdir(host_path):
                continue

            services_json_path = os.path.join(host_path, 'services.json')
            if not os.path.isfile(services_json_path):
                continue

            host_name = os.path.basename(host_path)
            self._services[host_name] = {}
            with open(services_json_path) as f:
                for service_name, metadata in json.loads(f.read()).items():
                    version = metadata.pop('version')
                    self._services[host_name][service_name] = ServiceResource(
                        service_name, str(version), metadata)

    def _get_filesystem_snapshot(self, host):
        if not host in self._filesystem_snapshots:
            self._filesystem_snapshots[host] = FilesystemSnapshot(
                os.path.join(self.basedir, host, 'filesystem'))
        return self._filesystem_snapshots[host]
