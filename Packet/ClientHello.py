# -*- coding: utf-8 -*-
import json
from Packet.Writer import ByteStream


class ClientHello(ByteStream):

    def __init__(self):
        self.id = 10100
        self.masterHash = json.load(open('config.json'))['MasterHash']
        super().__init__()

    def encode(self):

        self.writeInt(1)
        self.writeInt(15)
        self.writeInt(3)
        self.writeInt(0)
        self.writeInt(830)
        self.writeString(self.masterHash)
        self.writeInt(2)
        self.writeInt(2)
