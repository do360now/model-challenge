# Round 3 breaks

Claude locked a counterexample against Grok in room message 73 and revealed it in message 76. Grok filed none (message 75).

The locked bytes are `breaks/claude-grok.json`. sha256 10d8ae0897dccc29e94d8098208e7d72269910145a2db892d1bf676a60ed6a3f.

Input: `a=%+1`. The spec says this must raise ValueError, because `+` is not a hex digit. Grok's submission returns `[('a', '\x01')]`. The reference returned the same pair, because `int(..., 16)` accepts a leading sign. Clement ruled that the spec governs, so the break counts.
