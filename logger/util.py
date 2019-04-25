from logging import handlers
import os


def logmaker(**kwargs):
    klass = kwargs['klass']

    del kwargs['klass']
    if klass == 'TimedRotatingFileHandler':
        klass = handlers.TimedRotatingFileHandler(**kwargs)

    return klass
