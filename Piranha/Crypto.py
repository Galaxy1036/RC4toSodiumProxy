# -*- coding: utf-8 -*-
import nacl.utils
import json
import os
from nacl.public import Box, PrivateKey, PublicKey
from Piranha.Nonce import Nonce
from Packet.Reader import Reader


class Crypto:

    def __init__(self, serverKey):
        self.serverKey    = bytes.fromhex(serverKey)  # server publicKey (can be found in libg.so)
        self.pk           = None  # publicKey
        self.sk           = None  # privateKey
        self.sessionKey   = None  # sessionKey from 20100
        self.sharedKey    = None  # sharedKey used to decrypt packet
        self.Nonce        = None  # nonce
        self.decryptNonce = None  # rnonce
        self.encryptNonce = None  # snonce

    def encrypt(self, packetID, payload):
        if packetID == 10100:

            return payload

        elif packetID == 10101:

            self.encryptNonce = Nonce()
            self.Nonce        = Nonce(clientKey=self.pk, serverKey=self.serverKey)
            self.sharedKey    = Box(self.sk, PublicKey(self.serverKey))

            return bytes(self.pk) + self.encryptPacket(self.sessionKey + bytes(self.encryptNonce) + payload, self.Nonce)

        else:
            return self.encryptPacket(payload)

    def decrypt(self, packetID, payload):
        if packetID == 20100:
            self.sessionKey = payload[4:]
            self.sk         = PrivateKey.generate()
            self.pk         = self.sk.public_key

            return payload

        elif packetID == 20103 and not self.sessionKey:
            packetReader = Reader(payload)

            if packetReader.ReadVint() == 7:
                print('[*] Look like masterHash is outdated ! Let the proxy update it')
                fingerprint = packetReader.ReadString()
                if fingerprint:
                    with open('config.json', 'r') as f:
                        config = json.load(f)
                        fingerprint = json.loads(fingerprint)
                        config['MasterHash'] = fingerprint['sha']

                    with open('config.json', 'w') as f:
                        f.write(json.dumps(config, indent=4))
                        f.close()

                    print('[*] MasterHash has been updated, re-run the proxy')

                else:
                    print('[*] Got errorcode 7 without fingerprint')

            else:
                print('[*] PreAuth packet is outdated, please get the latest one on GaLaXy1036 Github !')

            os._exit(1)
            return payload

        elif packetID == 22280 or (packetID == 20103 and self.sessionKey):
            nonce                = Nonce(self.encryptNonce, self.pk, self.serverKey)
            decrypted            = self.decryptPacket(payload, nonce)
            self.sharedKey       = Box.decode(decrypted[24:56])  # Overwrite the previous sharedKey
            self.decryptNonce    = Nonce(decrypted[:24])

            return decrypted[56:]

        else:
            return self.decryptPacket(payload)

    def encryptPacket(self, payload, nonce=None):
        if not nonce:
            self.encryptNonce.increment()
            nonce = self.encryptNonce

        return self.sharedKey.encrypt(payload, bytes(nonce))[24:]
        # 24 because the lib add 24 null bytes at the start of the payload

    def decryptPacket(self, payload, nonce=None):
        if not nonce:
            self.decryptNonce.increment()
            nonce = self.decryptNonce

        return self.sharedKey.decrypt(payload, bytes(nonce))
