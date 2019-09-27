import socket
import logging
import struct


_LOGGER = logging.getLogger(__name__)

class FhwisePlayer:
    """Control Fhwise player though UDP."""

    def __init__(self, addr: str, port: int = 8080) -> None:
        """new a Fhwise player."""
        self.addr = addr
        self.port = port
        self._cmdid = 0

    def connect(self):
        """Connect to Fhwise device."""
        self.udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def disconnect(self):
        """disconnect to Fhwise device."""
        self.udp.close()
        self._cmdid = 0

    def send_raw_command(self, command: int, payload: bytes = None, ack: bool = True) -> bytes:
        """Send UDP data to Fhwise device."""
        data = bytearray(bytes.fromhex('7E7E'))
        data.append((len(payload)+4).to_bytes(2, byteorder="big", signed=False))
        data.append(command.to_bytes(1, signed=False))
        data.append(payload)
        data.append(self._cmdid.to_bytes(1, signed=False))
        data = bytearray(bytes.fromhex('0D0A'))
        _LOGGER.debug('Send command to device: ' + bytes(data).hex())

        self.udp.sendto(data, (self.addr, self.port))

        if (ack):
            self.udp.recv(65535)