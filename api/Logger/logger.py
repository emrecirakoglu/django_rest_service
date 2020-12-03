import logging
import logging.config
from inspect import getframeinfo, stack
import sys


class Logger(object):

    def __init__(self):
        super(Logger, self).__init__()

        logging.config.fileConfig('api/Logger/logger.conf')
        self.logger = logging.getLogger("giysLogger")

    def get_logger(self):
        return self.logger

    def debug(self, message):
        caller = getframeinfo(stack()[1][0])
        self.logger.debug('[{0}\t {1}]\t {2}'.format(self.get_log_header(caller.filename), caller.lineno, message))

    def info(self, message):
        caller = getframeinfo(stack()[1][0])
        self.logger.info('[{0}\t {1}]\t {2}'.format(self.get_log_header(caller.filename), caller.lineno, message))

    def warning(self, message):
        caller = getframeinfo(stack()[1][0])
        self.logger.warning('[{0}\t {1}]\t {2}'.format(self.get_log_header(caller.filename), caller.lineno, message))

    def error(self, message):
        try:
            exc_type, exc_value, exc_trace_back = sys.exc_info()
            caller = getframeinfo(stack()[1][0])

            if exc_type is None and exc_value is None and exc_trace_back is None:
                self.logger.error(
                    '[{0}\t  {1}]\t {2}'.format(self.get_log_header(caller.filename), caller.lineno, message))
            else:
                self.logger.error(
                    '[{0}\t  {1} {2}]\t {3}'.format(self.get_log_header(caller.filename), exc_trace_back.tb_lineno,
                                                    exc_type,
                                                    message))
        except Exception as e:
            self.logger.error(message)

    @staticmethod
    def get_log_header(file_path):

        if file_path is not None:
            name_list = file_path.split('/')
            result = ''
            if len(name_list) > 1:
                result = str(name_list[len(name_list) - 2]).upper() + ' >> ' + name_list[len(name_list) - 1]

            return result
        else:
            return None
