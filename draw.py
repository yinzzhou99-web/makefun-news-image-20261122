"""Draw the front page of The World Today for Sunday, 22 November 2026.

Renders a 1024x1024 newspaper front page with Pillow at build time and
writes preview.png next to this file. Run: python3 draw.py
"""
import math
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1024, 1024

PAPER = (247, 243, 234)
INK = (18, 18, 18)
RULE = (18, 18, 18)
MUTED = (90, 86, 76)
ACCENT = (158, 32, 24)
NAVY = (11, 30, 58)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_I = "/usr/share/fonts/truetype/noto/NotoSerif-Italic.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Wrap text into lines no wider than max_w pixels."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, xy, lines, fnt, fill=INK, leading=None, align="left"):
    x, y = xy
    lh = leading or int(fnt.size * 1.18)
    for line in lines:
        if align == "center":
            draw.text((W // 2, y), line, font=fnt, fill=fill, anchor="ma")
        else:
            draw.text((x, y), line, font=fnt, fill=fill)
        y += lh
    return y


def rule(draw, y, x0=32, x1=W - 32, width=2, fill=RULE):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def gradient(draw, box, top, bottom):
    x0, y0, x1, y1 = box
    span = max(1, y1 - y0)
    for yy in range(y0, y1):
        t = (yy - y0) / span
        col = tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3))
        draw.line([(x0, yy), (x1, yy)], fill=col)


def burst(draw, cx, cy, r, core=(255, 214, 120), mid=(255, 140, 40),
          edge=(220, 60, 20)):
    for rad, col in ((r, edge), (int(r * 0.66), mid), (int(r * 0.36), core)):
        draw.ellipse([cx - rad, cy - rad, cx + rad, cy + rad], fill=col)
    for ang in range(0, 360, 30):
        a = math.radians(ang)
        x2 = cx + int(math.cos(a) * r * 1.35)
        y2 = cy + int(math.sin(a) * r * 1.35)
        draw.line([(cx, cy), (x2, y2)], fill=mid, width=3)


def streak(draw, x0, y0, x1, y1):
    draw.line([(x0, y0), (x1, y1)], fill=(255, 170, 60), width=7)
    draw.line([(x0, y0), (x1, y1)], fill=(255, 240, 200), width=2)
    draw.ellipse([x1 - 6, y1 - 6, x1 + 6, y1 + 6], fill=(255, 240, 200))

def lead_photo(draw, box):
    """Night skyline over the Gulf: missile streaks, fire, a warship."""
    x0, y0, x1, y1 = box
    gradient(draw, box, (8, 20, 46), (38, 74, 116))
    horizon = y0 + int((y1 - y0) * 0.62)
    # Stars.
    stars = [(60, 30), (150, 55), (260, 26), (350, 70), (470, 34),
             (560, 58), (700, 28), (820, 62), (920, 30), (990, 80),
             (420, 90), (640, 100), (880, 110), (200, 100)]
    for sx, sy in stars:
        draw.ellipse([x0 + sx - 2, y0 + sy - 2, x0 + sx + 2, y0 + sy + 2],
                     fill=(220, 230, 245))
    # Skyline silhouettes.
    skyline = [(0, 150, 60, 150), (60, 110, 46, 120), (106, 170, 70, 90),
               (176, 90, 54, 130), (230, 140, 66, 100), (296, 120, 40, 115),
               (336, 160, 78, 95), (414, 100, 48, 125), (462, 145, 72, 100),
               (534, 115, 44, 118), (578, 165, 80, 92), (658, 95, 50, 128),
               (708, 140, 64, 100), (772, 120, 42, 115), (814, 170, 74, 90),
               (888, 105, 52, 122), (940, 150, 84, 95)]
    for bx, bw, bh, _ in skyline:
        draw.rectangle([x0 + bx, horizon - bh, x0 + bx + bw, horizon],
                       fill=(10, 16, 30))
    # Lit windows.
    for bx, bw, bh, _ in skyline:
        for wy in range(horizon - bh + 12, horizon - 8, 18):
            for wx in range(bx + 8, bx + bw - 6, 16):
                if (wx * 7 + wy * 13) % 5 < 2:
                    draw.rectangle([x0 + wx, wy, x0 + wx + 5, wy + 7],
                                   fill=(255, 205, 110))
    # Twin sail towers.
    draw.polygon([(x0 + 700, horizon), (x0 + 726, horizon - 132),
                  (x0 + 752, horizon)], fill=(14, 22, 40))
    draw.polygon([(x0 + 756, horizon), (x0 + 782, horizon - 132),
                  (x0 + 808, horizon)], fill=(14, 22, 40))
    # Sea.
    draw.rectangle([x0, horizon, x1, y1], fill=(9, 26, 52))
    for yy in range(horizon + 6, y1 - 4, 12):
        draw.line([(x0 + 20, yy), (x1 - 20, yy)], fill=(24, 52, 92), width=2)
    # Warship silhouette.
    draw.polygon([(x0 + 90, y1 - 26), (x0 + 250, y1 - 26),
                  (x0 + 235, y1 - 12), (x0 + 105, y1 - 12)],
                 fill=(22, 44, 74))
    draw.rectangle([x0 + 150, y1 - 52, x0 + 170, y1 - 26], fill=(22, 44, 74))
    draw.rectangle([x0 + 186, y1 - 44, x0 + 196, y1 - 26], fill=(22, 44, 74))
    draw.line([(x0 + 90, y1 - 26), (x0 + 250, y1 - 26)],
              fill=(120, 150, 190), width=2)
    # Explosions and missile streaks.
    burst(draw, x0 + 560, horizon - 60, 34)
    burst(draw, x0 + 880, horizon - 30, 24)
    streak(draw, x0 + 950, y0 + 18, x0 + 890, horizon - 42)
    streak(draw, x0 + 620, y0 + 40, x0 + 566, horizon - 66)
    streak(draw, x0 + 420, y0 + 12, x0 + 380, horizon - 96)
    # Smoke.
    for cx, cy, r in ((x0 + 560, horizon - 110, 30), (x0 + 600, horizon - 130, 22),
                      (x0 + 880, horizon - 70, 24)):
        draw.ellipse([cx - r, cy - r // 2, cx + r, cy + r // 2],
                     fill=(70, 74, 84))


def thumb_mexico(draw, box):
    x0, y0, x1, y1 = box
    gradient(draw, box, (214, 138, 60), (122, 52, 32))
    draw.ellipse([x1 - 42, y0 + 8, x1 - 6, y0 + 44], fill=(255, 226, 150))
    draw.polygon([(x0, y1), (x0 + 40, y0 + 58), (x0 + 90, y1)],
                 fill=(96, 44, 26))
    draw.polygon([(x0 + 70, y1), (x0 + 120, y0 + 44), (x0 + 170, y1)],
                 fill=(80, 36, 22))
    draw.rectangle([x0 + 118, y0 + 52, x0 + 126, y0 + 84], fill=(46, 92, 46))
    draw.rectangle([x0 + 104, y0 + 58, x0 + 118, y0 + 66], fill=(46, 92, 46))
    draw.rectangle([x0 + 104, y0 + 58, x0 + 110, y0 + 72], fill=(46, 92, 46))
    draw.rectangle([x0 + 126, y0 + 70, x0 + 140, y0 + 78], fill=(46, 92, 46))
    draw.rectangle([x0 + 134, y0 + 70, x0 + 140, y0 + 84], fill=(46, 92, 46))
    # Badge star.
    cx, cy = x0 + 52, y0 + 66
    pts = []
    for i in range(10):
        a = math.radians(-90 + i * 36)
        r = 20 if i % 2 == 0 else 8
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    draw.polygon(pts, fill=(255, 214, 120), outline=(120, 80, 10))


def thumb_ukraine(draw, box):
    x0, y0, x1, y1 = box
    gradient(draw, box, (30, 44, 78), (90, 90, 110))
    horizon = y0 + 62
    for bx, bw, bh in ((0, 34, 34), (36, 26, 48), (64, 40, 30), (106, 30, 44)):
        draw.rectangle([x0 + bx, horizon - bh, x0 + bx + bw, horizon],
                       fill=(16, 20, 34))
    burst(draw, x0 + 78, horizon - 26, 18)
    streak(draw, x0 + 140, y0 + 8, x0 + 118, horizon - 30)
    draw.rectangle([x0, horizon, x1, y1], fill=(52, 52, 58))
    for cx, cy, r in ((x0 + 78, horizon - 52, 14), (x0 + 104, horizon - 62, 10)):
        draw.ellipse([cx - r, cy - r // 2, cx + r, cy + r // 2],
                     fill=(96, 96, 104))


def thumb_climate(draw, box):
    x0, y0, x1, y1 = box
    gradient(draw, box, (16, 88, 110), (40, 140, 130))
    cx, cy, r = x0 + 72, y0 + 52, 38
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(24, 90, 110),
                 outline=(210, 235, 220), width=3)
    draw.arc([cx - r, cy - r, cx + r, cy + r], 200, 340, fill=(210, 235, 220),
             width=3)
    draw.ellipse([cx - 16, cy - 22, cx - 2, cy - 8], fill=(90, 170, 120))
    draw.ellipse([cx + 4, cy + 6, cx + 20, cy + 20], fill=(90, 170, 120))
    # Thermometer.
    draw.rectangle([x0 + 118, y0 + 18, x0 + 128, y0 + 74], fill=(240, 240, 230))
    draw.ellipse([x0 + 110, y0 + 68, x0 + 136, y0 + 94], fill=(220, 60, 40))
    draw.rectangle([x0 + 121, y0 + 30, x0 + 125, y0 + 74], fill=(220, 60, 40))


def thumb_markets(draw, box):
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(238, 238, 232))
    for gx in range(x0 + 12, x1, 18):
        draw.line([(gx, y0 + 6), (gx, y1 - 6)], fill=(214, 214, 206), width=1)
    for gy in range(y0 + 12, y1, 18):
        draw.line([(x0 + 6, gy), (x1 - 6, gy)], fill=(214, 214, 206), width=1)
    pts = [(x0 + 10, y0 + 22), (x0 + 40, y0 + 30), (x0 + 66, y0 + 26),
           (x0 + 92, y0 + 48), (x0 + 118, y0 + 62), (x0 + 142, y0 + 84)]
    draw.line(pts, fill=(178, 34, 24), width=5, joint="curve")
    draw.polygon([(pts[-1][0], pts[-1][1]), (pts[-1][0] - 12, pts[-1][1] - 2),
                  (pts[-1][0] - 2, pts[-1][1] + 12)], fill=(178, 34, 24))
    draw.text((x0 + 10, y0 + 70), "-3.7%", font=font(SANS_B, 24),
              fill=(178, 34, 24))


def story_cell(draw, x, y, w, thumb_fn, kicker, headline, deck):
    tw, th = 150, 104
    thumb_fn(draw, (x, y + 4, x + tw, y + 4 + th))
    tx = x + tw + 14
    draw.text((tx, y), kicker, font=font(SANS_B, 17), fill=ACCENT)
    hy = y + 24
    hl = wrap(draw, headline, font(SERIF_B, 23), w - tw - 14)
    hy = text_block(draw, (tx, hy), hl, font(SERIF_B, 23), leading=27)
    dl = wrap(draw, deck, font(SANS, 17), w - tw - 14)
    text_block(draw, (tx, hy + 2), dl, font(SANS, 17), leading=21)


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    # Masthead.
    d.text((W // 2, 14), "THE WORLD TODAY", font=font(SERIF_B, 82),
           fill=INK, anchor="ma")
    rule(d, 104, width=3)
    d.text((32, 114), "SUNDAY, 22 NOVEMBER 2026", font=font(SANS_B, 25),
           fill=INK)
    d.text((W - 32, 114), "ONE DAY  ·  ONE IMAGE", font=font(SANS_B, 25),
           fill=INK, anchor="ra")
    rule(d, 146, width=1)
    d.text((W // 2, 152), "Every story on this page happened, or was first "
           "reported, on Sunday, 22 November 2026.",
           font=font(SERIF_I, 19), fill=MUTED, anchor="ma")
    # Lead photo and caption.
    lead_photo(d, (32, 178, W - 32, 410))
    d.rectangle([32, 410, W - 32, 412], fill=RULE)
    cap = ("MANAMA, BAHRAIN — Smoke rises over the Gulf after Iran said it "
           "struck two U.S. bases. Bahrain reported a fire at an industrial "
           "site; no injuries.")
    cl = wrap(d, cap, font(SERIF_I, 18), W - 64)
    text_block(d, (32, 418), cl, font(SERIF_I, 18), fill=MUTED, leading=22)
    # Lead headline and deck.
    d.text((W // 2, 466), "IRAN STRIKES U.S. BASES", font=font(SERIF_B, 58),
           fill=INK, anchor="ma")
    d.text((W // 2, 528), "IN BAHRAIN", font=font(SERIF_B, 58), fill=INK,
           anchor="ma")
    deck = ("Tehran says it hit al-Riffa and Awali; Bahrain says air defences "
            "stopped other attacks. Trump seeks a permanent deal as Gulf "
            "shipping faces a wider war.")
    dl = wrap(d, deck, font(SANS, 23), W - 96)
    text_block(d, (48, 596), dl, font(SANS, 23), leading=29, align="center")
    rule(d, 664, width=2)
    # Secondary stories, two by two.
    story_cell(d, 32, 678, 480, thumb_mexico, "MEXICO",
               "FBI most-wanted cartel boss captured",
               "Seized in Sinaloa; 11 killed as violence follows the raid.")
    story_cell(d, 512, 678, 480, thumb_ukraine, "UKRAINE",
               "Missile hits Zelenskyy’s hometown",
               "Boy, 7, and a paramedic killed; rescuers struck as they "
               "arrived.")
    story_cell(d, 32, 808, 480, thumb_climate, "CLIMATE",
               "COP31 talks deadlock on fossil fuels",
               "Antalya summit runs past its deadline with no deal.")
    story_cell(d, 512, 808, 480, thumb_markets, "MARKETS",
               "AI sell-off pushes stocks into correction",
               "S&P 500 falls 3.7%; Nasdaq erases its 2026 gains.")
    rule(d, 940, width=1)
    # Also today strip.
    d.text((32, 948), "ALSO TODAY", font=font(SANS_B, 16), fill=ACCENT)
    strip = ("Drones hit a Russian cargo ship in the Baltic  ·  Estonia to "
             "close its border with Russia  ·  Israeli strike kills three in "
             "a Gaza aid vehicle  ·  Mathematician claims an AI-assisted "
             "proof of the Riemann hypothesis")
    sl = wrap(d, strip, font(SANS, 15), W - 64)
    text_block(d, (32, 970), sl, font(SANS, 15), fill=MUTED, leading=19)
    img.save(os.path.join(HERE, "preview.png"))
    print("wrote preview.png", img.size)


if __name__ == "__main__":
    build()
