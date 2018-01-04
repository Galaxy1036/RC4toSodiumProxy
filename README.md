# RC4toSodiumProxy :
A simple Clash Royale proxy

Proxy work like this:<br />
        
        Client ------->   Proxy     -------> Server
               (RC4)    (Convert)   (Sodium)
        Client <-------   Proxy     <------ Server

Run it with:<br />
`python Main.py`

For more information type:<br />
`python Main.py -h`

## Dependencies :
Install `pynacl` with:<br />

     python -m pip install pynacl

Install `pyblake2` with:<br />

     python -m pip install pyblake2

Install `pycryptodome` with:<br />

     python -m pip install pycryptodome

## PS :
You need a patched rc4 apk, here is one there for CR 2.1:<br />
https://mega.nz/#!eMlWFT7Z!hfaSup3cC58ffYQrFhU3fUigQX8kaNqMSnDGzBK_Th<br />
For more information contact me at @GaLaXy1036#1601
