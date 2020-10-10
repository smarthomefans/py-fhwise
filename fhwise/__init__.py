import socket
import logging
import struct
import select
from .protocol import Message

_LOGGER = logging.getLogger(__name__)
UDP_RECV_TIMEOUT_S=3

class FhwisePlayer:
    """Control Fhwise player though UDP."""

    def __init__(self, addr: str, port: int = 8080, timeout: int = UDP_RECV_TIMEOUT_S) -> None:
        """new a Fhwise player."""
        self.addr = addr
        self.port = port
        self._timeout = timeout
        self._send_cmdid = 1
        self._recv_cmdid = 1

    def connect(self):
        """Connect to Fhwise device."""
        self.udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp.bind(('0.0.0.0', self.port))
        self.udp.setblocking(0)

    def disconnect(self):
        """disconnect to Fhwise device."""
        self.udp.close()
        self._send_cmdid = 1
        self._recv_cmdid = 0

    def _send_raw_command(self, command: int, payload: bytes, ack: bool) -> bytes:
        """Send UDP data to Fhwise device."""
        send_raw = Message.build(dict(code=command, payload=payload,
                                      cmdid=self._send_cmdid))
        _LOGGER.debug('Send command to device: ' + bytes(send_raw).hex())

        self.udp.sendto(send_raw, (self.addr, self.port))

        if (ack):
            _LOGGER.debug('start receive.')
            ready = select.select([self.udp], [], [], self._timeout)
            if ready[0]:
                retval = b''
                recv_raw = self.udp.recv(1024)
                _LOGGER.debug('Received from device: ' + bytes(recv_raw).hex())
                try:
                    recv = Message.parse(recv_raw)
                    self._recv_cmdid = recv.cmdid
                    retval = recv.payload
                    self._send_cmdid += 1
                    if self._send_cmdid > 255:
                        self._send_cmdid = 1
                    return retval
                except:
                    _LOGGER.error('Received invalid raw data(%s)' % (recv_raw))
            else:
                _LOGGER.error('Received timeout')

        self._send_cmdid += 1
        if self._send_cmdid > 255:
            self._send_cmdid = 1
        return b''

    def send_raw_command(self, command: int, payload: bytes = b'', ack: bool = True) -> bytes:
        self.connect()
        retval = self._send_raw_command(command, payload, ack)
        self.disconnect()
        return retval

    def send_heartbeat(self) -> str:
        """Return device model in UTF8"""
        return self.send_raw_command(0xC0).decode('utf-8')

    def send_play_pause(self) -> bytes:
        return self.send_raw_command(0xC1)

    def send_previous_song(self) -> bytes:
        return self.send_raw_command(0xC2)

    def send_next_song(self) -> bytes:
        return self.send_raw_command(0xC3)

    def get_play_mode(self) -> int:
        """
        00 00 00 00 seq play
        01 00 00 00 repeat all
        02 00 00 00 repeat single
        03 00 00 00 radom play
        """
        return int.from_bytes(self.send_raw_command(0xC4, b'\x30'), byteorder = 'little', signed = True)

    def set_toggle_play_mode(self) -> int:
        """
        00 00 00 00 seq play
        01 00 00 00 repeat all
        02 00 00 00 repeat single
        03 00 00 00 radom play
        """
        return int.from_bytes(self.send_raw_command(0xC4, b'\x31'), byteorder = 'little', signed = True)

    def set_volume_down(self) -> int:
        return int.from_bytes(self.send_raw_command(0xC5, b'\x30'), byteorder = 'little', signed = True)

    def set_volume_up(self) -> int:
        return int.from_bytes(self.send_raw_command(0xC5, b'\x31'), byteorder = 'little', signed = True)

    def get_play_status(self) -> int:
        """
        FF FF FF FF no file
        00 00 00 00 invalid
        01 00 00 00 play
        02 00 00 00 pause
        03 00 00 00 stop
        04 00 00 00 pareSync
        05 00 00 00 pareComplete
        06 00 00 00 Complete
        """
        return int.from_bytes(self.send_raw_command(0xC6), byteorder = 'little', signed = True)

    def get_current_file_length(self) -> int:
        """
        A8 27 03 00 00 00 00 00 = 3"26' = 206760ms
        """
        return int.from_bytes(self.send_raw_command(0xC8), byteorder = 'little', signed = True)

    def get_current_file_position(self) -> int:
        """
        2A 7F 00 00 00 00 00 00 = 32' = 32554ms
        """
        return int.from_bytes(self.send_raw_command(0xC9), byteorder = 'little', signed = True)

    def get_current_file_name(self) -> str:
        """
        File name in UTF-8
        30 32 20 52 45 56 45 52 01 = 02 REVER
        """
        return self.send_raw_command(0xCA).decode('utf-8')

    def get_current_room_info(self) -> str:
        """
        File name in UTF-8
        72 6F 6F 6D 3A 3A 37 38 32 = room::782
        """
        return self.send_raw_command(0xCB).decode('utf-8')

    def set_current_file_position(self, pos: int = 0) -> int:
        """
        75 66 00 00 = 26' = 26229ms
        """
        return int.from_bytes(self.send_raw_command(0xCC, pos.to_bytes(length = 4, byteorder = 'little', signed = True)), byteorder = 'little', signed = True)

    def set_current_file_type(self, type: int = 0) -> int:
        """
        1：music   2：radio   3：video   4：image
        """
        return int.from_bytes(self.send_raw_command(0xCD, type.to_bytes(length = 4, byteorder = 'little', signed = True)), byteorder = 'little', signed = True)

    def get_current_list_file_account(self) -> int:
        """
        50 00 00 00 = 80
        """
        return int.from_bytes(self.send_raw_command(0xCE), byteorder = 'little', signed = True)

    def get_current_list_file_info(self, num: int) -> str:
        """
        00 00 00 00 = first file
        30 3A 3A E5 8C 97 E4 BA AC E7 88 B1 E5 AE B6 E5 B9 BF E6 92 AD 3A 3A 30 3A 3A = Name::length::Artist
        """
        return self.send_raw_command(0xCF, num.to_bytes(length = 4, byteorder = 'little', signed = True)).decode('utf-8')

    def set_current_list_play_file(self, num: int) -> int:
        """
        00 00 00 00 = first file
        """
        return int.from_bytes(self.send_raw_command(0xD0, num.to_bytes(length = 4, byteorder = 'little', signed = True)), byteorder = 'little', signed = True)

    def get_current_file_artist(self) -> str:
        """
        44 65 6F 72 72 6F = Deorro
        """
        return self.send_raw_command(0xD1).decode('utf-8')

    def set_volume_level(self, num: int) -> int:
        """
        level range 0--15
        """
        return int.from_bytes(self.send_raw_command(0xD2, num.to_bytes(length = 4, byteorder = 'little', signed = True)), byteorder = 'little', signed = True)

    def get_volume_level(self) -> int:
        """
        level range 0--15
        """
        return int.from_bytes(self.send_raw_command(0xD3), byteorder = 'little', signed = True)

    def set_room_name(self, name: str) -> str:
        """
        room name in UTF-8
        72 6F 6F 6D = room
        """
        return self.send_raw_command(0xD4, name.encode('utf-8')).decode('utf-8')

    def set_room_number(self, number: int) -> int:
        """
        room number in UTF-8
        00 00 00 31 = '1'
        """
        return int(self.send_raw_command(0xD5, str(number).encode('utf-8')).decode('utf-8'))

    def get_volume_source(self) -> int:
        """
        FF FF FF FF = -1
        00 00 00 00 = Local
        01 00 00 00 = ext1
        02 00 00 00 = ext2
        03 00 00 00 = BT
        04 00 00 00 = UX
        """
        return int.from_bytes(self.send_raw_command(0xD6, (-1).to_bytes(length = 4, byteorder = 'little', signed = True)), byteorder = 'little', signed = True)

    def set_volume_source(self, source: int) -> bytes:
        """
        FF FF FF FF = -1
        00 00 00 00 = Local
        01 00 00 00 = ext1
        02 00 00 00 = ext2
        03 00 00 00 = BT
        04 00 00 00 = UX
        """
        return int.from_bytes(self.send_raw_command(0xD6, source.to_bytes(length = 4, byteorder = 'little', signed = True)), byteorder = 'little', signed = True)

    def get_sub_area_control(self, number: int) -> str:
        """
        number range 0--3
        30 3A 3A 31 35 3A 3A 31 = '0::15::1' = area0, volume15, on
        """
        return self.send_raw_command(0xDC, number.to_bytes(length = 4, byteorder = 'little', signed = True)).decode('utf-8')

    def set_sub_area_control(self, number: int, volume: int, on: bool) -> str:
        """
        number range 0--3
        30 3A 3A 31 35 3A 3A 31 = area1, volume15, on
        """
        send_data = '%d::%d::%d' % (number, volume, on)
        return self.send_raw_command(0xDD, send_data.encode('utf-8')).decode('utf-8')

    def get_eq_type(self) -> int:
        """
        00 00 00 00	nomal
        01 00 00 00	rock
        02 00 00 00	pop
        03 00 00 00	dance
        04 00 00 00	hihop
        05 00 00 00	classic
        06 00 00 00	bass
        07 00 00 00	voice
        """
        return int.from_bytes(self.send_raw_command(0xDE), byteorder = 'little', signed = True)

    def set_eq_type(self, type: int) -> bytes:
        """
        00 00 00 00	normal
        01 00 00 00	rock
        02 00 00 00	pop
        03 00 00 00	dance
        04 00 00 00	hihop
        05 00 00 00	classic
        06 00 00 00	bass
        07 00 00 00	voice
        """
        return int.from_bytes(self.send_raw_command(0xDF, type.to_bytes(length = 4, byteorder = 'little', signed = True)), byteorder = 'little', signed = True)

    def get_eq_switch(self) -> int:
        """
        00 00 00 00	off
        01 00 00 00	on
        """
        return int.from_bytes(self.send_raw_command(0xE0), byteorder = 'little', signed = True)

    def set_eq_switch(self, on: bool) -> int:
        """
        00 00 00 00	off
        01 00 00 00	on
        """
        if on:
            return int.from_bytes(self.send_raw_command(0xE1, (1).to_bytes(length = 4, byteorder = 'little', signed = True)), byteorder = 'little', signed = True)
        else:
            return int.from_bytes(self.send_raw_command(0xE1, (0).to_bytes(length = 4, byteorder = 'little', signed = True)), byteorder = 'little', signed = True)

    def set_volume_toggle_mute(self) -> bytes:
        return self.send_raw_command(0xE3)