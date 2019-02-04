import logging


def getLogger(name):
    formatter = '%(asctime)s [%(name)25s] %(levelname)s : %(message)s'
    logging.basicConfig(level=logging.INFO, format=formatter)
    scheduler_logger = logging.getLogger('apscheduler.executors.default')
    scheduler_logger.setLevel(logging.ERROR)

    return logging.getLogger(name)
