from construct import (Struct, Bytes, Const, Int8ub, Int16ub, Rebuild, len_,
                       this)

Message = Struct(
    "header" / Const(bytes.fromhex('7E7E')),
    "length" / Rebuild(Int16ub, len_(this.payload) + 4),
    "code" / Int8ub,
    "payload" / Bytes(this.length-4),
    "cmdid" / Int8ub,
    "end" / Const(bytes.fromhex('0D0A')),
)
