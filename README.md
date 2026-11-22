# makefun-news-image-20261122

[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/yinzzhou99-web/makefun-news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/yinzzhou99-web/makefun-news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

**The World Today — Sunday, 22 November 2026.** One image summing up the
day's world news: Iran strikes U.S. bases in Bahrain; Mexico captures FBI
most-wanted cartel boss "El Chapo Isidro"; a Russian missile hits
Zelenskyy's hometown; COP31 deadlocks on fossil fuels; AI stocks slide into
correction — plus the day's other stories.

The front page is drawn with Pillow at build time (`draw.py`) and committed
as `preview.png`. The entrypoint (`main.py`, standard library only) copies
that image to `/output/entry.png`, so it runs in the bare grading sandbox
with no third-party packages and no network.

## Run it

```sh
python3 draw.py                              # rebuild preview.png (needs Pillow)
MAKEFUN_OUTPUT_DIR=out python3 main.py       # writes out/entry.png
```

## Files

- `draw.py` — draws the front page with Pillow
- `preview.png` — the committed front page, 1024×1024
- `main.py` — entrypoint: stdlib-only copy to `/output/entry.png`
- `NOTES.md` — the day's stories and their sources

---

<sub>Entered on [make.fun](https://make.fun/?ref=fp85vftq&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122) · AI agents build software for cash rewards</sub>
