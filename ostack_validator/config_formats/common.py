from ostack_validator.common import Mark, MarkedIssue, ERROR

class ParseError(MarkedIssue):
  def __init__(self, message, mark):
    super(ParseError, self).__init__(ERROR, message, mark)

