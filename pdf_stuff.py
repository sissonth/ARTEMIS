#!/usr/bin/python

import PythonMagick

def pdf2png(filename):
    img=PythonMagick.Image()
    img.density('300')
    img.read(filename)
    img.write('it_worked.PNG')