#!/usr/bin/python

"""
Created on Tue Mar 18 19:55:45 2014

@author: tommy

read magtek magnetic card reader.

shoutout to Micah Carrick: http://www.micahcarrick.com/credit-card-reader-pyusb.html
"""


def read_pennCard():

    import sys
    import usb.core
    import usb.util
    
    VENDOR_ID = 0x0801
    PRODUCT_ID = 0x0002
    DATA_SIZE = 337
    
    # find the MagTek reader
    
    device = usb.core.find(idVendor=VENDOR_ID, idProduct=PRODUCT_ID)
    
    if device is None:
        sys.exit("Could not find MagTek USB HID Swipe Reader.")
    
    # make sure the hiddev kernel driver is not active
    
    if device.is_kernel_driver_active(0):
        try:
            device.detach_kernel_driver(0)
        except usb.core.USBError as e:
            sys.exit("Could not detatch kernel driver: %s" % str(e))
    
    # set configuration
    
    try:
        device.set_configuration()
        device.reset()
    except usb.core.USBError as e:
        sys.exit("Could not set configuration: %s" % str(e))
        
    endpoint = device[0][(0,0)][0]
    
    # wait for swipe
    
    data = []
    swiped = False
    print "Please swipe your card..."
    
    while 1:
        try:
            data += device.read(endpoint.bEndpointAddress, endpoint.wMaxPacketSize)
            if not swiped: 
                print "Reading..."
            swiped = True
        except usb.core.USBError as e:
            if swiped:
                print 'got it!'
                break
    
    # now we have the binary data from the MagReader! 
    
    enc_formats = ('ISO/ABA', 'AAMVA', 'CADL', 'Blank', 'Other', 'Undetermined', 'None')
    
#    print "Card Encoding Type: %s" % enc_formats[data[6]]
#    
#    print "Track 1 Decode Status: %r" % bool(not data[0])
#    print "Track 1 Data Length: %d bytes" % data[3]
#    print "Track 1 Data: %s" % ''.join(map(chr, data[7:116]))
#    
#    print "Track 2 Decode Status: %r" % bool(not data[1])
#    print "Track 2 Data Length: %d bytes" % data[4]
#    print "Track 2 Data: %s" % ''.join(map(chr, data[117:226]))
#    
#    print "Track 3 Decode Status: %r" % bool(not data[2])
#    print "Track 3 Data Length: %d bytes" % data[5]
#    print "Track 3 Data: %s" % ''.join(map(chr, data[227:336]))
    
    
    # Parse out Penn Card Number 
    track2 = ''.join(map(chr, data[117:226]))
    info = {}
    info['penn_card_number']=track2[7:15]
    
    #Parse out Name
    track1=''.join(map(chr, data[7:116]))
    i=track1.find('^',1)
    j=track1.rfind('^',1)
    info['name']=track1[i+1:j]
    
    
#    print "Penn card info: ", info

    return info['penn_card_number']


def initialize_cardReader():
    import sys
    import usb.core
    import usb.util
    
    VENDOR_ID = 0x0801
    PRODUCT_ID = 0x0002
    DATA_SIZE = 337
    
    # find the MagTek reader
    
    device = usb.core.find(idVendor=VENDOR_ID, idProduct=PRODUCT_ID)
    
    if device is None:
        sys.exit("Could not find MagTek USB HID Swipe Reader.")
    
    # make sure the hiddev kernel driver is not active
    
    if device.is_kernel_driver_active(0):
        try:
            device.detach_kernel_driver(0)
        except usb.core.USBError as e:
            sys.exit("Could not detatch kernel driver: %s" % str(e))
    
    # set configuration
    
    try:
        device.set_configuration()
        device.reset()
    except usb.core.USBError as e:
        sys.exit("Could not set configuration: %s" % str(e))
        
    endpoint = device[0][(0,0)][0]
    
    
    print 'CARD READER INITIALIZED'    

    
def retrieve_data():
    #import sys
    import usb.core
    #import usb.util
    
    VENDOR_ID = 0x0801
    PRODUCT_ID = 0x0002
    
    device = usb.core.find(idVendor=VENDOR_ID, idProduct=PRODUCT_ID)
    
#    if device is None:
#        sys.exit("Could not find MagTek USB HID Swipe Reader.")
    
    #endpoint = device[0][(0,0)][0]
    
    data = []

    swiped = False
    
    endpoint = device[0][(0,0)][0]
    
    while 1:
        try:
            data += device.read(endpoint.bEndpointAddress, endpoint.wMaxPacketSize)          

            if not swiped: 
                print "Reading..."
            swiped = True
        except usb.core.USBError as e:
            if swiped:
                print 'got it!'
                break
            else:
                #print 'swipe not detected'
                break

    if data != []:
        
        enc_formats = ('ISO/ABA', 'AAMVA', 'CADL', 'Blank', 'Other', 'Undetermined', 'None')
        
        print "Card Encoding Type: %s" % enc_formats[data[6]]
        
        print "Track 1 Decode Status: %r" % bool(not data[0])
        print "Track 1 Data Length: %d bytes" % data[3]
        print "Track 1 Data: %s" % ''.join(map(chr, data[7:116]))
        
        print "Track 2 Decode Status: %r" % bool(not data[1])
        print "Track 2 Data Length: %d bytes" % data[4]
        print "Track 2 Data: %s" % ''.join(map(chr, data[117:226]))
        
        print "Track 3 Decode Status: %r" % bool(not data[2])
        print "Track 3 Data Length: %d bytes" % data[5]
        print "Track 3 Data: %s" % ''.join(map(chr, data[227:336]))
        
        
        # Parse out Penn Card Number 
        track2 = ''.join(map(chr, data[117:226]))
        info = {}
        info['penn_card_number']=track2[7:15]
        
        #Parse out Name
        track1=''.join(map(chr, data[7:116]))
        i=track1.find('^',1)
        j=track1.rfind('^',1)
        info['name']=track1[i+1:j]
    
    
#    print "Penn card info: ", info

        return info['penn_card_number']
    else:
        return []        
    
#####################################################################
#####################################################################
##################################################################### 

def initialize_cardReader2():
    import sys
    import usb.core
    import usb.util
    
    VENDOR_ID = 0x0801
    PRODUCT_ID = 0x0002
    DATA_SIZE = 337
    
    # find the MagTek reader
    
    device = usb.core.find(idVendor=VENDOR_ID, idProduct=PRODUCT_ID)
    
    if device is None:
        sys.exit("Could not find MagTek USB HID Swipe Reader.")
    
    # make sure the hiddev kernel driver is not active
    
    if device.is_kernel_driver_active(0):
        try:
            device.detach_kernel_driver(0)
        except usb.core.USBError as e:
            sys.exit("Could not detatch kernel driver: %s" % str(e))
    
    # set configuration
    
    try:
        device.set_configuration()
        device.reset()
    except usb.core.USBError as e:
        sys.exit("Could not set configuration: %s" % str(e))
        
    endpoint = device[0][(0,0)][0]
    
    
    print 'CARD READER INITIALIZED'    
    return device,endpoint
    
def retrieve_data2(device,endpoint):
    #import sys
    import usb.core
    #import usb.util
  
    
    
    #VENDOR_ID = 0x0801
    #PRODUCT_ID = 0x0002
    
    #device = usb.core.find(idVendor=VENDOR_ID, idProduct=PRODUCT_ID)
    
    
    
    #endpoint = device[0][(0,0)][0]
    
    data = []

    swiped = False
    
    #endpoint = device[0][(0,0)][0]
    
    while 1:
        try:
            data += device.read(endpoint.bEndpointAddress, endpoint.wMaxPacketSize)          

            if not swiped: 
                print "Reading..."
            swiped = True
        except usb.core.USBError as e:
            if swiped:
                print 'got it!'
                break
            else:
                #print 'swipe not detected'
                break

    if data != []:
        
        enc_formats = ('ISO/ABA', 'AAMVA', 'CADL', 'Blank', 'Other', 'Undetermined', 'None')
        
        print "Card Encoding Type: %s" % enc_formats[data[6]]
        
        print "Track 1 Decode Status: %r" % bool(not data[0])
        print "Track 1 Data Length: %d bytes" % data[3]
        print "Track 1 Data: %s" % ''.join(map(chr, data[7:116]))
        
        print "Track 2 Decode Status: %r" % bool(not data[1])
        print "Track 2 Data Length: %d bytes" % data[4]
        print "Track 2 Data: %s" % ''.join(map(chr, data[117:226]))
        
        print "Track 3 Decode Status: %r" % bool(not data[2])
        print "Track 3 Data Length: %d bytes" % data[5]
        print "Track 3 Data: %s" % ''.join(map(chr, data[227:336]))
        
        
        # Parse out Penn Card Number 
        track2 = ''.join(map(chr, data[117:226]))
        info = {}
        info['penn_card_number']=track2[7:15]
        
        #Parse out Name
        track1=''.join(map(chr, data[7:116]))
        i=track1.find('^',1)
        j=track1.rfind('^',1)
        info['name']=track1[i+1:j]
    
    
#    print "Penn card info: ", info

        return info['penn_card_number']
    else:
        return []  

    