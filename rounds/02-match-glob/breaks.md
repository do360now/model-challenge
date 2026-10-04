# Round 2 breaks

Claude locked a counterexample against Grok in room message 49 and revealed it in message 51. Grok filed none.

The locked bytes are `breaks/claude-grok.json`. sha256 f28352b584090bc6110ed31511fb42ac713cd9bb5652dc9425efe13bb1955653.

Input: pattern and text are each 2000 `a` characters. The spec answer is True. The judge reference returns True. Grok's submission raises RecursionError at CPython's default recursion limit of 1000. Grok accepted the break.
