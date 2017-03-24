from brpc.reader import Reader
from brpc.writer import Writer
from unittest import TestCase

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
        y = Reader(x.render())
        # print "1: {}".format(y.readU8())
        # print "2: {}".format(y.readU8())
        # print "3: {}".format(y.readU16())
        # print "4: {}".format(y.readU16())
        # print "5: {}".format(y.readU16BE())
        # print "6: {}".format(y.readVarint())
        # print "7: {}".format(y.readVarint())
        # print "8: {}".format(y.readVarint())
        # print "9: {}".format(y.readVarint())
        # print u"10: {}".format(y.readString('ascii', 4))
        # print u"11: {}".format(y.readString('utf-8', 3))
        # print u"12: {}".format(y.readBytes(3))
        # print u"13: {}".format(y.readU8())
        # y.seek(-y.offset)
        self.assertEqual(y.offset, 0)
        self.assertEqual(y.readU8(), 0xfa)
        self.assertEqual(y.readU8(), 0xcc)
        self.assertEqual(y.readU16(), 0x1234)
        self.assertEqual(y.readU16BE(), 0x1234)
        self.assertEqual(y.readU32(), 0xaaaabbbb)
        self.assertEqual(y.readU32BE(), 0xccccdddd)
        self.assertEqual(y.readU64(), 0x0123456789abcdef)
        self.assertEqual(y.readVarint(), 0xfa)
        self.assertEqual(y.readVarint(), 0xff)
        self.assertEqual(y.readVarint(), 0xcccc)
        self.assertEqual(y.readVarint(), 0xaaaabbbb)
        self.assertEqual(y.readString('ascii', 4), 'cool')
        self.assertEqual(y.readString('utf-8', 3), u'\u263a')
        self.assertEqual(y.readBytes(3), '\x01'*3)
        self.assertEqual(y.readU8(), 0xfa)
        self.assertEqual(y.offset, 45)
        y.seek(-y.offset)
        self.assertEqual(y.offset, 0)
