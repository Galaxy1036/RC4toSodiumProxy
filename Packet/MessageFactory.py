# -*- coding: utf-8 -*-


class Factory:

    def __init__(self, crypto):
        self.crypto = crypto

    def process(self, packet):
        packetID = packet.id.to_bytes(2, 'big')

        if hasattr(packet, 'version'):
            packetVersion = packet.version.to_bytes(2, 'big')
        else:
            packetVersion = (0).to_bytes(2, 'big')

        packet.encode()
        payload      = self.crypto.encrypt(packet.id, packet.buffer)
        packetLength = len(payload).to_bytes(3, 'big')
        return packetID + packetLength + packetVersion + payload
