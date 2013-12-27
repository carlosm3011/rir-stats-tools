###
# Properties
# carlos@lacnic.net
###

import os

## System paths
srchome = os.environ.get('SRCHOME', '')

paths = { 'tmp': "%s/tmp" % (srchome),
          'etc': "%s/etc" % (srchome) }

## -------------

## Servers
servers = { 'ripeval': {'http://ripeval.labs.lacnic.net:8080'}
           }
## -------------