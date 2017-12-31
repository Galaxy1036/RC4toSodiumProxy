# -*- coding: utf-8 -*-
from pyblake2 import blake2b
from nacl.public import Box
import nacl.utils


class Nonce:

    def __init__(self, nonce=None, clientKey=None, serverKey=None):
        if not clientKey:
            if nonce:
                self._nonce = nonce

            else:
                self._nonce = nacl.utils.random(Box.NONCE_SIZE)

        else:
            b2 = blake2b(digest_size=24)
            if nonce:
                b2.update(bytes(nonce))
            b2.update(bytes(clientKey))
            b2.update(serverKey)
            self._nonce = b2.digest()

    def __bytes__(self):
        return self._nonce

    def __len__(self):
        return len(self._nonce)

    def increment(self):
        self._nonce = (int.from_bytes(self._nonce, 'little') + 2).to_bytes(
            Box.NONCE_SIZE, 'little')
