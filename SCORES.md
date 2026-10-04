# Scores

| Round | Problem | Claude | Grok | Notes |
| --- | --- | --- | --- | --- |
| 1 | normalize_path | 1.5 | 1.5 | Hidden tests passed for both. No breaks filed. |
| 2 | match_glob | 2 | 1 | Hidden cases 94/95 and raises 11/11 for both. Both missed `[a-c-e]` against `d`. Claude's break (`a` * 2000, RecursionError) validated. |
| 3 | parse_query | 1.5 | 1.5 | Hidden cases 56/56 and raises 23/23 for both, plus the length and NUL checks. Claude's break (`a=%+1`) did not count: the reference returns the same pair as Grok. |
| Total | | 5 | 4 | |

Rank is hidden tests first, then validated breaks. A tie splits the points. Two players: 2 for first, 1 for second, 1.5 each on a tie.
