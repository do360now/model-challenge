# Scores

| Round | Problem | Claude | Grok | Notes |
| --- | --- | --- | --- | --- |
| 1 | normalize_path | 1.5 | 1.5 | Hidden tests passed for both. No breaks filed. |
| 2 | match_glob | 2 | 1 | Hidden cases 94/95 and raises 11/11 for both. Both missed `[a-c-e]` against `d`. Claude's break (`a` * 2000, RecursionError) validated. |
| Total | | 3.5 | 2.5 | |

Rank is hidden tests first, then validated breaks. A tie splits the points. Two players: 2 for first, 1 for second, 1.5 each on a tie.
