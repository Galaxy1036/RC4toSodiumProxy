# -*- coding: utf-8 -*-
import socket
import argparse
import time
import os
from threading import Thread
from hexdump import hexdump
from Piranha.Crypto import Crypto
from RC4.CryptoRC4 import CryptoRc4
from Packet.ClientHello import ClientHello
from Packet.MessageFactory import Factory
from ReplayManager import SavePacket
from Packet.packetList import *


def recvall(sock, size):
    data = []
    while size > 0:
        sock.settimeout(5.0)
        s = sock.recv(size)
        sock.settimeout(None)
        if not s:
            raise EOFError
        data.append(s)
        size -= len(s)
    return b''.join(data)


class ClientSide(Thread):

    def __init__(self, clientSocket, serverSocket, pepperCrypto, rc4Crypto, saveMessage, verbose):
        Thread.__init__(self)
        self.client       = clientSocket
        self.server       = serverSocket
        self.pepperCrypto = pepperCrypto
        self.rc4Crypto    = rc4Crypto
        self.factory      = Factory(pepperCrypto)
        self.saveMessage  = saveMessage
        self.verbose      = verbose

    def run(self):
        while True:
            header     = self.client.recv(7)
            data       = self.rc4Crypto.decrypt(recvall(self.client, int.from_bytes(header[2:5], 'big')))
            packetID   = int.from_bytes(header[:2], 'big')
            packetName = availablePacket.get(packetID, packetID)

            if len(header) > 0:

                print('[*] {} received from client (len: {})'.format(packetName, int.from_bytes(header[2:5], 'big')))

                if packetID == 10101:
                    preAuth = self.factory.process(ClientHello())
                    self.server.send(preAuth)
                    print('[*] PreAuth sended')
                    time.sleep(1)

                if self.verbose:
                    print(hexdump(header + data))

                if self.saveMessage:
                    SavePacket(header + data, packetName)

                if packetID != 10100:
                    encrypted = self.pepperCrypto.encrypt(packetID, data)
                    self.server.send(header[:2] + len(encrypted).to_bytes(3, 'big') + header[5:] + encrypted)

                else:
                    print('[*] Your client isn\'t patched (RC4) !')
                    os._exit(1)


class ServerSide(Thread):

    def __init__(self, clientSocket, serverSocket, pepperCrypto, rc4Crypto, saveMessage, verbose):
        Thread.__init__(self)
        self.client       = clientSocket
        self.server       = serverSocket
        self.pepperCrypto = pepperCrypto
        self.rc4Crypto    = rc4Crypto
        self.saveMessage  = saveMessage
        self.verbose      = verbose

    def run(self):
        while True:
            header     = self.server.recv(7)
            packetID   = int.from_bytes(header[:2], 'big')
            data       = self.pepperCrypto.decrypt(packetID, recvall(self.server, int.from_bytes(header[2:5], 'big')))
            packetName = availablePacket.get(packetID, packetID)

            if len(header) > 0:

                print('[*] {} received from server (len: {})'.format(packetName, int.from_bytes(header[2:5], 'big')))

                if self.verbose:
                    print(hexdump(header + data))

                if self.saveMessage:
                    SavePacket(header + data, packetName)

                if packetID != 20100:
                    encrypted = self.rc4Crypto.encrypt(data)
                    self.client.send(header[:2] + len(encrypted).to_bytes(3, 'big') + header[5:] + encrypted)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--save', action='store_true', help='Will save every packets')
    parser.add_argument('-v', '--verbose', action='store_true', help='Will display the contents of the packet on the screen')
    args = parser.parse_args()

    clientSocket = socket.socket()
    clientSocket.bind(('0.0.0.0', 9339))

    print('[*] Proxy is listening on port 9339')

    while True:

        clientSocket.listen(5)
        client, adress = clientSocket.accept()

        print('[*] Got connection from {}'.format(adress[0]))

        serverSocket = socket.socket()
        serverSocket.connect(('game.clashroyaleapp.com', 9339))

        PepperCrypto = Crypto("99b61876f3ff18caeca0aec1f326d9981bbcaf64e7daa317a7f10966867af968")
        Rc4Crypto    = CryptoRc4()

        clientThread = ClientSide(client, serverSocket, PepperCrypto, Rc4Crypto, args.save, args.verbose)
        serverThread = ServerSide(client, serverSocket, PepperCrypto, Rc4Crypto, args.save, args.verbose)

        clientThread.start()
        serverThread.start()
