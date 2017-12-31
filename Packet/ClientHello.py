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
        self.writeString('74ecd0057e94aee0f6b485473ef3a047b4663e39')
        self.writeInt(2)
        self.writeInt(2)
