from __future__ import absolute_import

import sys
from twisted.python import log
from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks
from autobahn.twisted.websocket import WebSocketServerFactory, WebSocketClientFactory
from brpc.twisted import TwistedBRPCServerProtocol, TwistedBRPCClientProtocol

class BRPC_Server(TwistedBRPCServerProtocol):
    # def onOpen(self):
    #     print " SERVER OPEN"
    #
    # def call_foo(self, message):
    #     print( " SERVER H_FOO: {}".format(message) )
    #     return " some response... "

    # def event_bar(self, message):
    #     print " E_BAR: {}".format(message)

    class CallHandlers():
        @staticmethod
        def foo(message):
            print( " SERVER Z_FOO: {}".format(message) )
            return " some other response... "

    class EventHandlers():
        @staticmethod
        def bar(message):
            print( " SERVER E_BAR: {}".format(message) )



log.startLogging(sys.stdout)

factory = WebSocketServerFactory(u"ws://127.0.0.1:9001")
factory.protocol = BRPC_Server
# factory.setProtocolOptions(maxConnections=2)

# note to self: if using putChild, the child must be bytes...

reactor.listenTCP(9001, factory)
# reactor.run()


class BRPC_Client(TwistedBRPCClientProtocol):
    @inlineCallbacks
    def onOpen(self):
        print " CLIENT OPEN"
        resp = yield self.call('foo', bytearray('message_str'))
        print " CLIENT FOO RESP: {}".format(resp)
        # print " RESP: {}".format([i for i in resp])

    # def ack_foo(self, id, message):
    #     print " ACK_FOO: {}".format(message)


factory2 = WebSocketClientFactory(u"ws://127.0.0.1:9001")
factory2.protocol = BRPC_Client
reactor.connectTCP('127.0.0.1', 9001, factory2)
reactor.run()
