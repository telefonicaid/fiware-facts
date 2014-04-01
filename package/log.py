__author__ = 'fla'

from package.configuration import LOGGING_PATH

import logging

logger = logging.getLogger('environments')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler(LOGGING_PATH + 'fiware-facts.log')
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s %(levelname)s policymanager.facts %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)
