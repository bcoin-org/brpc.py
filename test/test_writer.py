import struct
from unittest import TestCase
from brpc.writer import Writer, hexify

class TestWriter(TestCase):
    def test_writer(self):
        x = Writer(45)
        x.writeU8(0xfa)
        x.writeU8(0xcc)
        x.writeU16(0x1234)
        x.writeU16BE(0x1234)
        x.writeU32(0xaaaabbbb)
        x.writeU32BE(0xccccdddd)
        x.writeU64(0x0123456789abcdef)
        x.writeVarint(0xfa)
        x.writeVarint(0xff)
        x.writeVarint(0xcccc)
        x.writeVarint(0xaaaabbbb)
        x.writeString("cool", 'ascii')
        x.writeString(u"\u263a", 'utf-8')
        x.writeBytes('\x01'*3)
        x.writeU8(0xfa)
        # print(" Writer: {}".format(x))
        self.assertEqual(str(x),
            "facc12343412aaaabbbbddddcccc0123456789abcdeffafd00fffdccccfeaaaabbbb636f6f6ce298ba010101fa")
        self.assertEqual(x.written, 45)
        self.assertTrue(x.render())
