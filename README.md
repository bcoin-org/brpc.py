# BRPC python server/client
[BRPC](https://github.com/bcoin-org/brpc) is a binary-only RPC protocol for websockets (think socket.io, only faster).

### Supported websocket libs
  Python 2.5+ [Autobahn](https://github.com/crossbario/autobahn-python) (twisted or asyncio/trollius)

  Python 3+ Websocket (coming soon)

### Interface
Autobahn Twisted
``` python
import sys
from twisted.python import log
from twisted.internet import reactor
from autobahn.twisted.websocket import WebSocketServerFactory, WebSocketClientFactory

from brpc.twisted import TwistedBRPCServerProtocol, TwistedBRPCClientProtocol

class BRPC_ServerProtocol(TwistedBRPCServerProtocol):
    class CallHandlers():
        @staticmethod
        def foo(message):
            print( " Received message {}".format(message) )
            return " some response... "

    class EventHandlers():
        @staticmethod
        def bar(message):
            print( " Received message: {}".format(message) )

from twisted.internet.defer import inlineCallbacks

class BRPC_ClientProtocol(TwistedBRPCClientProtocol):
    @inlineCallbacks
    def onOpen(self):
        resp = yield self.call('foo', bytearray('message_str'))
        print(" Response for 'foo': {}".format(resp))
        self.fire('bar', bytearray('message_str'))

log.startLogging(sys.stdout)
factory = WebSocketServerFactory(u"ws://127.0.0.1:9001")
factory.protocol = BRPC_ServerProtocol
factory2 = WebSocketClientFactory(u"ws://127.0.0.1:9001")
factory2.protocol = BRPC_ClientProtocol
reactor.listenTCP(9000, factory)
reactor.connectTCP('127.0.0.1', 9000, factory2)
reactor.run()
```

### Testing
`python -m unittest discover`
