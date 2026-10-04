# Round 3 breaks

Claude locked a counterexample against Grok in room message 73 and revealed it in message 76. Grok filed none (message 75).

The locked bytes are `breaks/claude-grok.json`. sha256 10d8ae0897dccc29e94d8098208e7d72269910145a2db892d1bf676a60ed6a3f.

Input: `a=%+1`. The spec says this must raise ValueError, because `+` is not a hex digit. The reference and Grok's submission both return `[('a', '\x01')]`. `int(..., 16)` accepts a leading sign, and the reference does that too. A break counts only when the reference passes and the target fails, so this one does not count.
