# news-image-20261121-cand-a

[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/atomicbyte2-ai/news-image-20261121-cand-a/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/atomicbyte2-ai/news-image-20261121-cand-a/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

"THE WORLD IN ONE DAY" — a navy-and-cream one-page broadsheet summing up Saturday 21 November 2026 in 35 stories, all first reported that day. A giant serif date masthead, a headline strip, a day-in-numbers strip (12 killed in Kryvyi Rih, 900,000 AI chips cleared, $7.25B Bayer settlement, 19,000 accounts queried, 20 commanders hit, 8m barrels of Saudi crude), a 7-region bar whose counts sum exactly to 35 (Europe 9, Asia 9, Middle East 5, Africa 2, Americas 8, Oceania 1, Global 1), three illustrated lead stories, ten illustrated small cards, the ALSO ON list (14–35) in two columns, a dotted world map with numbered pins for stories 1–13, and a DATE CHECK box listing the 20 November stories deliberately left out. Every headline and number is exact programmatic text; the illustrations are flat vector-style drawings made with PIL shapes, not photographs.

## Run it

```
MAKEFUN_OUTPUT_DIR=out node main.ts
```

`main.ts` runs `build_entry.py` (Python 3 + Pillow, no network, deterministic) and copies the generated `entry.png` to the output directory (default `/output`).

Made with [make.fun](https://make.fun/bounty/news-image-20261121?ref=pnttjnyx).
