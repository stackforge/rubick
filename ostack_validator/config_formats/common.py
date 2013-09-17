from ostack_validator.common import Mark, Issue, MarkedIssue

class ParseError(MarkedIssue):
  def __init__(self, message, mark):
    super(ParseError, self).__init__(Issue.ERROR, message, mark)

