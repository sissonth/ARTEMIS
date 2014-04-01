#!/usr/bin/python

from card_reader import initialize_reader
from card_reader import test

x=initialize_reader()
print 'beginning test'
test(x)
