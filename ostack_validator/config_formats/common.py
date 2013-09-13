from ostack_validator.common import Mark, MarkedError

class ParseError(MarkedError): pass

class ParseResult:
  def __init__(self, success, value):
    self.success = success
    self.value = value

