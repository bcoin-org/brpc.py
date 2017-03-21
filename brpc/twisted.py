#!/usr/bin/env python
from __future__ import absolute_import

# py2 requires trollius
# py3 requires asyncio
# 2&3 require autobahn

from brpc.writer import Writer, hexify
# from reader import Reader
from brpc.packet import Packet, Parser

# from autobahn.asyncio.websocket import (WebSocketServerProtocol,
#                                         WebSocketServerFactory)

from autobahn.twisted.websocket import (WebSocketServerProtocol,
                                        WebSocketClientProtocol)

from twisted.internet import defer

# if __name__ == '__main__':
# try:
#     import asyncio
# except ImportError:
#     # Trollius >= 0.3 was renamed
#     import trollius as asyncio

class TwistedBRPCProtocol():
    call_sequence = 0
    ping_challenge = 0
    call_defers = {}
    ping_defers = {}

    # Should be overloaded by users
    class CallHandlers():
        pass
    # Should be overloaded by users
    class EventHandlers():
        pass

    # def onConnect(self, request):
    #     print "Client Connecting..."
    #
    # def onOpen(self):
    #     print "WS open"

    def onMessage(self, payload, isBinary):
        assert(isBinary)
        if not hasattr(self, 'parser'):
            self.parser = Parser(self.onEvent)
        # print "RECEIVED MSG: {}".format(hexify(bytearray(payload)))
        self.parser.feed(payload)
        # print "cool"

    # def onClose(self, )

    def onEvent(self, packet):
        print " #### Handling[{}]: {}".format(packet.type, packet)
        if packet.type == Packet.types['EVENT']:
            handlers = self.EventHandlers
            if hasattr(handlers, '{}'.format(packet.event)):
                getattr(handlers, '{}'.format(packet.event))(packet.payload)
            elif hasattr(self, 'event_{}'.format(packet.event)):
                getattr(self, 'event_{}'.format(packet.event))(packet.payload)
            else:
                raise Exception("Received EVENT for unimplemented method: {}"
                        .format(packet.event))
        elif packet.type == Packet.types['CALL']:
            handlers = self.CallHandlers
            if hasattr(handlers, '{}'.format(packet.event)):
                ret = getattr(handlers, '{}'.format(packet.event))(packet.payload)
            elif hasattr(self, 'call_{}'.format(packet.event)):
                ret = getattr(self, 'call_{}'.format(packet.event))(packet.payload)
            else:
                raise Exception("Received CALL for unimplemented method: {}"
                        .format(packet.event))
            # self.sendAck(packet.id, ret)
            # send ACK
            ack_pak = Packet()
            ack_pak.type = Packet.types['ACK']
            ack_pak.id = packet.id
            ack_pak.payload = ret
            # print "sending Ack[{}]: {}".format(id, message)
            self.sendMessage(ack_pak.frame(), isBinary=True)
        elif packet.type == Packet.types['ACK']:
            print " RESOLVE ACK {}".format(packet.id)
            if packet.id in self.call_defers:
                self.call_defers[packet.id].callback(packet.payload)
                # self.defers.delete(packet.id) #TODO: ?
            else:
                raise Exception("Received ACK[{}] but no handler exists."
                        .format(packet.id))
        elif packet.type == Packet.types['ERROR']:
            #TODO:
            packet = Packet()
            packet.type = Packet.types['ERROR']
            packet.id = id
            packet.payload = message
            print "sending ERR[{}]: {}".format(id, message)
            self.sendMessage(packet.frame(), isBinary=True)
        elif packet.type == Packet.types['PING']:
            # send pong
            ping_pkt = Packet()
            ping_pkt.type = Packet.types['PING']
            ping_pkt.payload = nonce
            self.sendMessage(ping_pkt.frame(), isBinary=True)
        elif packet.type == Packet.types['PONG']:
            # resolve pong
            if packet.payload in self.ping_defers:
                self.ping_defers[packet.payload].callback(True)
            else:
                raise "pong without ping!"
        else:
            raise "Unknown Packet"

    # expects a response
    def call(self, event, payload):
        print "calling: {}".format(event, payload)
        packet = Packet()
        # packet = Packet(Packet.types['CALL'], payload)
        packet.type = Packet.types['CALL']
        packet.id = self.call_sequence
        self.call_sequence += 1
        packet.event = event
        packet.payload = payload
        dd = defer.Deferred()
        self.sendMessage(packet.frame(), isBinary=True)
        assert(packet.id not in self.call_defers)
        self.call_defers[packet.id] = dd
        return dd

    # trigger event
    def fire(self, event, payload):
        packet = Packet()
        packet.type = Packet.types['EVENT']
        packet.event = event
        packet.payload = payload
        self.sendMessage(packet.frame(), isBinary=True)

    def ping(self, nonce):
        assert(nonce not in self.ping_defers)
        packet = Packet()
        packet.type = Packet.types['PING']
        packet.payload = nonce
        dd = defer.Deferred()
        self.sendMessage(packet.frame(), isBinary=True)
        self.ping_defers[nonce] = dd  #TODO: ?
        return dd

class TwistedBRPCServerProtocol(TwistedBRPCProtocol, WebSocketServerProtocol):
    pass

class TwistedBRPCClientProtocol(TwistedBRPCProtocol, WebSocketClientProtocol):
    pass
