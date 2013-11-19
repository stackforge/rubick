from rubick.common import Issue, MarkedIssue


class ParseError(MarkedIssue):

    def __init__(self, message, mark):
        super(ParseError, self).__init__(Issue.ERROR, message, mark)
