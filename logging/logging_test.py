import logging
import datetime

logging.basicConfig(filename='logging_test.log', level=logging.INFO, filemode='w')

# filemode = 'w' to overwrite the log file.
# filemod = 'a' (default) to append.

logging.info(msg=f'Code run on {datetime.datetime.now()}')
