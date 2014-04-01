#!/usr/bin/python

import usb.core
import usb.util



vendorid = 0x0801
productid = 0x0002

device = usb.core.find(idVendor=vendorid, idProduct=productid)


device.detach_kernel_driver(0)
endpoint = device[0][(0,0)][0]

device.read(endpoint.bEndpointAddress, endpoint.wMaxPacketSize, timeout=5000)
array('B', [2, 0, 34, 0, 0, 0, 0, 0])
device.read(endpoint.bEndpointAddress, endpoint.wMaxPacketSize, timeout=5000)
array('B', [0, 0, 0, 0, 0, 0, 0, 0])
device.read(endpoint.bEndpointAddress, endpoint.wMaxPacketSize, timeout=5000)
array('B', [2, 0, 5, 0, 0, 0, 0, 0])
device.read(endpoint.bEndpointAddress, endpoint.wMaxPacketSize, timeout=5000)
array('B', [0, 0, 0, 0, 0, 0, 0, 0])
device.read(endpoint.bEndpointAddress, endpoint.wMaxPacketSize, timeout=5000)
array('B', [0, 0, 36, 0, 0, 0, 0, 0])