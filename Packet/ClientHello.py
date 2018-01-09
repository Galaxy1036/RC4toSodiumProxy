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
        self.writeString('54331441934eeb7385d865d4e5bb251384aa7843')
        self.writeInt(2)
        self.writeInt(2)
