import struct
from unittest import TestCase
from brpc.writer import Writer, hexify


#NOTE: more tests in test_reader
class TestWriter(TestCase):
    def test_float(self):
        x = Writer(12)
        x.writeFloat(0xcafebabe)
        x.writeFloatBE(0xcafebabe)
        x.writeFloat(1.0/3.0)
        self.assertEqual(x.written, 12)
        self.assertEqual(str(x), 'bbfe4a4f''4f4afebb''abaaaa3e')

    def test_double(self):
        x = Writer(24)
        x.writeDouble(0xdeadbeefcafebabe)
        x.writeDoubleBE(0xdeadbeefcafebabe)
        x.writeDouble(1.0/3.0)
        self.assertEqual(str(x), 'd75ff9ddb7d5eb43'
                                 '43ebd5b7ddf95fd7'
                                 '555555555555d53f')

    def test_copy(self):
        pass



    def test_fill(self):
        pass

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
            "facc34121234bbbbaaaaccccddddefcdab8967452301fafdff00fdccccfebbbbaaaa636f6f6ce298ba010101fa")
        self.assertEqual(x.written, 45)
        self.assertTrue(x.render())
