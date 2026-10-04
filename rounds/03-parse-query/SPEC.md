Round 3 spec, hidden-test hash, and lock deadline. Same protocol as rounds 1 and 2.

parse_query(query: str) -> list[tuple[str, str]]

Parse one application/x-www-form-urlencoded query into pairs, in order. This is not a URL parser. Do not cut on #, do not treat ; as a separator, and do not fetch anything.

Submit parse_query.py with that function. Python 3.11 or newer. Standard library is fine. One second per call.

Limits, checked on the input string before any decoding. If query contains a NUL character, or len(query) is greater than 4096, raise ValueError. A query of length 4096 is allowed. A decoded %00 is a NUL inside a key or value and does not raise.

Leading question mark. If query starts with ?, strip exactly one. A later ? is an ordinary character. If the string is empty after that strip, return []. So both "" and "?" return [].

Pairs. Split the remaining string on &. Every piece is a pair, including empty ones, so "&" is two pairs and "&&" is three. In each piece, the first = separates the key from the value. Extra = characters stay in the value, so a=b=c is ("a", "b=c"). If there is no =, the value is "". Keys and values may be empty. Order is kept. Duplicate keys are not merged.

Decoding, applied to the key and to the value separately. Build a byte buffer, then decode it as strict UTF-8. If that fails, raise ValueError.
- A raw + contributes the byte 0x20, a space.
- % and the next two characters are one byte. The two characters are hexadecimal, case insensitive. %2b and %2B are both the byte 0x2B, which is a plus sign, not a space. A plus that comes from percent-decoding stays a plus.
- If % is not followed by two hex digits, raise ValueError. That includes a trailing %, a single digit, and %zz.
- Any other character, including space, tab, #, ;, and non-ASCII characters, is encoded as UTF-8 and those bytes are appended.
- The finished buffer must be valid UTF-8. Invalid sequences raise ValueError, including a lone continuation byte, an unfinished multibyte sequence, an overlong encoding, and an encoded surrogate.

Lock deadline: 2026-10-04 20:00:00 UTC (22:00 Berlin). A lock is `LOCK 3 <player> parse_query.py sha256=<hex>` and nothing else. Same hash convention: UTF-8, no BOM, LF, exactly one trailing newline. First lock is final.

Hidden tests: test_parse_query.py, sha256 d0cf1e7576e81d5228ac58205598cc31f17d0f6d214064fa60bfed1c16808e55. It imports parse_query from parse_query. I will publish that file only after the reveal window.
