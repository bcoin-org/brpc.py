import struct
from brpc import encoding

# Prints a bytearray as a hex string
def hexify(byte_array, spacer=''):
    return spacer.join(['{:02x}'.format(x) for x in byte_array])


class Writer():
    def __init__(self, size=0):
        # print "initing {}".format(size)
        self.data = bytearray(size)
        self.written = 0

     # Allocate and render the final buffer.
     # @param {Boolean?} keep - Do not destroy the writer.
     # @returns {Buffer} Rendered buffer.
    def render(self, keep=False):
        assert(self.written == len(self.data));
        data = self.data
        if not keep:
            self.destroy()
        return bytes(data)

    # Get size of data written so far.
    # @returns {Integer}
    def getSize(self):
        return self.written

    # Seek to relative offset.
    # @param {Integer} offset
    def seek(self, offset):
        self.written += offset

    # Destroy the buffer writer.
    def destroy(self):
        self.data = None
        self.written = None

    # Write uint8.
    # @param {Integer} value
    def writeU8(self, value):
        # self.data += bytearray(struct.pack('>H', value))
        struct.pack_into('<B', self.data, self.written, value)
        self.written += 1
        assert(struct.calcsize('<B') == 1)
        # print " writeU8[{}]: {}".format(value, hexify(self.data))

    # Write uint16le.
    # @param {Number} value
    def writeU16(self, value):
        # self.data += bytearray(struct.pack('>I', value))
        struct.pack_into('<H', self.data, self.written, value)
        self.written += 2
        assert(struct.calcsize('<H') == 2)
        # print "   writeU16[{}]: {}".format(value, hexify(self.data))

    # Write uint16be.
    # @param {Number} value
    def writeU16BE(self, value):
        # self.data += bytearray(struct.pack('<I', value))
        struct.pack_into('>H', self.data, self.written, value)
        self.written += 2
        assert(struct.calcsize('>H') == 2)
        # print " writeU16be[{}]: {}".format(value, hexify(self.data))

    # Write uint32le.
    # @param {Number} value
    def writeU32(self, value):
        # self.data += bytearray(struct.pack('>Q', value))
        struct.pack_into('<I', self.data, self.written, value)
        self.written += 4
        assert(struct.calcsize('<I') == 4)
        # print "   writeU32[{}]: {}".format(value, hexify(self.data))

    # Write uint32be.
    # @param {Number} value
    def writeU32BE(self, value):
        # self.data += bytearray(struct.pack('>Q', value))
        struct.pack_into('>I', self.data, self.written, value)
        self.written += 4
        assert(struct.calcsize('>I') == 4)
        # print "   writeU32BE[{}]: {}".format(value, hexify(self.data))

    # Write uint64le.
    # @param {Number} value
    def writeU64(self, value):
        struct.pack_into('<Q', self.data, self.written, value)
        self.written += 8
        assert(struct.calcsize('<Q') == 8)
        # print "   writeU64[{}]: {}".format(value, hexify(self.data))

    # Write uint64be.
    # @param {Number} value
    def writeU64BE(self, value):
        struct.pack_into('>Q', self.data, self.written, value)
        self.written += 8
        assert(struct.calcsize('>Q') == 8)
        # print "   writeU64BE[{}]: {}".format(value, hexify(self.data))

    # Write int8.
    # @param {Number} value
    def write8(self, value):
        # self.data += bytearray(struct.pack('<Q', value))
        struct.pack_into('<b', self.data, self.written, value)
        self.written += 1
        assert(struct.calcsize('<b') == 1)
        # print " write8[{}]: {}".format(value, hexify(self.data))

    # Write int16le.
    # @param {Number} value
    def write16(self, value):
        # self.data += bytearray(struct.pack('<Q', value))
        struct.pack_into('<h', self.data, self.written, value)
        self.written += 2
        assert(struct.calcsize('<h') == 2)
        # print " write16[{}]: {}".format(value, hexify(self.data))

    # Write int16be.
    # @param {Number} value
    def write16BE(self, value):
        # self.data += bytearray(struct.pack('<Q', value))
        struct.pack_into('>h', self.data, self.written, value)
        self.written += 2
        assert(struct.calcsize('>h') == 2)
        # print " write16[{}]: {}".format(value, hexify(self.data))

    # Write int32le.
    # @param {Number} value
    def write32(self, value):
        # self.data += bytearray(struct.pack('<Q', value))
        struct.pack_into('<i', self.data, self.written, value)
        self.written += 4
        assert(struct.calcsize('<i') == 4)
        # print " write32[{}]: {}".format(value, hexify(self.data))

    # Write int32be.
    # @param {Number} value
    def write32BE(self, value):
        # self.data += bytearray(struct.pack('<Q', value))
        struct.pack_into('>i', self.data, self.written, value)
        self.written += 4
        assert(struct.calcsize('>i') == 4)
        # print " write32BE[{}]: {}".format(value, hexify(self.data))

    # Write int64le.
    # @param {Number} value
    def write64(self, value):
        struct.pack_into('<q', self.data, self.written, value)
        self.written += 8
        assert(struct.calcsize('<q') == 8)
        # print "   write64[{}]: {}".format(value, hexify(self.data))

    # Write int64be.
    # @param {Number} value
    def write64BE(self, value):
        struct.pack_into('>q', self.data, self.written, value)
        self.written += 8
        assert(struct.calcsize('>q') == 8)
        # print "   write64BE[{}]: {}".format(value, hexify(self.data))

    # Write float le.
    # @param {Number} value
    def writeFloat(self, value):
        struct.pack_into('<f', self.data, self.written, value)
        self.written += 4
        assert(struct.calcsize('<f') == 4)

    # Write float be.
    # @param {Number} value
    def writeFloatBE(self, value):
        struct.pack_into('>f', self.data, self.written, value)
        self.written += 4
        assert(struct.calcsize('>f') == 4)

    # Write double le.
    # @param {Number} value
    def writeDouble(self, value):
        struct.pack_into('<d', self.data, self.written, value)
        self.written += 8
        assert(struct.calcsize('<d') == 8)

    # Write double be.
    # @param {Number} value
    def writeDoubleBE(self, value):
        struct.pack_into('>d', self.data, self.written, value)
        self.written += 8
        assert(struct.calcsize('>d') == 8)

    def writeVarint(self, value):
        self.written = encoding.writeVarint(self.data, value, self.written)
        # print "writeVarint[{}]: {}".format(value, hexify(self.data))
        # print "written: {}".format(self.written)

    def writeBytes(self, value):
        l = len(value)
        if l == 0: return
        # self.data += bytes(value)
        self.data[self.written:self.written + l] = value
        self.written += l
        # print " writeBytes[{}]: {}".format(value, hexify(self.data))

    # Write bytes with a varint length before them.
    # @param {Buffer} value
    def writeVarBytes(self, value):
        self.writeVarint(len(value))
        self.writeBytes(value)

    # Copy bytes into data.
    # @param {Buffer} value
    # @param {Number} start
    # @param {Number} end
    #TODO:
    # def copy(self, value, start, end=None):
    #     # self.writeBytes(value, start, end)
    #     # if end and end - start
    #     # self.data[self.written]

    # Write string to buffer
    # @param {String}
    # @param {String?} enc - Any buffer-supported encoding.
    def writeString(self, value, enc, writeLen=False):
        value = bytearray(value, enc, 'strict')
        l = len(value)
        if writeLen: self.writeVarint(l)
        self.data[self.written:self.written + l] = value
        self.written += l
        # print "writeString[{}]: {}".format(value, hexify(self.data))

    # Write a string with a varint length before it.
    # @param {String}
    # @param {String?} enc - Any buffer-supported encoding.
    def writeVarString(self, value, enc):
        self.writeString(value, enc, writeLen=True)

    # Fill N bytes with value.
    # @param {Number} value
    # @param {Number} size
    def fill(self, value, size):
        pass

    # Wrap struct.pack for convenience
    def pack(self, frmt, *values):
        struct.pack_into(frmt, self.data, self.written, *values)
        self.written += struct.calcsize(frmt)

    def __str__(self):
        return hexify(self.data)

    def __repr__(self):
        return "<Writer: {}>".format(hexify(self.data, ' '))
