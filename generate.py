"""Render the 20 November 2026 world-news image (1024x1024 PNG).

Front-page layout, drawn with Pillow only: a masthead with the date, one
lead story, two second stories, three third stories and an "also today"
strip. Every fact on the image was checked against reporting of that day:
ICJ Myanmar/Rohingya ruling, the Shenzhen three-way summit, the 20 Nov
market sell-off, the Kyiv strikes, the Riyadh missile, and COP31.
Run:  python3 generate.py   (writes entry.png next to this file)
"""
import textwrap

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 232)
INK = (17, 24, 39)
RED = (185, 28, 28)
NAVY = (30, 58, 95)
BLUE = (29, 78, 216)
GREY = (100, 116, 139)
LIGHT = (255, 255, 255)
GOLD = (180, 130, 29)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"


def font(name, size):
    return ImageFont.truetype(FONT_DIR + name, size)


F_TITLE = font("DejaVuSans-Bold.ttf", 46)
F_DATE = font("DejaVuSans-Bold.ttf", 72)
F_HEAD = font("DejaVuSans-Bold.ttf", 34)
F_HEAD2 = font("DejaVuSans-Bold.ttf", 28)
F_HEAD3 = font("DejaVuSans-Bold.ttf", 24)
F_BODY = font("DejaVuSans.ttf", 22)
F_BODY2 = font("DejaVuSans.ttf", 20)
F_TAG = font("DejaVuSans-Bold.ttf", 20)
F_SMALL = font("DejaVuSans.ttf", 19)


def wrap(draw, text, fnt, width):
    lines, out = [], ""
    for word in text.split():
        trial = (out + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            out = trial
        else:
            lines.append(out)
            out = word
    if out:
        lines.append(out)
    return lines


def para(draw, x, y, text, fnt, width, fill=INK, leading=30):
    for chunk in text.split("\n"):
        for line in wrap(draw, chunk, fnt, width):
            draw.text((x, y), line, font=fnt, fill=fill)
            y += leading
    return y


def box(draw, x, y, w, h, fill=LIGHT, outline=INK, width=2):
    draw.rectangle([x, y, x + w, y + h], fill=fill, outline=outline, width=width)


def tag(draw, x, y, text, fill=RED):
    w = draw.textlength(text, font=F_TAG) + 18
    draw.rectangle([x, y, x + w, y + 30], fill=fill)
    draw.text((x + 9, y + 4), text, font=F_TAG, fill=LIGHT)
    return w


def scales(draw, cx, cy, s):
    """Simple scales-of-justice pictogram, centred at (cx, cy), size s."""
    draw.line([(cx, cy - s), (cx, cy + s)], fill=NAVY, width=6)
    draw.line([(cx - s, cy - s + 12), (cx + s, cy - s + 12)], fill=NAVY, width=5)
    for sx in (-1, 1):
        draw.line([(cx + sx * s, cy - s + 12), (cx + sx * s, cy + 6)], fill=NAVY, width=4)
        draw.arc([cx + sx * s - 26, cy - 8, cx + sx * s + 26, cy + 34],
                 0, 180, fill=NAVY, width=4)
    draw.ellipse([cx - 8, cy - s - 10, cx + 8, cy - s + 6], fill=GOLD)


def chart_down(draw, x, y, w, h):
    pts = [(x, y + 8), (x + w * 0.25, y + h * 0.3), (x + w * 0.45, y + h * 0.2),
           (x + w * 0.7, y + h * 0.6), (x + w, y + h - 6)]
    draw.line(pts, fill=RED, width=6, joint="curve")
    draw.polygon(pts + [(x + w, y + h), (x, y + h)], fill=(254, 226, 226))
    draw.line(pts, fill=RED, width=6, joint="curve")
    draw.ellipse([x + w - 8, y + h - 14, x + w + 8, y + h + 2], fill=RED)


def skyline(draw, x, y, w, h):
    base = y + h
    for bx, bw, bh in [(0, 34, 70), (40, 26, 96), (72, 30, 58), (108, 24, 84)]:
        draw.rectangle([x + bx, base - bh, x + bx + bw, base], fill=NAVY)
    draw.polygon([(x + 108, base - 84), (x + 132, base - 84), (x + 120, base - 112)],
                 fill=RED)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # Masthead
    d.rectangle([0, 0, W, 118], fill=NAVY)
    d.text((36, 26), "THE WORLD IN ONE DAY", font=F_TITLE, fill=LIGHT)
    d.text((36, 78), "FRIDAY", font=F_TAG, fill=(253, 224, 71))
    d.text((W - 36 - d.textlength("20 NOVEMBER 2026", font=F_DATE) + 260, 78),
           "", font=F_TAG, fill=LIGHT)
    d.rectangle([0, 118, W, 124], fill=RED)
    d.text((36, 138), "20 NOVEMBER 2026", font=F_DATE, fill=INK)
    d.text((36, 218), "The day's world news, in one image.", font=F_BODY, fill=GREY)

    # Lead story: ICJ ruling
    box(d, 36, 262, 952, 210)
    scales(d, 130, 356, 52)
    tag(d, 220, 280, "THE HAGUE  -  JUSTICE")
    d.text((220, 318), "WORLD COURT: MYANMAR", font=F_HEAD, fill=INK)
    d.text((220, 356), "COMMITTED GENOCIDE", font=F_HEAD, fill=INK)
    para(d, 220, 402, "ICJ rules 9-6 against Myanmar over the Rohingya - the first "
       "genocide finding against a state. 1.3m Rohingya remain displaced.",
       F_BODY, 740, leading=27)

    # Second row: Shenzhen + markets
    box(d, 36, 490, 466, 204)
    tag(d, 56, 506, "SHENZHEN  -  SUMMIT")
    d.text((56, 544), "TRUMP, XI AND PUTIN", font=F_HEAD2, fill=INK)
    d.text((56, 576), "MEET, SIGN PEACE PACT", font=F_HEAD2, fill=INK)
    para(d, 56, 618, "First three-way summit: a joint declaration on nuclear risk, "
       "UN reform and energy. No mention of Ukraine or Iran.",
       F_BODY2, 426, leading=26)

    box(d, 522, 490, 466, 204, fill=(254, 242, 242))
    tag(d, 542, 506, "MARKETS  -  SELL-OFF")
    chart_down(d, 880, 528, 88, 70)
    d.text((542, 544), "AI SELL-OFF DEEPENS", font=F_HEAD2, fill=RED)
    para(d, 542, 584, "Nasdaq -5.3%  |  S&P 500 -3.7%\nNvidia -14% on SEC probe\nNikkei -4.8% in Asia",
       F_BODY2, 426, leading=28)

    # Third row: Kyiv, Riyadh, COP31
    cols = [
        ("KYIV  -  WAR", "RUSSIA HITS KYIV",
         "Overnight strikes kill 8 and hit bridges."),
        ("RIYADH  -  CONFLICT", "MISSILE HITS RIYADH TOWER",
         "Houthi missile damages the Saudi wealth-fund tower."),
        ("ANTALYA  -  CLIMATE", "COP31 DROPS FOSSIL-FUEL EXIT",
         "Draft drops the phase-out call and net-zero dates."),
    ]
    x = 36
    for tg, head, body in cols:
        box(d, x, 712, 304, 196)
        tag(d, x + 16, 728, tg, fill=NAVY)
        y = 768
        for line in wrap(d, head, F_HEAD3, 272):
            d.text((x + 16, y), line, font=F_HEAD3, fill=INK)
            y += 30
        para(d, x + 16, y + 6, body, F_BODY2, 272, leading=26)
        x += 324

    # Also today strip
    d.rectangle([36, 926, 988, 968], fill=INK)
    d.text((52, 938), "ALSO TODAY: ", font=F_TAG, fill=(253, 224, 71))
    d.text((206, 938), "Kenya discharges its last Ebola patient  |  EU-UK summit agrees youth mobility",
           font=F_SMALL, fill=LIGHT)

    d.text((36, 984), "Friday 20 November 2026  -  The Hague  -  Shenzhen  -  New York  -  Kyiv  -  Riyadh  -  Antalya",
           font=F_SMALL, fill=GREY)

    img.save("entry.png", optimize=True)


if __name__ == "__main__":
    main()
