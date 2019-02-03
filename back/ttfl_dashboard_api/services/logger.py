import logging


def getLogger(name):
    formatter = '%(asctime)s [%(name)s] %(levelname)s : %(message)s'
    logging.basicConfig(level=logging.INFO, format=formatter)

    return logging.getLogger(name)
