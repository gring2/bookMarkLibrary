import logging


class ErrorFilter(logging.Filter):

    def filter(self, record):
        return record.levelno >= logging.ERROR


class WarningFilter(logging.Filter):

    def filter(self, record):
        return record.levelno >= logging.WARN


class DebugFilter(logging.Filter):

    def filter(self, record):
        return record.levelno >= logging.DEBUG


class InfoFilter(logging.Filter):
    def filter(self, record):
        return record.levelno <= logging.INFO
