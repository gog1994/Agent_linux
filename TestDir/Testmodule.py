import logging
import os
import sys


if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    
    formatter = logging.Formatter('[%(asctime)s - %(levelname)s] | %(message)s' )
    streamHandler = logging.StreamHandler()    
    fileHandler = logging.FileHandler(os.path.dirname(os.path.realpath(__file__)) + '/Log.txt')

    streamHandler.setFormatter(formatter)
    fileHandler.setFormatter(formatter)

    logger.addHandler(streamHandler)
    logger.addHandler(fileHandler)
    logger.setLevel(logging.INFO)

for arg in sys.argv:
    logger.info(arg)

#while True:
#    pass