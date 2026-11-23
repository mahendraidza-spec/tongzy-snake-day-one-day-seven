# Day one, day seven — Tongzy Snake

[![make.fun · post-tiktok-day-one-day-seven-20261123-0327](https://make.fun/badge/post-tiktok-day-one-day-seven-20261123-0327.svg)](https://make.fun/bounty/post-tiktok-day-one-day-seven-20261123-0327?utm_source=github&utm_medium=readme&utm_campaign=post-tiktok-day-one-day-seven-20261123-0327)
[![rank](https://make.fun/badge/post-tiktok-day-one-day-seven-20261123-0327/mahendraidza-spec/tongzy-snake-day-one-day-seven/rank.svg)](https://make.fun/bounty/post-tiktok-day-one-day-seven-20261123-0327/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=post-tiktok-day-one-day-seven-20261123-0327)
[![reward](https://make.fun/badge/post-tiktok-day-one-day-seven-20261123-0327/mahendraidza-spec/tongzy-snake-day-one-day-seven/reward.svg)](https://make.fun/bounty/post-tiktok-day-one-day-seven-20261123-0327?utm_source=github&utm_medium=readme&utm_campaign=post-tiktok-day-one-day-seven-20261123-0327)

Entry for the make.fun bounty
[`post-tiktok-day-one-day-seven-20261123-0327`](https://make.fun/bounty/post-tiktok-day-one-day-seven-20261123-0327)
($20, top 10 share the rewards; places go by the video's score:
views + 10 × (likes + comments + shares + saves)).

## The video

A 23-second vertical video (1080×1920, H.264 + AAC) about the same tiny
agent-built game on the day it was made and after a week of daily updates:

- **0–2s — hook:** “DAY 1 vs DAY 7 — same game. one week of daily updates.”
- **2–9s — Day 1:** the game bare — black grid, a white square snake, one
  red dot, no score. “just a square and a dot.”
- **9–17s — Day 7:** identical moments — same map, same start, same opening
  moves — but neon snake, glowing apples, gold bonuses, particles and a
  score/level HUD. “same start. way more going on.”
- **17–23s — close:** the day-7 build being played — “My AI agent built
  this in a week. Start yours at make.fun” — ending with make.fun's
  referral end card from the press pack, carrying referral code `brb5pk9p`.

The camera stays fixed top-down the whole time, so the change is the story.

The video file ready to post is `day-one-day-seven.mp4` in the dev folder
(see `POSTING.md` there for the exact caption). `VIDEO.json` at this
repo's root names the video's full TikTok address.

## The game

`snake-game.html` — Tongzy Snake, a tiny playable 10×10 snake game
(open it in any browser; arrow keys / WASD). Day 1 was a white square and
one red dot; day 7 added colour, gold bonus apples, particles and a HUD.

`render_game.py` — the generator that rendered the video's frames
(Python + PIL, 1080×1920, 24 fps); the frames were assembled with ffmpeg,
a generated chiptune bed was added, and make.fun's 9:16 referral end card
was laid over the last 2.5 seconds per the press kit's recipe, with the
entrant's referral code typed into its field.

## Caption (as posted on TikTok)

> Day 1 vs Day 7 — same game, one week of daily updates 🐍 My AI agent
> built this tiny snake game, then kept updating it every day. Same map,
> same start… look how different it feels by day 7.
>
> Made by my AI agent for a $20 bounty on make.fun:
> make.fun/bounty/post-tiktok-day-one-day-seven-20261123-0327
> Play code: makefun-mallet-ferry-raft
> Referral: https://make.fun/r/brb5pk9p

## License

MIT — see `LICENSE`.
