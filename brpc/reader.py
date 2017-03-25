import struct
from brpc import encoding
from brpc.writer import hexify

class Reader():

    def __init__(self, data):
        self.data = bytearray(data)
        self.offset = 0

    def getSize(self):
        return len(self.data)

    def left(self):
        assert(len(self.data) <= self.offset)
        return len(self.data) - self.offset

    def seek(self, off):
        assert(self.offset + off >= 0)
        assert(self.offset + off <= len(self.data))
        self.offset += off

    def readU8(self):
        ret = struct.unpack_from('<B', self.data, self.offset)[0]
        self.offset += 1
        return ret

    def readU16(self):
        ret = struct.unpack_from('<H', self.data, self.offset)[0]
        self.offset += 2
        return ret

    def readU16BE(self):
        ret = struct.unpack_from('>H', self.data, self.offset)[0]
        self.offset += 2
        return ret

    def readU32(self):
        ret = struct.unpack_from('<I', self.data, self.offset)[0]
        self.offset += 4
        return ret

    def readU32BE(self):
        ret = struct.unpack_from('>I', self.data, self.offset)[0]
        self.offset += 4
        return ret

    def readU64(self):
        ret = struct.unpack_from('<Q', self.data, self.offset)[0]
        self.offset += 8
        return ret

    def readU64BE(self):
        ret = struct.unpack_from('>Q', self.data, self.offset)[0]
        self.offset += 8
        return ret

    def read8(self):
        ret = struct.unpack_from('<b', self.data, self.offset)[0]
        self.offset += 1
        return ret

    def read16(self):
        ret = struct.unpack_from('<h', self.data, self.offset)[0]
        self.offset += 2
        return ret

    def read16BE(self):
        ret = struct.unpack_from('>h', self.data, self.offset)[0]
        self.offset += 2
        return ret

    def read32(self):
        ret = struct.unpack_from('<i', self.data, self.offset)[0]
        self.offset += 4
        return ret

    def read32BE(self):
        ret = struct.unpack_from('>i', self.data, self.offset)[0]
        self.offset += 4
        return ret

    def read64(self):
        ret = struct.unpack_from('<q', self.data, self.offset)[0]
        self.offset += 8
        return ret

    def read64BE(self):
        ret = struct.unpack_from('>q', self.data, self.offset)[0]
        self.offset += 8
        return ret

    def readFloat(self):
        ret = struct.unpack_from('<f', self.data, self.offset)[0]
        self.offset += 4
        return ret

    def readFloatBE(self):
        ret = struct.unpack_from('>f', self.data, self.offset)[0]
        self.offset += 4
        return ret

    def readDouble(self):
        ret = struct.unpack_from('<d', self.data, self.offset)[0]
        self.offset += 8
        return ret

    def readDoubleBE(self):
        ret = struct.unpack_from('>d', self.data, self.offset)[0]
        self.offset += 8
        return ret

    def readVarint(self):
        ret = encoding.readVarint(self.data, self.offset)
        self.offset += ret['size']
        return ret['value']

    def skipVarint(self):
        size = encoding.skipVarint(self.data, self.offset)
        assert(self.offset + size <= len(self.data))
        self.offset += size

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

    def readVarBytes(self, zeroCopy=False):
        return self.readBytes(self.readVarint(), zeroCopy)

    def readString(self, enc, size):
        assert(size >= 0)
        assert(self.offset + size <= len(self.data))
        ret = self.data[self.offset : self.offset + size].decode(enc)
        self.offset += size
        return ret

    def readVarString(self, enc):
        size = self.readVarint()
        ret = self.readString(enc, size)
        return ret

    # Wrap struct.unpack for convenience
    def unpack(self, frmt):
        ret = struct.unpack_from(frmt, self.data, self.offset)
        self.offset += struct.calcsize(frmt)
        return ret
