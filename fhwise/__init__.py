import socket
import logging
import struct
from .protocol import Message

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

    def send_raw_command(self, command: int, payload: bytes = b'', ack: bool = True) -> bytes:
        """Send UDP data to Fhwise device."""
        send_raw = Message.build(dict(code=command, payload=payload,
                                      cmdid=self._cmdid))
        _LOGGER.debug('Send command to device: ' + bytes(send_raw).hex())

        self.udp.sendto(send_raw, (self.addr, self.port))

        if (ack):
            retval = b''
            recv_raw = self.udp.recv(1024)
            try:
                recv = Message.parse(recv_raw)
                if recv.cmdid == self._cmdid:
                    retval = recv.payload
                    self._cmdid++
                    return retval
                else:
                    _LOGGER.warn('Received msg(%s) but id not match.' % (recv))
            except expression as identifier:
                _LOGGER.error('Received invalid raw data(%s)' % (recv_raw))

        self._cmdid++
        return b''

    def send_heartbeat(self) -> bytes:
        """Return device model in UTF8"""
        return self.send_raw_command(0xC0)

    def send_play_pause(self) -> bytes:
        return self.send_raw_command(0xC1)

    def send_previous_song(self) -> bytes:
        return self.send_raw_command(0xC2)

    def send_next_song(self) -> bytes:
        return self.send_raw_command(0xC3)

    def get_play_mode(self) -> bytes:
        """
        00 00 00 00 seq play
        01 00 00 00 repeat all
        02 00 00 00 repeat single
        03 00 00 00 radom play
        """
        return self.send_raw_command(0xC4, b'\x30')
