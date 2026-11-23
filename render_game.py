#!/usr/bin/env python3
"""Render frames for 'Tongzy Snake' — day one vs day seven TikTok video.

Game: a tiny snake game built by the agent. Same 10x10 map, same start
(2,5), same opening moves in both versions; only the build changes.
Day 1: bare black grid, white square snake, one red dot, no score.
Day 7: neon snake, glowing apples, particles, score/level HUD, faster.
Camera stays fixed top-down the whole time: the change is the story.

Output: frames/frame_%04d.png, 1080x1920, 24 fps.
Segments: title 2.0s | day1 7.0s | day7 8.0s | close 6.0s = 23.0s total.
"""
import math, os, random
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1920
FPS = 24
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "frames")
os.makedirs(OUT, exist_ok=True)

F_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
F_MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"

def font(path, size):
    return ImageFont.truetype(path, size)

# ---- playfield ----
GX, GY, CELL, N = 60, 540, 96, 10   # 960x960 board

# Closed rectangular loop, 16 steps per cycle, no self-collision ever.
LOOP = []
x, y = 2, 5
LOOP.append((x, y))
for _ in range(5): x += 1; LOOP.append((x, y))       # -> (7,5)
for _ in range(3): y += 1; LOOP.append((x, y))       # -> (7,8)
for _ in range(5): x -= 1; LOOP.append((x, y))       # -> (2,8)
for _ in range(3): y -= 1; LOOP.append((x, y))       # -> (2,5)
LOOP = LOOP[:-1]  # 16 cells, index wraps
assert len(LOOP) == 16, len(LOOP)
assert LOOP[0] == (2, 5)

# Apples on the loop, in eat order (step index within first cycle, then repeat).
APPLES = [((5, 5), "red", 3), ((7, 6), "gold", 6), ((4, 8), "red", 11), ((2, 7), "gold", 14)]
APPLE_STEP = {s: (pos, kind) for pos, kind, s in APPLES}

def head_at(step):
    return LOOP[step % 16]

def body_cells(step, length):
    # most recent `length` cells ending at head
    return [LOOP[(step - i) % 16] for i in range(length)]

def check_no_collision(max_step, max_len):
    for s in range(max_step + 1):
        b = body_cells(s, max_len)
        assert len(set(b)) == len(b), f"collision at step {s}: {b}"

check_no_collision(60, 10)

def cell_px(cx, cy):
    return GX + cx * CELL, GY + cy * CELL

def lerp(a, b, t):
    return a + (b - a) * t

def smooth_pos(step_float):
    """Interpolated head position in cell coords (float)."""
    s = int(math.floor(step_float))
    f = step_float - s
    # ease slightly so motion reads smooth, not robotic
    f = f * f * (3 - 2 * f)
    x0, y0 = head_at(s)
    x1, y1 = head_at(s + 1)
    return lerp(x0, x1, f), lerp(y0, y1, f)

# ---- drawing helpers ----
def text_center(d, cx, y, s, fnt, fill):
    w = d.textlength(s, font=fnt)
    d.text((cx - w / 2, y), s, font=fnt, fill=fill)

def draw_snake(d, step_float, length, neon):
    s = int(math.floor(step_float))
    cells = body_cells(s, length)
    hx, hy = smooth_pos(step_float)
    # draw tail->head so head is on top
    for i, (cx, cy) in enumerate(reversed(cells)):
        px, py = cell_px(cx, cy)
        pad = 6 if not neon else 4
        if i == len(cells) - 1:
            # head: interpolated position
            px = GX + hx * CELL
            py = GY + hy * CELL
        if neon:
            # glow underlay
            d.rounded_rectangle([px - 2, py - 2, px + CELL - 2 + 4, py + CELL - 2 + 4],
                                radius=18, fill=(57, 255, 106, 60))
            col = (190, 255, 200) if i == len(cells) - 1 else (57, 255, 106)
            d.rounded_rectangle([px + pad, py + pad, px + CELL - pad, py + CELL - pad],
                                radius=16, fill=col)
            if i == len(cells) - 1:
                ex, ey = px + CELL * 0.30, py + CELL * 0.34
                d.ellipse([ex, ey, ex + 16, ey + 16], fill=(11, 16, 38))
                ex2 = px + CELL * 0.58
                d.ellipse([ex2, ey, ex2 + 16, ey + 16], fill=(11, 16, 38))
        else:
            col = (255, 255, 255) if i == len(cells) - 1 else (235, 235, 235)
            d.rectangle([px + pad, py + pad, px + CELL - pad, py + CELL - pad], fill=col)
            if i == len(cells) - 1:
                ex, ey = px + CELL * 0.30, py + CELL * 0.34
                d.ellipse([ex, ey, ex + 14, ey + 14], fill=(0, 0, 0))
                ex2 = px + CELL * 0.58
                d.ellipse([ex2, ey, ex2 + 14, ey + 14], fill=(0, 0, 0))

def draw_apple(d, pos, kind, t_now, neon):
    px, py = cell_px(*pos)
    cx, cy = px + CELL / 2, py + CELL / 2
    r = 30 + (4 * math.sin(t_now * 6) if neon else 0)
    if kind == "gold":
        col, hi = (255, 214, 10), (255, 240, 150)
    else:
        col, hi = (229, 72, 77), (255, 150, 150)
    if neon:
        d.ellipse([cx - r - 8, cy - r - 8, cx + r + 8, cy + r + 8], fill=col + (70,) if False else (255, 80, 60, 40) if kind == "red" else (255, 214, 10, 40))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col)
    d.ellipse([cx - r * 0.45, cy - r * 0.55, cx - r * 0.05, cy - r * 0.15], fill=hi)
    d.arc([cx - 6, cy - r - 14, cx + 14, cy - r + 6], start=200, end=340, fill=(80, 200, 90), width=5)

class Particles:
    def __init__(self):
        self.parts = []  # (x, y, vx, vy, born, life, color)
    def burst(self, pos, t_now, kind):
        px, py = cell_px(*pos)
        cx, cy = px + CELL / 2, py + CELL / 2
        rnd = random.Random(hash((pos, t_now)) & 0xffff)
        cols = [(255, 214, 10), (255, 120, 60), (57, 255, 106), (255, 255, 255)] if kind == "gold" \
            else [(229, 72, 77), (255, 150, 150), (255, 255, 255)]
        for _ in range(16):
            ang = rnd.uniform(0, 6.283)
            sp = rnd.uniform(60, 320)
            self.parts.append((cx, cy, math.cos(ang) * sp, math.sin(ang) * sp,
                               t_now, rnd.uniform(0.4, 0.7), rnd.choice(cols)))
    def draw(self, d, t_now):
        keep = []
        for (x, y, vx, vy, born, life, col) in self.parts:
            age = t_now - born
            if age > life:
                continue
            keep.append((x, y, vx, vy, born, life, col))
            nx, ny = x + vx * age, y + vy * age + 140 * age * age
            a = int(255 * (1 - age / life))
            r = max(2, int(9 * (1 - age / life)))
            d.ellipse([nx - r, ny - r, nx + r, ny + r], fill=col)
        self.parts = keep

# ---- segments ----
TITLE_S, DAY1_S, DAY7_S, CLOSE_S = 2.0, 7.0, 8.0, 6.0
TOTAL_S = TITLE_S + DAY1_S + DAY7_S + CLOSE_S  # 23.0
N_FRAMES = int(TOTAL_S * FPS)
print(f"total {TOTAL_S}s -> {N_FRAMES} frames")

DAY1_STEP = 0.45   # seconds per grid step, day 1 (slow, bare)
DAY7_STEP = 0.32   # day 7 (faster)

particles = Particles()
day7_eaten = []  # (step, kind)
day1_eaten = False

def band(d, y0, y1, alpha=150):
    ov = Image.new("RGBA", (W, y1 - y0), (0, 0, 0, alpha))
    d._image.paste(ov, (0, y0), ov)

def draw_board(d, neon, t_now):
    if neon:
        d.rectangle([0, 0, W, H], fill=(11, 16, 38))
        # soft vignette dots
        rnd = random.Random(7)
        for _ in range(40):
            x = rnd.uniform(0, W); y = rnd.uniform(0, H)
            r = rnd.uniform(2, 5)
            d.ellipse([x - r, y - r, x + r, y + r], fill=(120, 140, 255, 26))
        for i in range(N + 1):
            x = GX + i * CELL
            d.line([x, GY, x, GY + N * CELL], fill=(38, 52, 96), width=2)
            yy = GY + i * CELL
            d.line([GX, yy, GX + N * CELL, yy], fill=(38, 52, 96), width=2)
        d.rectangle([GX - 6, GY - 6, GX + N * CELL + 6, GY + N * CELL + 6],
                    outline=(0, 229, 255), width=5)
    else:
        d.rectangle([0, 0, W, H], fill=(0, 0, 0))
        for i in range(N + 1):
            x = GX + i * CELL
            d.line([x, GY, x, GY + N * CELL], fill=(34, 34, 34), width=2)
            yy = GY + i * CELL
            d.line([GX, yy, GX + N * CELL, yy], fill=(34, 34, 34), width=2)
        d.rectangle([GX - 4, GY - 4, GX + N * CELL + 4, GY + N * CELL + 4],
                    outline=(90, 90, 90), width=3)

def frame_title(i):
    img = Image.new("RGB", (W, H), (11, 16, 38))
    d = ImageDraw.Draw(img, "RGBA")
    # magenta glow bar
    d.rectangle([0, 880, W, 896], fill=(196, 28, 131))
    pulse = 1 + 0.04 * math.sin(i / FPS * 4)
    f1 = font(F_BOLD, int(106 * pulse))
    text_center(d, W // 2, 620, "DAY 1 vs DAY 7", f1, (255, 255, 255))
    text_center(d, W // 2, 940, "same game. one week", font(F_BOLD, 62), (201, 209, 255))
    text_center(d, W // 2, 1020, "of daily updates.", font(F_BOLD, 62), (201, 209, 255))
    text_center(d, W // 2, 1180, "built by my AI agent", font(F_BOLD, 46), (140, 150, 190))
    # tiny snake preview
    for k in range(4):
        px = W // 2 - 120 + k * 62
        d.rounded_rectangle([px, 1420, px + 52, 1472], radius=12,
                            fill=(57, 255, 106) if k == 3 else (255, 255, 255))
    d.ellipse([W // 2 + 150, 1432, W // 2 + 190, 1472], fill=(229, 72, 77))
    return img

def frame_day1(t):
    img = Image.new("RGB", (W, H), (0, 0, 0))
    d = ImageDraw.Draw(img, "RGBA")
    draw_board(d, neon=False, t_now=t)
    step_f = t / DAY1_STEP
    s = int(math.floor(step_f))
    # day 1: exactly one apple, at (5,5); eaten at step 3, never respawns
    if s < 3:
        draw_apple(d, (5, 5), "red", t, neon=False)
    length = 3 + (1 if s >= 3 else 0)
    draw_snake(d, step_f, length, neon=False)
    text_center(d, 200, 180, "DAY 1", font(F_BOLD, 64), (150, 150, 150))
    d.text((W - 200, 180), "", font=font(F_BOLD, 40), fill=(150, 150, 150))
    band(d, 1560, 1760, 140)
    text_center(d, W // 2, 1600, "just a square", font(F_BOLD, 58), (200, 200, 200))
    text_center(d, W // 2, 1670, "and a dot.", font(F_BOLD, 58), (200, 200, 200))
    return img

def frame_day7(t, close=False):
    img = Image.new("RGB", (W, H), (11, 16, 38))
    d = ImageDraw.Draw(img, "RGBA")
    draw_board(d, neon=True, t_now=t)
    step_f = t / DAY7_STEP
    s = int(math.floor(step_f))
    # apples: cycle of 4, eaten in order; next one shows
    eaten_steps = [st for _, _, st in APPLES]
    # how many full cycles done
    cycle = s // 16
    idx = None
    score = 0
    # count eats up to current step across cycles
    eats = 0
    for c in range(cycle + 1):
        for (pos, kind, ast) in APPLES:
            st = c * 16 + ast
            if st <= s:
                eats += 1
                score += 50 if kind == "gold" else 10
            elif idx is None and c == cycle:
                idx = (pos, kind, st)
    if idx is None:  # between cycles, next apple is first of next cycle
        pos, kind, ast = APPLES[0]
        idx = (pos, kind, (cycle + 1) * 16 + ast)
    # burst particles on eat steps (once per step)
    for c in range(cycle + 1):
        for (pos, kind, ast) in APPLES:
            st = c * 16 + ast
            if st == s and abs(step_f - st) < 0.06:
                particles.burst(pos, t, kind)
    draw_apple(d, idx[0], idx[1], t, neon=True)
    length = min(3 + eats, 10)
    draw_snake(d, step_f, length, neon=True)
    particles.draw(d, t)
    # HUD (skipped in the close: the top band carries the message instead)
    if not close:
        level = 1 + score // 60
        d.text((60, 150), f"SCORE {score}", font=font(F_MONO, 58), fill=(255, 255, 255))
        d.text((60, 230), f"LEVEL {level}", font=font(F_MONO, 48), fill=(57, 255, 106))
        # DAY 7 pill top-right
        pill = "DAY 7"
        fw = d.textlength(pill, font=font(F_BOLD, 52))
        d.rounded_rectangle([W - 60 - fw - 50, 150, W - 60, 150 + 84], radius=42, fill=(196, 28, 131))
        d.text((W - 60 - fw - 25, 168), pill, font=font(F_BOLD, 52), fill=(255, 255, 255))
    if close:
        band(d, 60, 420, 160)
        text_center(d, W // 2, 120, "My AI agent built this", font(F_BOLD, 62), (255, 255, 255))
        text_center(d, W // 2, 200, "in a week.", font(F_BOLD, 62), (255, 255, 255))
        text_center(d, W // 2, 300, "same map. same start.", font(F_BOLD, 46), (201, 209, 255))
        band(d, 1560, 1760, 160)
        text_center(d, W // 2, 1600, "Start yours at make.fun", font(F_BOLD, 60), (255, 255, 255))
    else:
        band(d, 1560, 1760, 140)
        text_center(d, W // 2, 1600, "same start.", font(F_BOLD, 58), (255, 255, 255))
        text_center(d, W // 2, 1670, "way more going on.", font(F_BOLD, 58), (57, 255, 106))
    return img

for i in range(N_FRAMES):
    t = i / FPS
    if t < TITLE_S:
        img = frame_title(i)
    elif t < TITLE_S + DAY1_S:
        img = frame_day1(t - TITLE_S)
    elif t < TITLE_S + DAY1_S + DAY7_S:
        img = frame_day7(t - TITLE_S - DAY1_S, close=False)
    else:
        img = frame_day7(t - TITLE_S - DAY1_S + 0.0, close=True)  # day7 clock keeps running
        # note: close continues the same day-7 timeline (no reset)
    img.save(os.path.join(OUT, f"frame_{i:04d}.png"))
    if i % 120 == 0:
        print(f"frame {i}/{N_FRAMES}")

print("DONE", N_FRAMES, "frames in", OUT)
