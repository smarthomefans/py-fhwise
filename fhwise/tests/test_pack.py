from fhwise.protocol import Message

play_msg = Message.parse(bytes.fromhex('7E7E0004C1010D0A'))

print("%s" % (play_msg))

play_raw = Message.build(dict(code=0xC1, payload=b'', cmdid=1))
print("%s" % (play_raw))