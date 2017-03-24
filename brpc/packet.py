from brpc import encoding
from brpc.writer import Writer, hexify
from brpc.reader import Reader

class Packet():
    types = {
        'CALL': 0,
        'EVENT': 1,
        'ACK': 2,
        'ERROR': 3,
        'PING': 4,
        'PONG': 5,
    }

    class Header():
        # type = 0
        # size = 0
        # checksum = 0
        #
        def __init__(self, data=None):
            if data:
                # print " PH_DATA:{}".format(hexify(bytearray(data)))
                self.br = Reader(data)
                self.type = self.br.readU8()
                self.size = self.br.readU32()
                # self.checksum = self.br.readU32()
                # print "HEADER: {}".format(self.__dict__)

        # def fromRaw(self, data):
        #     br = Reader(data)
        #     self.type = br.readU8()
        #     self.size = br.readU32()
        #     return self

        def __str__(self):
            return "<packet.Header[{}] size:{}>".format(self.type, self.size)


    def __init__(self):
        self.type = 0
        self.id = 0
        self.event = ''
        self.payload = None#[]
        self.code = 0
        self.msg = ''

    def fromRaw(self, type, data):
        print "RAW:"
        self.type = type
        self.id = 0
        self.event = ''
        self.payload = None#[]
        self.code = 0
        self.msg = ''
        self.br = Reader(data)
        print " FROM RAW CALL:[{}] {}.".format(type, hexify(data))

        if type == self.types['EVENT']:
            size = self.br.readU8()
            self.event = self.br.readString('ascii', size)
            # print " FROM RAW CALL:[{}] {}.".format(size, self.event)
            print " EVT: {}".format(self.event)
            # count = br.readU8()
            size = self.br.readVarint()
            print " SIZE: {}".format(size)
            self.payload = self.br.readBytes(size)
            print " PAYLOAD: {}".format(self.payload)
        elif type == self.types['CALL']:
            size = self.br.readU8()
            self.event = self.br.readString('ascii', size)
            # print " FROM RAW CALL:[{}] {}.".format(size, self.event)
            print " EVT: {}".format(self.event)
            self.id = self.br.readU32()
            # count = br.readU8()
            size = self.br.readVarint()
            print " SIZE: {}".format(size)
            self.payload = self.br.readBytes(size)
            print " PAYLOAD: {}".format(self.payload)
        elif type == self.types['ACK']:
            self.id = self.br.readU32()
            size = self.br.readVarint()
            self.payload = self.br.readBytes(size)
        elif type == self.types['ERROR']:
            self.id = br.readU32()
            self.code = self.br.readU8()
            size = self.br.readU8();
            #TODO: make payload?
            self.msg = self.br.readString('acii', size)
        # elif type in (self.types['PING'], self.types['PONG']):
        elif type == self.types['PING']:
            self.payload = self.br.readBytes(8)
        elif type == self.types['PONG']:
            self.payload = self.br.readU64()
        else:
            raise "Unknown Packet Type"

        return self

    def getSize(self):
        size = 0
        if self.type == Packet.types['EVENT']:
            size += 1
            size += len(self.event)
            # size += 1
            # for i in self.payload:
            #     size += encoding.sizeVarint(len(i))
            #     size += len(i)  #TODO:
            size += encoding.sizeVarint(len(self.payload))
            size += len(self.payload)  #TODO:
        elif self.type == Packet.types['CALL']:
            size += 1
            size += len(self.event)
            size += 4
            # size += 1
            # for i in self.payload:
            #     size += encoding.sizeVarint(len(i))
            #     size += len(i)  #TODO:
            size += encoding.sizeVarint(len(self.payload))
            size += len(self.payload)  #TODO:
        elif self.type == Packet.types['ACK']:
            size += 4
            # size += 1
            # for i in self.payload:
            #     size += encoding.sizeVarint(len(i))
            #     size += len(i)  #TODO:
            size += encoding.sizeVarint(len(self.payload))
            size += len(self.payload)  #TODO:
        #TODO:
        elif self.type == self.types['ERROR']:
            size += 4
            size += 1
            size += 1
            size += len(self.msg)
        elif self.type in (self.types['PING'], self.types['PONG']):
            size += 8
        # elif self.type == self.types['PONG']:
        else:
            raise Exception("Unknown message type: {}.".format(self.type))
        return size

    # to_bytes
    def frame(self):
        size = self.getSize()
        # print " self: {}".format(self.__dict__)
        # print " FRAME: size={}".format(size)
        bw = Writer(size + 9)
        # i, item, data
        # write header
        bw.writeU8(self.type)
        bw.writeU32(size)
        bw.writeU32(0)

        if self.type == Packet.types['EVENT']:
            bw.writeU8(len(self.event))
            bw.writeString(self.event, 'ascii')
            # bw.writeU8(len(self.payload))
            # for item in self.payload:
                # bw.writeVarint(len(item))
                # bw.writeBytes(item)
            bw.writeVarint(len(self.payload))
            bw.writeBytes(self.payload)
        elif self.type == Packet.types['CALL']:
            print " FRAME_CALL: {}".format(self.__dict__)
            bw.writeU8(len(self.event))
            bw.writeString(self.event, 'ascii')
            bw.writeU32(self.id)
            # bw.writeU8(len(self.payload))
            # for item in self.payload:
            #     bw.writeVarint(len(item))
            #     bw.writeBytes(item)
            bw.writeVarint(len(self.payload))
            bw.writeBytes(self.payload)
        elif self.type == Packet.types['ACK']:
            bw.writeU32(self.id)
            # bw.writeU8(len(self.payload))
            ####
            bw.writeVarint(len(self.payload))
            bw.writeBytes(self.payload)
        elif self.type == Packet.types['ERROR']:
            bw.writeU32(self.id)
            bw.writeU8(self.code)
            bw.writeU8(len(self.msg))
            bw.writeString(self.msg, 'ascii')
        # elif self.type in (Packet.types['PING'], Packet.types['PONG']):
        elif self.type == Packet.types['PING']:
            bw.writeU64(self.payload)
        elif self.type == Packet.types['PONG']:
            bw.writeBytes(self.payload)
        else:
            raise Exception("Unknown message type {}.".format(self.type))

        data = bw.render()
        # print " DDDD: {}".format(data)
        #TODO: checksum
        return data


    # @classmethod
    # def parse(data):
        # Packet.Header(data)

class Parser():
    MAX_MESSAGE = 10000000

    def __init__(self, eventHandler):
        self.eventHandler = eventHandler
        # self.pending = bytearray()
        self.pending = []
        self.total = 0
        self.waiting = 9
        self.header = None

    def feed(self, data):
        #TODO: is this nessicary, or do all ws libs give you full frames?
        # chunk, off, data
        self.total += len(data)
        self.pending.append(data)
        # self.pending += data
        while self.total >= self.waiting:
            print " ==== OUTER: total:{},  wait:{}".format(self.total, self.waiting)
            chunk = bytearray(self.waiting)
            off = 0
            length = 0
            while off < len(chunk):
                # length = self.pending[0][:]#TODO....
                chunk[off:] = self.pending[0][:self.waiting]
                length = len(chunk)
                print " == INNER: off:{}, len:{}, len_p0:{}".format(off, length, len(self.pending[0]))
                ######################3333
                if length == len(self.pending[0]):
                # if len(chunk) == len(self.pending[0]):
                    self.pending.pop(0) #TODO: efficient?
                else:
                    self.pending[0] = self.pending[0][length:]
                off += length

            # assert(off == len(chunk))
            self.total -= len(chunk)
            self.parse(chunk)

    def parse(self, data):
        header = self.header
        packet = None
        data = bytearray(data)
        # assert(len(data) <= self.MAX_MESSAGE)
        if not self.header:
            self.header = Packet.Header(data)
            print " HEADER: {}".format(self.header)
            self.waiting = self.header.size
            if self.waiting > self.MAX_MESSAGE:
                self.waiting = 9
                self.error('Packet too Large.')
            return

        self.waiting = 9
        self.header = None

        # if header.checksum !== #TODO:
        #     self.error('Checksum mismatch.')

        # try:
        packet = Packet().fromRaw(header.type, data)
        # except Exception as e:
        #     self.emit('error', e)
        #     return

        print " GHGH: {}".format(packet)
        # self.emit('message', packet)
        self.eventHandler(packet)
