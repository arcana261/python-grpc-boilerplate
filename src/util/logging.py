import logging

logging.basicConfig(format='%(asctime)-15s %(message)s')


def getLogger(name):
    result = logging.getLogger(name)
    result.setLevel(logging.INFO)
    return result
