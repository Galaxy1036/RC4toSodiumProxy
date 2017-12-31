# -*- coding: utf-8 -*-


class ByteStream:

    def __init__(self):
        self.buffer = b''

    def writeByte(self, data):
        self.writeInt(data, 1)

    def writeInt(self, data, length=4):
        self.buffer += data.to_bytes(length, 'big')

    def writeVint(self, data):

        rotate = True
        final = b''
        if data == 0:
            self.writeByte(0)

        else:
            data = (data << 1) ^ (data >> 31)
            while data:
                b = data & 0x7f

                if data >= 0x80:
                    b |= 0x80

                if rotate:

                    rotate = False
                    lsb = b & 0x1
                    msb = (b & 0x80) >> 7
                    b >>= 1
                    b = b & ~(0xC0)
                    b = b | (msb << 7) | (lsb << 6)

                final += b.to_bytes(1, 'big')
                data >>= 7

        self.buffer += final

    def writeString(self, data=None):
        if data is not None:
            self.writeInt(len(data))
            self.buffer += data.encode('utf-8')
        else:
            self.writeInt(2**32 - 1)
