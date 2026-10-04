Round 2. Spec, hidden-test hash, and lock deadline. Same protocol as round 1.

match_glob(pattern: str, text: str) -> bool

Does the whole text match the pattern? No filesystem. Case sensitive. A leading dot is an ordinary character.

Submit match_glob.py with that function. Python 3.11 or newer. Standard library is fine. One second per call.

Limits. If either string contains NUL, or len of either is greater than 4096, raise ValueError. An illegal pattern raises ValueError. Otherwise return True or False, and do not raise.

Segments. Split the text on `/`. Split the pattern on `/`, and also on `\/` , which is the same separator as `/`. A segment that is exactly `**` matches zero or more text segments, including matching none, so `a/**/b` matches `a/b`, `a/x/b`, and `a/x/y/b`. `**` at the start or the end is allowed. `**` anywhere that is not a whole segment is illegal: `a**b`, `***`, `a/**b`, and `**a` all raise.

Within one segment:
- `*` matches any run of characters, including empty. It cannot cross `/`, because `/` already split the segments.
- `?` matches one character.
- `[abc]` and `[a-c]` match one character from the set. A range is inclusive by code point. If the start of a range is after the end, raise ValueError. `-` at either end of the class is literal. `]` immediately after `[` or `[!` is literal. `[!...]` is the complement. A class never matches `/`, even if `/` is listed, so `[/a]` matches `a` and `[/]` matches nothing.
- An unclosed `[`, an empty class (`[]` or `[!]`), or a trailing `\` raises ValueError.
- `\` escapes the next character, so `\*` is a literal star. `\/` is a separator, not a literal slash inside a segment.
- A `]` outside a class is literal.

Empty pattern matches only empty text. `a/` matches `a/` and not `a`. `/a` matches `/a` and not `a`. `a//b` matches `a//b` and not `a/b`.

Lock deadline: 2026-10-04 18:00:00 UTC (20:00 Berlin). A lock is `LOCK 2 <player> match_glob.py sha256=<hex>` and nothing else. Same hash convention as round 1: UTF-8, no BOM, LF, exactly one trailing newline. First lock is final.

Hidden tests: test_match_glob.py, sha256 3c6099915dc324d43d50a8b656f339f11bd776cbed81fde15f8d16c4fe45be50. It imports match_glob from match_glob. I will publish that file only after the reveal window.
