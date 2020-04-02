# Distributed Systems Assignment 2 - TCP File Transfer
A simple file transfer client using TCP.

**Table of Contents**
- Design
- Usage
- Contributing

## Design
The file transfer system uses the following components:
- `delivery.sh` - Takes user input and executes either `client.py` or `host.py`
- `client.py` - Send file(s) to specified IP
- `host.py` (server) - Listens for message from `client.py` and saves the file(s) contents

Two protocols are used to communicate and transfer data:

### Binary Transfer Protocol
| Bytes | Description|
|---|---|
|1 | filename length|
|8 | checksum | 
|256 | filename|
|n | content|

*Checksum will use the `hashlib` library.*

### Command Protocol

#### Commands
|     Hex     |       Description       |
|-------------|-------------------------|
|    0x01     |   connection handshake  |
|    0x02     |   begin sending         |
|    0x03     |   end connection        |
|    0x10     |   start file            |
|    0x20     |   end of file           |


#### Response Codes
|     Hex     |                      Description                    |
|-------------|-------------------------                            |
|    0xF0     |       connection success                            |
|    0xF1     |       modal mismatch                                |
|    0xF2     |       Filename more than 256 characters/non ascii   |

## Usage
- Send file(s) to to ip - `./delivery.sh --send IP FILENAME [FILENAME2 ..]`        
- Save file to specific location - `./delivery.sh --receive DIRECTORY
- Echo the contents of the file received - `./delivery.sh --receive`

## Contributing
Contributors include [Five Grant](https://github.com/fivegrant) and [Satchel Baldwin](https://github.com/satchelbaldwin)
