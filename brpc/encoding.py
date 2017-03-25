import struct

def sizeVarint(num):
    if num < 0xfd:
        return 1
    if num <= 0xffff:
        return 3
    if num <= 0xffffffff:
        return 5
    raise Exception("uint64 varints not supported")

def skipVarint(data, off):
    assert(off < len(data))

    if data[off] == 0xff:
        raise Exception("uint64 varints not supported")
    if data[off] == 0xfe:
        return 5
    if data[off] == 0xfd:
        return 3
    return 1

# Assumes unsigned
def writeVarint(dst, num, off):
    # the first byte tells us how long the varint is, if its > 0xfd
    if num <= 0xfd:
        struct.pack_into('<B', dst, off, num)
        return off + 1
    if num <= 0xffff:
        dst[off] = 0xfd
        struct.pack_into('<H', dst, off+1, num)
        return off + 3
    if num <= 0xffffffff:
        dst[off] = 0xfe
        struct.pack_into('<I', dst, off+1, num)
        return off + 5

def readVarint(data, off):
    assert(off < len(data))
    if data[off] == 0xff:
        raise Exception("uint64 varints not supported")
    elif data[off] == 0xfe:
        size = 5
        assert(off + size <= len(data))
        value =  struct.unpack_from('<I', data, off+1)[0]
        assert(value > 0xffff)
    elif data[off] == 0xfd:
        size = 3
        value = struct.unpack_from('<H', data, off+1)[0]
        assert(value >= 0xfd)
    else:
        size = 1
        value = struct.unpack_from('<B', data, off)[0]
    return {'size': size, 'value': value}
