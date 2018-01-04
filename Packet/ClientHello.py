# -*- coding: utf-8 -*-
from Packet.Writer import ByteStream


class ClientHello(ByteStream):

    def __init__(self):
        self.id = 10100
        super().__init__()

    def encode(self):
        
        self.writeInt(1)
        self.writeInt(15)
        self.writeInt(3)
        self.writeInt(0)
        self.writeInt(830)
        self.writeString('09214cae532dd8867928b3022c2d2e7e76e4a441')
        self.writeInt(2)
        self.writeInt(2)
