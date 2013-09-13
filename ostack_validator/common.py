
def find(l, predicate):
  results = [x for x in l if predicate(x)]
  return results[0] if len(results) > 0 else None

class Mark(object):
  def __init__(self, source, line, column):
    self.source = source
    self.line = line
    self.column = column

  def __eq__(self, other):
    return (self.source == source) and (self.line == other.line) and (self.column == other.column)

  def __ne__(self, other):
    return not self == other

class Error(object):
  def __init__(self, message):
    self.message = message

  def __repr__(self):
    return '<%s "%s">' % (str(self.__class__).split('.')[-1], self.message)

class MarkedError(Error):
  def __init__(self, message, mark):
    super(MarkedError, self).__init__(message)
    self.mark = mark

  def __str__(self):
    return self.message + (" (source '%s' line %d column %d)" % (self.mark.source, self.mark.line, self.mark.column))


class Inspection(object):
  def inspect(openstack):
    pass

