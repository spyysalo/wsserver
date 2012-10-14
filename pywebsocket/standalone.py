# Some support classes from pywebsocket standalone.py (+minor modifications)

# Copyright 2012, Google Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
#     * Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above
# copyright notice, this list of conditions and the following disclaimer
# in the documentation and/or other materials provided with the
# distribution.
#     * Neither the name of Google Inc. nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

class StandaloneConnection(object):
    """Mimic mod_python mp_conn."""

    def __init__(self, request_handler):
        self._request_handler = request_handler

    def get_local_addr(self):
        """Mimic mp_conn.local_addr."""
        return (self._request_handler.server.server_name,
                self._request_handler.server.server_port)
    local_addr = property(get_local_addr)

    def get_remote_addr(self):
        """Mimic mp_conn.remote_addr."""
        return self._request_handler.client_address
    remote_addr = property(get_remote_addr)

    def write(self, data):
        """Mimic mp_conn.write()."""
        return self._request_handler.wfile.write(data)

    def read(self, length):
        """Mimic mp_conn.read()."""
        return self._request_handler.rfile.read(length)


class StandaloneRequest(object):
    """Mimic mod_python request."""

    def __init__(self, request_handler, use_tls=False):
        self._request_handler = request_handler
        self.connection = StandaloneConnection(request_handler)
        self._use_tls = use_tls
        self.headers_in = request_handler.headers

    def get_uri(self):
        """Getter to mimic request.uri."""
        return self._request_handler.path
    uri = property(get_uri)

    def get_method(self):
        """Getter to mimic request.method."""
        return self._request_handler.command
    method = property(get_method)

    def get_protocol(self):
        """Getter to mimic request.protocol."""
        return self._request_handler.request_version
    protocol = property(get_protocol)

    def is_https(self):
        """Mimic request.is_https()."""
        return False

    def _drain_received_data(self):
        """Don't use this method from WebSocket handler. Drains unread data
        in the receive buffer.
        """
        raw_socket = self._request_handler.connection
        drained_data = util.drain_received_data(raw_socket)
