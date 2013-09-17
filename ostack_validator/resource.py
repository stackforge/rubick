import glob
import os.path

from ostack_validator.common import Error

class Resource(object):
  def __init__(self, name):
    super(Resource, self).__init__()
    self.name = name

  def get_contents(self):
    raise Error, 'Not implemented'

class ResourceLocator(object):
  def find_hosts(self):
    return []

  def find_host_components(self, host):
    return []

  def find_resource(self, host, component, name):
    return None

class FileResource(Resource):
  def __init__(self, name, path):
    super(FileResource, self).__init__(name)
    self.path = path

  def get_contents(self):
    with open(self.path) as f:
      return f.read()

class ConfigSnapshotResourceLocator(object):
  def __init__(self, basedir):
    super(ConfigSnapshotResourceLocator, self).__init__()
    self.basedir = basedir
    if not os.path.isdir(self.basedir):
      raise Error, 'Invalid argument: base directory does not exist'

  def find_hosts(self):
    return [os.path.basename(host_path) for host_path in glob.glob(os.path.join(self.basedir, '*')) if os.path.isdir(host_path)]

  def find_host_components(self, host):
    return [os.path.basename(component_path) for component_path in glob.glob(os.path.join(self.basedir, host, '*')) if os.path.isdir(component_path)]

  def find_resource(self, host, component, name):
    if not host:
      raise Error, 'Invalid argument: "host" need to be specified'

    if not component:
      raise Error, 'Invalid argument: "component" need to be specified'

    path = os.path.join(self.basedir, host, component, name)
    if not os.path.exists(path):
      return None

    fullname = '%s/%s/%s' % (host, component, name)

    return FileResource(fullname, path)

