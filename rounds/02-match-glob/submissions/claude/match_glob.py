"""Round 2: segment-aware glob matching (Claude).

Pattern is parsed left to right into segments. `/` and `\\/` separate
segments, except inside a character class, where `/` is just a member
(and can never match, since text segments never contain `/`).
Within a segment, stars split the tokens into fixed-length chunks that are
matched greedily (leftmost), which is exact for `*` and avoids regex
backtracking. Across segments, `**` is handled the same way one level up.
"""

import re

MAX_LEN = 4096

_LIT, _ANY, _CLS, _STAR = 0, 1, 2, 3


def _cp(c: str) -> str:
    return "\\U%08x" % ord(c)


def _parse(pattern: str):
    """Return a list of segments; each segment is a list of tokens."""
    segs = [[]]
    i, n = 0, len(pattern)
    while i < n:
        c = pattern[i]
        if c == "\\":
            if i + 1 >= n:
                raise ValueError("trailing backslash")
            nxt = pattern[i + 1]
            if nxt == "/":
                segs.append([])
            else:
                segs[-1].append((_LIT, nxt))
            i += 2
        elif c == "/":
            segs.append([])
            i += 1
        elif c == "*":
            segs[-1].append((_STAR,))
            i += 1
        elif c == "?":
            segs[-1].append((_ANY,))
            i += 1
        elif c == "[":
            tok, i = _parse_class(pattern, i)
            segs[-1].append(tok)
        else:
            segs[-1].append((_LIT, c))
            i += 1
    out = []
    for seg in segs:
        if len(seg) == 2 and seg[0][0] == _STAR and seg[1][0] == _STAR:
            out.append(None)  # None marks a `**` segment
            continue
        for a, b in zip(seg, seg[1:]):
            if a[0] == _STAR and b[0] == _STAR:
                raise ValueError("'**' must be a whole segment")
        out.append(seg)
    return out


def _parse_class(p: str, i: int):
    n = len(p)
    i += 1  # skip '['
    negate = False
    if i < n and p[i] == "!":
        negate = True
        i += 1
    items = []  # (lo, hi)
    first = True

    def read_char(j):
        if j >= n:
            raise ValueError("unclosed class")
        if p[j] == "\\":
            if j + 1 >= n:
                raise ValueError("trailing backslash")
            return p[j + 1], j + 2
        return p[j], j + 1

    while True:
        if i >= n:
            raise ValueError("unclosed class")
        if p[i] == "]" and not first:
            i += 1
            break
        first = False
        lo, i = read_char(i)
        if i + 1 < n and p[i] == "-" and p[i + 1] != "]":
            hi, i = read_char(i + 1)
            if ord(lo) > ord(hi):
                raise ValueError("reversed range")
            items.append((lo, hi))
        else:
            items.append((lo, lo))
    if not items:
        raise ValueError("empty class")
    body = "".join(_cp(a) if a == b else _cp(a) + "-" + _cp(b) for a, b in items)
    return (_CLS, negate, "[" + ("^" if negate else "") + body + "]"), i


def _chunk_matcher(tokens):
    """Fixed-length chunk -> (length, literal_or_None, compiled_regex_or_None)."""
    if all(t[0] == _LIT for t in tokens):
        return len(tokens), "".join(t[1] for t in tokens), None
    parts = []
    for t in tokens:
        if t[0] == _LIT:
            parts.append(_cp(t[1]))
        elif t[0] == _ANY:
            parts.append(".")
        else:
            parts.append(t[2])
    return len(tokens), None, re.compile("".join(parts), re.DOTALL)


class _Seg:
    __slots__ = ("chunks", "has_star")

    def __init__(self, tokens):
        groups = [[]]
        for t in tokens:
            if t[0] == _STAR:
                groups.append([])
            else:
                groups[-1].append(t)
        self.has_star = len(groups) > 1
        self.chunks = [_chunk_matcher(g) for g in groups]

    @staticmethod
    def _at(chunk, s, pos):
        length, lit, rx = chunk
        if lit is not None:
            return s.startswith(lit, pos)
        return rx.match(s, pos) is not None

    @staticmethod
    def _find(chunk, s, pos, endpos):
        length, lit, rx = chunk
        if length == 0:
            return pos if pos <= endpos else -1
        if lit is not None:
            return s.find(lit, pos, endpos)
        m = rx.search(s, pos, endpos)
        return m.start() if m else -1

    def match(self, s: str) -> bool:
        chunks = self.chunks
        if not self.has_star:
            c = chunks[0]
            return len(s) == c[0] and self._at(c, s, 0)
        first, last = chunks[0], chunks[-1]
        end = len(s) - last[0]
        if first[0] > end or not self._at(first, s, 0):
            return False
        pos = first[0]
        for c in chunks[1:-1]:
            k = self._find(c, s, pos, end)
            if k < 0:
                return False
            pos = k + c[0]
        return pos <= end and self._at(last, s, end)


def match_glob(pattern: str, text: str) -> bool:
    for v in (pattern, text):
        if len(v) > MAX_LEN or "\x00" in v:
            raise ValueError("input too long or contains NUL")

    segs = [None if s is None else _Seg(s) for s in _parse(pattern)]
    tsegs = text.split("/")

    cache = {}

    def seg_ok(k, t):
        key = (k, t)
        r = cache.get(key)
        if r is None:
            r = cache[key] = segs[k].match(t)
        return r

    # groups of consecutive non-** segment indices, split by **
    groups = [[]]
    for k, s in enumerate(segs):
        if s is None:
            groups.append([])
        else:
            groups[-1].append(k)

    def group_at(g, i):
        return all(seg_ok(k, tsegs[i + off]) for off, k in enumerate(g))

    n = len(tsegs)
    if len(groups) == 1:
        g = groups[0]
        return len(g) == n and group_at(g, 0)

    first, last = groups[0], groups[-1]
    end = n - len(last)
    if len(first) > end or not group_at(first, 0):
        return False
    pos = len(first)
    for g in groups[1:-1]:
        L = len(g)
        i = pos
        while i + L <= end and not group_at(g, i):
            i += 1
        if i + L > end:
            return False
        pos = i + L
    return pos <= end and group_at(last, end)
