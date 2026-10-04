Round 1. Spec, hidden-test hash, and lock deadline. Protocol is the one you both signed: hash-only locks, reveal after both locks or the deadline, salted counterexample locks, mismatch or a missing lock forfeits.

normalize_path(path: str) -> str

Lexical cleanup of one path. Only `/` is a separator. Backslash, space, and newline are ordinary characters. Do not touch the filesystem, and do not expand `~`.

- Length is Python's len. If len(path) > 4096 or path contains a NUL (U+0000), raise ValueError. Otherwise do not raise.
- A path that starts with `/` is absolute. Two or more leading slashes still mean one slash. `//foo` is `/foo`, not a special prefix.
- Split on `/`. Drop empty pieces and `.`.
- `..` removes the previous real piece. On an absolute path, `..` at the root is dropped. On a relative path with nothing real behind it, it stays.
- Absolute result is `/` plus the pieces joined by `/`, or `/` if nothing is left.
- Relative result is the pieces joined by `/`, or `.` if nothing is left.
- No trailing slash except the root `/`.

Submit normalize_path.py with that function. Python 3.11 or newer. Standard library is fine. One second per call.

Lock deadline: 2026-10-04 17:00:00 UTC (19:00 Berlin). A lock is `LOCK 1 <player> normalize_path.py sha256=<hex>` and nothing else. Hash convention: UTF-8, no BOM, LF, exactly one trailing newline.

Hidden tests: test_normalize_path.py, sha256 62e04fd12638b0940a4506d5e00e4eef02455ee6c970fa059de7ea17b4b4eac6. I will push that file only after the reveal window. It imports normalize_path from normalize_path.

Your problem proposals can still land, but this is the round. No source until both locks are in.
