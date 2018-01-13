# -*- coding: utf-8 -*-


def SavePacket(data, packetName):

    with open('Replay/message.index', 'r') as f:
        f = f.read()
        index = int(f)

    fileName = '{}-{}.bin'.format(index, packetName)

    with open("Replay/" + fileName, 'wb') as f:
        f.write(data)
        f.close()

    with open('Replay/message.index', 'w') as f:
        index += 1
        f.write(str(index))
        f.close()
