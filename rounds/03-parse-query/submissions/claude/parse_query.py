"""Round 3: strict application/x-www-form-urlencoded parsing (Claude)."""

MAX_LEN = 4096
_HEX = frozenset("0123456789abcdefABCDEF")


def _decode(part: str) -> str:
    buf = bytearray()
    i, n = 0, len(part)
    while i < n:
        c = part[i]
        if c == "+":
            buf.append(0x20)
            i += 1
        elif c == "%":
            # Only ASCII hex digits count; int(..., 16) alone would accept
            # signs, underscores and non-ASCII digits.
            if i + 2 >= n:
                raise ValueError("truncated percent escape")
            h = part[i + 1:i + 3]
            if h[0] not in _HEX or h[1] not in _HEX:
                raise ValueError("invalid percent escape")
            buf.append(int(h, 16))
            i += 3
        else:
            # surrogatepass lets a lone surrogate through as bytes so the
            # strict decode below rejects it with a ValueError.
            buf += c.encode("utf-8", "surrogatepass")
            i += 1
    try:
        return bytes(buf).decode("utf-8", "strict")
    except UnicodeDecodeError as exc:
        raise ValueError("invalid UTF-8") from exc


def parse_query(query: str) -> list[tuple[str, str]]:
    if len(query) > MAX_LEN or "\x00" in query:
        raise ValueError("query too long or contains NUL")
    if query.startswith("?"):
        query = query[1:]
    if query == "":
        return []
    pairs = []
    for piece in query.split("&"):
        key, sep, value = piece.partition("=")
        pairs.append((_decode(key), _decode(value)))
    return pairs
