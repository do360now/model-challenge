def match_glob(pattern: str, text: str) -> bool:
    if len(pattern) > 4096 or len(text) > 4096 or "\x00" in pattern or "\x00" in text:
        raise ValueError
    psegs = _pattern_segments(pattern)
    tsegs = text.split("/")
    memo = {}

    def rec(pi, ti):
        key = (pi, ti)
        if key in memo:
            return memo[key]
        if pi == len(psegs):
            memo[key] = ti == len(tsegs)
            return memo[key]
        if psegs[pi] is None:
            for k in range(ti, len(tsegs) + 1):
                if rec(pi + 1, k):
                    memo[key] = True
                    return True
            memo[key] = False
            return False
        if ti == len(tsegs) or not _seg_match(psegs[pi], tsegs[ti]):
            memo[key] = False
            return False
        memo[key] = rec(pi + 1, ti + 1)
        return memo[key]

    return rec(0, 0)


def _pattern_segments(pattern: str):
    segs = []
    buf = []
    i = 0
    n = len(pattern)
    in_class = False
    while i < n:
        ch = pattern[i]
        if ch == "\\" and not in_class:
            if i + 1 >= n:
                raise ValueError
            nxt = pattern[i + 1]
            if nxt == "/":
                segs.append("".join(buf))
                buf = []
                i += 2
                continue
            buf.append("\\")
            buf.append(nxt)
            i += 2
            continue
        if ch == "/" and not in_class:
            segs.append("".join(buf))
            buf = []
            i += 1
            continue
        if ch == "[" and not in_class:
            in_class = True
            buf.append(ch)
            i += 1
            if i < n and pattern[i] == "!":
                buf.append("!")
                i += 1
            if i < n and pattern[i] == "]":
                buf.append("]")
                i += 1
            continue
        if ch == "]" and in_class:
            in_class = False
            buf.append(ch)
            i += 1
            continue
        buf.append(ch)
        i += 1
    if in_class:
        raise ValueError
    segs.append("".join(buf))
    out = []
    for seg in segs:
        if seg == "**":
            out.append(None)
            continue
        if _has_bare_globstar(seg):
            raise ValueError
        out.append(_compile(seg))
    return out


def _has_bare_globstar(seg):
    i = 0
    n = len(seg)
    while i < n:
        if seg[i] == "\\":
            if i + 1 >= n:
                return False
            i += 2
            continue
        if seg[i] == "*" and i + 1 < n and seg[i + 1] == "*":
            return True
        i += 1
    return False


def _compile(seg):
    tokens = []
    i = 0
    n = len(seg)
    while i < n:
        ch = seg[i]
        if ch == "\\":
            if i + 1 >= n:
                raise ValueError
            tokens.append(("lit", seg[i + 1]))
            i += 2
            continue
        if ch == "*":
            tokens.append(("star",))
            i += 1
            continue
        if ch == "?":
            tokens.append(("any",))
            i += 1
            continue
        if ch == "[":
            cls, i = _compile_class(seg, i)
            tokens.append(cls)
            continue
        tokens.append(("lit", ch))
        i += 1
    return tokens


def _compile_class(seg, i):
    n = len(seg)
    i += 1
    if i >= n:
        raise ValueError
    negated = False
    if seg[i] == "!":
        negated = True
        i += 1
        if i >= n:
            raise ValueError
    atoms = []
    first = True
    while i < n and not (seg[i] == "]" and not first):
        first = False
        if seg[i] == "\\" and i + 1 < n:
            ch = seg[i + 1]
            i += 2
        else:
            ch = seg[i]
            i += 1
        if ch == "-" and atoms and i < n and seg[i] != "]":
            start = atoms.pop()
            if seg[i] == "\\" and i + 1 < n:
                end = seg[i + 1]
                i += 2
            else:
                end = seg[i]
                i += 1
            if ord(start) > ord(end):
                raise ValueError
            atoms.append((start, end))
            continue
        atoms.append(ch)
    if i >= n or seg[i] != "]":
        raise ValueError
    i += 1
    chars = set()
    for atom in atoms:
        if isinstance(atom, tuple):
            a, b = atom
            for cp in range(ord(a), ord(b) + 1):
                chars.add(chr(cp))
        else:
            chars.add(atom)
    if not chars:
        raise ValueError
    return ("class", negated, frozenset(chars)), i


def _seg_match(tokens, text):
    memo = {}

    def rec(ti, si):
        key = (ti, si)
        if key in memo:
            return memo[key]
        if ti == len(tokens):
            memo[key] = si == len(text)
            return memo[key]
        kind = tokens[ti][0]
        if kind == "star":
            for k in range(si, len(text) + 1):
                if rec(ti + 1, k):
                    memo[key] = True
                    return True
            memo[key] = False
            return False
        if si == len(text):
            memo[key] = False
            return False
        ch = text[si]
        if kind == "lit":
            ok = ch == tokens[ti][1]
        elif kind == "any":
            ok = True
        else:
            _, neg, chars = tokens[ti]
            ok = (ch in chars) != neg
            if ch == "/":
                ok = False
        if not ok:
            memo[key] = False
            return False
        memo[key] = rec(ti + 1, si + 1)
        return memo[key]

    return rec(0, 0)
