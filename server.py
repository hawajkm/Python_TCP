#!/usr/bin/env python
#=========================================================================
# server.py
#=========================================================================
# Author : Khalid Al-Hawaj
# Date   : August 30, 2017

import socket
import sys
import threading
import os
import random
import struct

#----------------------------------------------------------------------
# Helper functions
#----------------------------------------------------------------------

def send_data ( sock, data ):

  packer = struct.Struct('I {}s'.format( len(data) ))
  packet = ( len(data), data )
  packet_data = packer.pack( *packet )
  sock.sendall( packet_data )

def recv_data ( sock ):

  unpacker = struct.Struct('I')
  
  len_data = sock.recv( unpacker.size )
  length   = unpacker.unpack( len_data )[0]

  unpacker = struct.Struct('{}s'.format( length ))
  packet   = sock.recv( unpacker.size )
  data     = unpacker.unpack( packet )[0]

  return data

#----------------------------------------------------------------------
# Servicing Routine
#----------------------------------------------------------------------

def serviceClient(client, address):

  global reply
  global shutdown
  global sock

  try:
    data = recv_data( client )
    if data:
      send_data( client, reply )
      print '[{}] says "{}"'.format(address, data)
      if data == 'Bye! Bye! Miss American Pie':
        sock.close()
        shutdown = True
  except:
    pass

  client.close()

#----------------------------------------------------------------------
# Main Routine
#----------------------------------------------------------------------

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

address = ('', 1111)

reply = 'Roger that!'
shutdown = False

if len(sys.argv) > 1:
  reply = ' '.join(sys.argv[1:])

try:
  sock.bind(address)
  sock.listen(5)
except:
  print 'ERROR listening'
  quit(-1)

sock.settimeout(0.2)

print 'listening ...'

while not shutdown:
  try:
    client, address = sock.accept()
    client.settimeout(60)
    threading.Thread(target = serviceClient,args = (client, address[0])).start()
  except:
    pass
