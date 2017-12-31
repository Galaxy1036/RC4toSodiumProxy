# -*- coding: utf-8 -*-


def SavePacket(data):

    with open('Replay/message.index', 'r') as f:
        f = f.read()
        index = int(f)

    packetID = int.from_bytes(data[:2], 'big')
    fileName = '{}-{}.bin'.format(index, packetID)

    with open("Replay/" + fileName, 'wb') as f:
        f.write(data)
        f.close()

    with open('Replay/message.index', 'w') as f:
        index += 1
        f.write(str(index))
        f.close()
