#!/usr/bin/env python
#=========================================================================
# client.py
#=========================================================================
# Author : Khalid Al-Hawaj
# Date   : August 30, 2017

import socket
import sys
import time
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
# Main Routine
#----------------------------------------------------------------------

#sleep_time = int(random.random() * 10)
#print 'sleeping for ', sleep_time
#time.sleep(sleep_time)

# Create a TCP/IP socket
sock = socket.create_connection(('localhost', 1111))

message = 'THIS IS MESSAGE!'

if len(sys.argv) > 1:
  message = ' '.join(sys.argv[1:])

try:
    
    # Send data
    send_data( sock, message )
    sock.sendall(message)

    data = recv_data( sock )
    print 'Server\'s reponse: {}'.format( data )

finally:
    sock.close()
