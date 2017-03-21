import struct
from brpc import encoding
from brpc.writer import hexify

class Reader():

    def __init__(self, data):
        # print " READ TYPE: {}".format(type(data))
        if data:
            self.data = bytearray(data)
        # self.data = data
        self.offset = 0

    def getSize(self):
        return len(self.data)

    def left(self):
        assert(len(self.data) <= self.offset)
        return len(self.data) - self.offset

    def seek(self, off):
        # print " SEEK[{}] += {}".format(self.offset, off)
        assert(self.offset + off >= 0)
        assert(self.offset + off <= len(self.data))
        self.offset += off

    def readU8(self):
        ret = struct.unpack_from('>B', self.data, self.offset)[0]
        # print "  readU8[{}]: {}".format(self.offset,ret)
        self.offset += 1
        return ret

    def readU16(self):
        ret = struct.unpack_from('>H', self.data, self.offset)[0]
        # print " readU16[{}]: {}".format(self.offset,ret)
        self.offset += 2
        return ret

    def readU16BE(self):
        ret = struct.unpack_from('<H', self.data, self.offset)[0]
        # print " readU16BE[{}]: {}".format(self.offset,ret)
        self.offset += 2
        return ret

    def readU32(self):
        ret = struct.unpack_from('>I', self.data, self.offset)[0]
        # print " readU32[{}]: {}".format(self.offset,ret)
        self.offset += 4
        return ret

    def readVarint(self):
        ret = encoding.readVarint(self.data, self.offset)
        self.offset += ret['size']
        return ret['value']

    def readString(self, enc, size):
        assert(size >= 0)
        # print " DFDFFD: off:{},  size:{},  len:{}".format(self.offset, size, len(self.data))
        assert(self.offset + size <= len(self.data))
        ret = self.data[self.offset : self.offset + size].decode(enc)
        # print u"readString[{}]: {}".format(self.offset, ret)
        self.offset += size
        return ret

    def readBytes(self, size, zeroCopy=False):
        assert(size >= 0)
        assert(self.offset + size <= len(self.data))
        if zeroCopy:
            ret = self.data[self.offset : self.offset + size]
        else:
            ret = bytearray()
            ret[:] = self.data[self.offset : self.offset + size]
        self.offset += size
        return ret
