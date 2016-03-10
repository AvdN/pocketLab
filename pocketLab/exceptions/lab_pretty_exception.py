__author__ = 'rcj1492'
__created__ = '2016.03'

import sys
from pprint import pprint

class LabPrettyException(Exception):

    def __init__(self, message='', printout=None, error=None):
        text = 'Errr! %s' % message
        self.error = error
        print(text)
        if printout:
            pprint(printout)
        sys.exit(2)