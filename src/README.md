
# Generic Post-Quantum Key Exchange Service

## Introduction

## Building
```shell
make clean
make
```

## Setting
- IPTable.cfg: IP and port setting.
    - GatewayID: Gateway's identity.
    - Mode: Client/Server mode or Peer-2-Peer mode.
    - Role: Client or Server in Client/Server mode
    - ServerID: Server's identity set for client side.
    - PresetInitialStatus: whether or not the client sets up the internal status upon being started. If set "Yes", the server must be started before the client is starting up.
- gw_xxx_xxx.cfg: client or server side setting.

## Running
```shell
cd bin/
./KexService ../gw_xxx_xxx.cfg ../IPTable.cfg
```

  
Modules		C_State	Language	status
- DH, not available now due to some issues.
- RSA-KEM	OK	cpp		Round2-only
- BIKE 		X	cpp		Round3-Alternative
- Frodo 	X	cpp		Round3-Alternative		
- NewHope 	X	cpp		Round2-only
- HQC 		X	cpp		Round3-Alternative
- RQC		OK	cpp		Round2-only
- NTRU 		X	cpp		Round3-FinalList
- NTRU Prime	OK	cpp		Round3-Alternative
- LEDAcrypt 	X	cpp		Round2-only
- LAC 		X	cpp		Round2-only
- SIKE		OK	cpp		Round3-Alternative
- NTS		OK	cpp		Round2-only
- ThreeBears	OK	cpp		Round2-only
- Kyber 	X	cpp		Round3-FinalList
- Saber		OK	cpp		Round3-FinalList
- Rollo		OK	cpp		Round2-only
- Round5	OK	cpp		Round2-only
- CM 		X	cpp		Round2-only

