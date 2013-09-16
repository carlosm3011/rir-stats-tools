###
# Properties
# carlos@lacnic.net
###

import os

srchome = os.environ.get('SRCHOME', '')

paths = { 'tmp': "%s/tmp" % (srchome),
          'etc': "%s/etc" % (srchome) }