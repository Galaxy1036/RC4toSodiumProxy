# RC4toSodiumProxy :
A simple Clash Royale proxy

Proxy work like this:<br />
        
        Client ------->   Proxy     -------> Server
               (RC4)    (Convert)   (Sodium)
        Client <-------   Proxy     <------ Server

Run it with:<br />
`python Main.py`

For more information:<br />
`python Main.py -h`

## Dependencies :
Install `pynacl` with:<br />

     python -m pip install pynacl

Install `pyblake2` with:<br />

     python -m pip install pyblake2

Install `pycryptodome` with:<br />

     python -m pip install pycryptodome

## PS :
You need a patched rc4 apk, here is one there for CR 2.1:
https://mega.nz/#!mUtAxTCR!tl8VCAQkftyIqMdxv4Z8p_X-hQ_uK016FtCyRQ6IR8k
For more information contact me at @GaLaXy1036#1601
