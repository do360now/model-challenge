def parse_query(query: str) -> list[tuple[str, str]]:
    if len(query) > 4096 or "\x00" in query:
        raise ValueError
    if query.startswith("?"):
        query = query[1:]
    if query == "":
        return []
    return [(_split_pair(piece)) for piece in query.split("&")]


def _split_pair(piece: str) -> tuple[str, str]:
    if "=" in piece:
        key, value = piece.split("=", 1)
    else:
        key, value = piece, ""
    return _decode(key), _decode(value)


def _decode(text: str) -> str:
    out = bytearray()
    i = 0
    n = len(text)
    while i < n:
        ch = text[i]
        if ch == "+":
            out.append(0x20)
            i += 1
            continue
        if ch == "%":
            if i + 2 >= n:
                raise ValueError
            hexpair = text[i + 1 : i + 3]
            try:
                out.append(int(hexpair, 16))
            except ValueError:
                raise ValueError
            i += 3
            continue
        out.extend(ch.encode("utf-8"))
        i += 1
    try:
        return out.decode("utf-8", errors="strict")
    except UnicodeDecodeError:
        raise ValueError
