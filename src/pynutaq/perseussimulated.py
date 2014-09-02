__author__ = 'antmil'

from random import randint

MI125_BOARD_NUMBER = 1


class PerseusSimulated(object):

    def __init__(self):
        self.connect()
        print "Init DONE"

    def connect(self):
        print "Connected"

    def write(self, address, value):
        print "Value to write in address %d -> %d" % (address, value)

    def read(self, address):
        return randint(0, 0xFFFFFFFF)
