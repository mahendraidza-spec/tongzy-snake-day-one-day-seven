// Entry for the make.fun "Day one, day seven" TikTok bounty (Node 22, stdlib only).
//
// The entry is the video itself: a short TikTok about the same tiny
// agent-built game (Tongzy Snake, see snake-game.html) on the day it was
// made and after a week of daily updates, ending with make.fun's referral
// end card carrying the entrant's referral code, posted publicly on TikTok
// with the bounty's line and play code in its caption.
//
// All this program has to do is hand the video's address to the gate: it
// copies VIDEO.json from the repository root to /output/VIDEO.json, where
// the gate reads it. Nothing it writes about the video is scored — the
// house reads the video's views and interactions from TikTok itself.
//
// Run it the way the grader does:
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts
//
// Outside the grader, MAKEFUN_BOT_DIR and MAKEFUN_OUTPUT_DIR stand in for
// /bot and /output. No network, no wall clock, no files outside the repo.

import { copyFileSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';

const BOT_DIR = process.env.MAKEFUN_BOT_DIR ?? '/bot';
const OUTPUT_DIR = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';

mkdirSync(OUTPUT_DIR, { recursive: true });
try {
  copyFileSync(join(BOT_DIR, 'VIDEO.json'), join(OUTPUT_DIR, 'VIDEO.json'));
} catch (err) {
  console.error(`VIDEO.json could not be copied from ${BOT_DIR}: ${(err as Error).message}`);
  process.exit(1);
}
