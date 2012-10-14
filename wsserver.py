#!/usr/bin/env python

'''
Simple threading standalone WebSocket server. Builds on pywebsocket
standalone.py functionality. This is a toy for learning about web
sockets and shouldn't be used for anything serious. If you want to
use this anyway, it's under the MIT license.

Author: Sampo Pyysalo
'''

import sys

from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from SocketServer import ThreadingMixIn

from pywebsocket.standalone import StandaloneRequest
import pywebsocket.handshake as handshake

_SERVER_ADDR = ''
_SERVER_PORT = 9997

class BaseWSRequestHandler(BaseHTTPRequestHandler):
    """Base class for web socket handlers. Inherit from this class and
    override handle_stream()."""

    def handle_stream(self, stream):
        """Handle communication over an open web socket.
        
        Arg stream: mod_pywebsocket.stream.Stream"""
        raise NotImplementedError

    class _Dispatcher(object):
        """Dispatcher for pywebsocket.handshake, always accepts the request."""
        def do_extra_handshake(self, request):
            pass

    def parse_request(self):
        """Parse request as WebSocket handshake and pass stream to
        handle_stream(). 
        Overrides BaseHTTPRequestHandler.parse_request().
        """

        # Sets self.headers, self.path etc. for do_handshake()
        BaseHTTPRequestHandler.parse_request(self)

        request = StandaloneRequest(self)

        try:
            handshake.do_handshake(request, BaseWSRequestHandler._Dispatcher())
        except (handshake.VersionException, handshake.HandshakeException), e:
            # TODO: error handling
            print "Handshake failed:", e
            return False

        return self.handle_stream(request.ws_stream)

class EchoWSRequestHandler(BaseWSRequestHandler):
    """Example text echo handler that counts received messages."""

    def handle_stream(self, stream):
        """Handle communication over an open web socket.
        
        Arg stream: mod_pywebsocket.stream.Stream"""

        message_num = 1

        while True:
            message = stream.receive_message()

            if message is None:
                # client closed connection
                return False
            if not isinstance(message, unicode):
                raise NotImplementedError # TODO

            echo = '%d: %s' % (message_num, message)
            message_num += 1
            stream.send_message(echo, binary=False)
    
class WSServer(ThreadingMixIn, HTTPServer):
    def __init__(self, server_address, RequestHandlerClass):
        HTTPServer.__init__(self, server_address, RequestHandlerClass)

def main(argv):
    server = WSServer((_SERVER_ADDR, _SERVER_PORT), EchoWSRequestHandler)
    server.serve_forever()

if __name__ == '__main__':
    main(sys.argv)
