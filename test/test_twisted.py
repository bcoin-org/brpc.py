from __future__ import absolute_import

import sys
from twisted.trial.unittest import TestCase
from twisted.internet.defer import Deferred, inlineCallbacks
from autobahn.twisted.websocket import WebSocketServerFactory, WebSocketClientFactory, connectWS, listenWS
from brpc.twisted import TwistedBRPCServerProtocol, TwistedBRPCClientProtocol


class TestBRPCProtocol():
    class CallHandlers():
        @staticmethod
        def echo(message):
            return message

    # class EventHandlers():
        # @staticmethod
        # def bar(message):
        #     print( " Received: {}".format(message) )

    def onOpen(self):
        self._open.callback(self)

    def onClose(self ,a,b,c):
        if hasattr(self, '_close'):
            self._close.callback(None)

class TestServerProtcol(TestBRPCProtocol, TwistedBRPCServerProtocol):
    pass
class TestClientProtcol(TestBRPCProtocol, TwistedBRPCClientProtocol):
    pass


class TwistedTestCase(TestCase):

    @inlineCallbacks
    def test_client_call_echo(self):
        resp = yield self.client.call('echo', bytearray('message_str'))
        self.assertEqual(resp, "message_str")

    @inlineCallbacks
    def test_server_call_echo(self):
        resp = yield self.server.call('echo', bytearray('other_str'))
        self.assertEqual(resp, "other_str")

    @inlineCallbacks
    def test_client_event(self):
        class EventHandlers():
            @staticmethod
            def foo(msg):
                assert(msg == 'message_str')
                x.callback(True)

        self.server.EventHandlers = EventHandlers
        x = Deferred()
        yield self.client.fire('foo', bytearray('message_str'))
        yield x  # ensure the event handler got called

    @inlineCallbacks
    def test_server_event(self):
        class EventHandlers():
            @staticmethod
            def foo(msg):
                assert(msg == 'message_str')
                x.callback(True)

        self.client.EventHandlers = EventHandlers
        x = Deferred()
        yield self.server.fire('foo', bytearray('message_str'))
        yield x  # ensure the event handler got called

    @inlineCallbacks
    def test_client_ping(self):
        #TODO: mock something to ensure it works
        yield self.client.ping(99)

    @inlineCallbacks
    def test_server_ping(self):
        #TODO: mock something to ensure it works
        yield self.server.ping(99)


    ##################################################
    @inlineCallbacks
    def setUp(self):
        port = 9009
        factory = WebSocketServerFactory(u"ws://127.0.0.1:{}".format(port))
        factory.protocol = TestServerProtcol
        client_factory = WebSocketClientFactory(u"ws://127.0.0.1:{}".format(port))
        client_factory.protocol = TestClientProtcol

        self.srdy = Deferred()
        self.crdy = Deferred()
        self.done = Deferred()

        # Save the client & server so they can be used inside tests.
        def client_rdy(clientProtocol):
            self.client = clientProtocol
        def server_rdy(serverProtocol):
            self.server = serverProtocol

        self.srdy.addCallback(server_rdy)
        self.crdy.addCallback(client_rdy)
        factory.protocol._open = self.srdy
        client_factory.protocol._open = self.crdy
        client_factory.protocol._close = self.done

        self.listening_port = listenWS(factory)
        connectWS(client_factory)
        yield self.srdy  # wait until ready
        yield self.crdy  # wait until ready

    def tearDown(self):
        self.listening_port.stopListening()
        self.client.sendClose()
        return self.done
