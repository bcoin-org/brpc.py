import array
import StringIO
import struct
import encoding
# import buffer
# import bytearray

## DEBUG ##
def hexify(byte_array):
    return ''.join(['{:02x}'.format(x) for x in byte_array])

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
        if self.written != len(self.data):
            # print " FuCKED: {} != {} => {}".format(self.written, len(self.data), hexify(self.data))
            assert(0)
        #TODO:
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
        struct.pack_into('>B', self.data, self.written, value)
        self.written += 1
        assert(struct.calcsize('>B') == 1)
        # print " writeU8[{}]: {}".format(value, hexify(self.data))

    # Write uint16le.
    # @param {Number} value * Write uint16le.
    # @param {Number} value
    def writeU16(self, value):
        # self.data += bytearray(struct.pack('>I', value))
        struct.pack_into('>H', self.data, self.written, value)
        self.written += 2
        assert(struct.calcsize('>H') == 2)
        # print "   writeU16[{}]: {}".format(value, hexify(self.data))

    # Write uint16be.
    # @param {Number} value * Write uint16be.
    # @param {Number} value
    def writeU16BE(self, value):
        # self.data += bytearray(struct.pack('<I', value))
        struct.pack_into('<H', self.data, self.written, value)
        self.written += 2
        assert(struct.calcsize('<H') == 2)
        # print " writeU16be[{}]: {}".format(value, hexify(self.data))

    # Write uint32le.
    # @param {Number} value * Write uint32le.
    # @param {Number} value
    def writeU32(self, value):
        # self.data += bytearray(struct.pack('>Q', value))
        struct.pack_into('>I', self.data, self.written, value)
        self.written += 4
        assert(struct.calcsize('>I') == 4)
        # print "   writeU32[{}]: {}".format(value, hexify(self.data))

    # Write uint32be.
    # @param {Number} value * Write uint32be.
    # @param {Number} value
    def writeU32BE(self, value):
        # self.data += bytearray(struct.pack('<Q', value))
        struct.pack_into('<I', self.data, self.written, value)
        self.written += 4
        assert(struct.calcsize('<I') == 4)
        # print " writeU32be[{}]: {}".format(value, hexify(self.data))

    def writeVarint(self, value):
        # l = encoding.sizeVarint(value)
        # self.data[self.written:self.written + l] = bytearray(value)[:l]
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

    def writeString(self, value, enc):
        value = bytearray(value, enc, 'strict')
        l = len(value)
        self.data[self.written:self.written + l] = value
        self.written += l
        # print "writeString[{}]: {}".format(value, hexify(self.data))

    def __str__(self):
        return hexify(self.data)

    # def __repr__(self):
    #     return "<Writer: {}>".format(self)
