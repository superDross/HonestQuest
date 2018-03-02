''' Custom exceptions used througout the package.'''


class StatError(Exception):
    ''' Raise if an invalid stat is parsed.'''
    def __init__(self, stat, stats=['hp', 'mp', 'ag', 'st'], msg=None):
        if not msg:
            string = '''{} is invalid. The stat variable must be one of the following: {}'''
            msg = string.format(stat, ', '.join(stats))
        Exception.__init__(self, msg)
        self.stats = stats
        self.stat = stat
        self.msg = msg
