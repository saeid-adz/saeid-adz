"""Render the profile artwork: python3 scripts/generate_profile_assets.py.

Requires Pillow and Arial (macOS) or DejaVu Sans (Linux). Generated artwork is
committed locally; visitors need no Python or third-party animation service.
"""

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "profile"
OUT.mkdir(parents=True, exist_ok=True)
BG, WHITE, MUTED, CYAN, PURPLE = "#080e1c", "#edf5ff", "#98abc5", "#67e8f9", "#b393ff"


def font(size, bold=False, mono=False):
    names = (
        ["/System/Library/Fonts/Supplemental/Courier New.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"]
        if mono else
        [f"/System/Library/Fonts/Supplemental/Arial{' Bold' if bold else ''}.ttf",
         f"/usr/share/fonts/truetype/dejavu/DejaVuSans{'-Bold' if bold else ''}.ttf"]
    )
    for name in names:
        if Path(name).exists():
            return ImageFont.truetype(name, size)
    raise RuntimeError("Install Arial or DejaVu Sans to regenerate artwork.")


def label(draw, xy, text, size=16, fill=MUTED, bold=False, mono=False):
    draw.text(xy, text, font=font(size, bold, mono), fill=fill)


def rounded(draw, box, fill, outline=None, radius=15, width=1):
    draw.rounded_rectangle(box, radius, fill, outline, width)


def hero_base():
    im = Image.new("RGB", (1280, 600), BG)
    d = ImageDraw.Draw(im)
    for y in range(600):
        for x in range(740, 1280, 3):
            strength = max(0, 1 - math.hypot((x - 1040) / 480, (y - 275) / 390))
            if strength:
                d.line((x, y, x + 2, y), fill=(8 + int(12 * strength), 14 + int(12 * strength), 28 + int(27 * strength)))
    for x in range(32, 1280, 32):
        for y in range(30, 600, 32):
            d.point((x, y), fill="#243049")
    d.line((48, 78, 1232, 78), fill="#253049")
    label(d, (48, 32), "SD / CLOUD & AI", 17, WHITE, True, True)
    d.ellipse((998, 39, 1005, 46), fill="#72efb0")
    label(d, (1019, 31), "HELLO FROM SWEDEN", 14, MUTED, mono=True)
    label(d, (48, 113), "ENGINEER. EDUCATOR. COMMUNITY BUILDER.", 15, CYAN, mono=True)
    label(d, (40, 149), "SAEID", 122, WHITE, True)
    label(d, (40, 267), "DAHL.", 122, WHITE, True)
    label(d, (48, 416), "Cloud chaos. Automated magic.", 29, WHITE, True)
    label(d, (48, 459), "Azure & AI geek  /  Speaker  /  Mentor", 19, MUTED)
    d.line((48, 517, 1232, 517), fill="#253049")
    label(d, (48, 546), "MICROSOFT MVP", 15, CYAN, True, True)
    label(d, (281, 546), "+", 15, MUTED)
    label(d, (316, 546), "MCT LEADER", 15, PURPLE, True, True)
    label(d, (901, 546), "LESS CLICKING. MORE SHIPPING.", 14, MUTED, mono=True)
    return im


def cube(d, x, y, size=27, color=CYAN):
    d.polygon([(x, y-size), (x+size, y-size/2), (x, y), (x-size, y-size/2)], fill="#254364", outline=color)
    d.polygon([(x-size, y-size/2), (x, y), (x, y+size), (x-size, y+size/2)], fill="#10213b", outline=color)
    d.polygon([(x, y), (x+size, y-size/2), (x+size, y+size/2), (x, y+size)], fill="#15394f", outline=color)


def save_loop(frames, name, duration, still_frame=0):
    # A shared palette prevents per-frame color flicker.
    palette = frames[-1].quantize(colors=128)
    indexed = [frame.quantize(palette=palette, dither=Image.Dither.NONE) for frame in frames]
    indexed[0].save(OUT / f"{name}.gif", save_all=True, append_images=indexed[1:], duration=duration, loop=0, optimize=True, disposal=1)
    frames[still_frame].save(OUT / f"{name}-still.png", optimize=True)


def render_hero():
    base = hero_base()
    frames = []
    for frame in range(64):
        t = frame / 64 * math.tau
        im = base.copy()
        d = ImageDraw.Draw(im)
        d.ellipse((799, 137, 1215, 455), outline="#29405d", width=1)
        d.ellipse((825, 160, 1189, 432), outline="#1b304c", width=1)
        for offset, color in [(0, CYAN), (math.pi, PURPLE)]:
            x, y = 1007 + 208 * math.cos(t + offset), 296 + 159 * math.sin(t + offset)
            d.ellipse((x-6, y-6, x+6, y+6), fill=color)
        for index, (x, y) in enumerate([(864, 233), (1160, 236), (1007, 423)]):
            d.line((1007, 290, x, y), fill="#385570", width=2)
            phase = (frame / 64 * 2 + index / 3) % 1
            px, py = 1007 + (x-1007)*phase, 290 + (y-290)*phase
            d.ellipse((px-4, py-4, px+4, py+4), fill=CYAN)
            cube(d, x, y, 24, PURPLE if index == 1 else CYAN)
        lift = int(5 * math.sin(t))
        cloud = Image.new("RGBA", im.size)
        c = ImageDraw.Draw(cloud)
        c.ellipse((932, 232+lift, 1010, 308+lift), fill="#122d49", outline=CYAN, width=2)
        c.ellipse((970, 200+lift, 1058, 294+lift), fill="#122d49", outline=CYAN, width=2)
        c.ellipse((1022, 239+lift, 1080, 309+lift), fill="#122d49", outline=CYAN, width=2)
        c.rounded_rectangle((930, 263+lift, 1082, 320+lift), 25, fill="#122d49", outline=CYAN, width=2)
        c.rectangle((949, 264+lift, 1061, 299+lift), fill="#122d49")
        c.line((1005, 252+lift, 988, 278+lift, 1010, 278+lift, 996, 301+lift), fill=WHITE, width=4)
        im = Image.alpha_composite(im.convert("RGBA"), cloud).convert("RGB")
        d = ImageDraw.Draw(im)
        rounded(d, (780, 179, 896, 207), BG, "#385570", 8)
        label(d, (794, 185), "AUTOMATE", 13, CYAN, mono=True)
        rounded(d, (1122, 180, 1200, 208), BG, "#385570", 8)
        label(d, (1144, 186), "AI", 13, PURPLE, mono=True)
        label(d, (921, 475), "BUILD / SHARE / REPEAT", 12, MUTED, mono=True)
        frames.append(im)
    save_loop(frames, "mission-control", 100)


def render_terminal():
    base = Image.new("RGB", (1280, 420), BG)
    d = ImageDraw.Draw(base)
    rounded(d, (1, 1, 1278, 418), BG, "#29374e", 18)
    for x, color in [(29, "#ff7b91"), (53, "#ffd580"), (77, "#72efb0")]:
        d.ellipse((x, 22, x+11, 33), fill=color)
    label(d, (113, 19), "saeid@cloud-lab ~ / the automation mindset", 16, MUTED, mono=True)
    d.line((1, 55, 1278, 55), fill="#29374e")
    label(d, (37, 82), "PS >", 23, PURPLE, mono=True)
    command = "./build-something-awesome.ps1"
    lines = [
        ("01", "Design the foundation", "Azure / landing zones / governance"),
        ("02", "Automate the boring parts", "Bicep / Terraform / PowerShell"),
        ("03", "Make AI useful", "Agents / copilots / real-world problems"),
        ("04", "Share what you learn", "Talks / workshops / community"),
    ]
    frames = []
    for frame in range(80):
        im = base.copy()
        d = ImageDraw.Draw(im)
        count = min(len(command), frame * 2)
        label(d, (112, 82), command[:count], 23, WHITE, mono=True)
        if frame < 18 and frame % 8 < 5:
            x = 112 + d.textlength(command[:count], font=font(23, mono=True))
            d.rectangle((x+3, 85, x+13, 108), fill=CYAN)
        for i, (number, text, tools) in enumerate(lines):
            if frame >= 20 + i * 8:
                y = 143 + i * 47
                label(d, (38, y), number, 18, CYAN, mono=True)
                label(d, (93, y), text, 20, WHITE)
                label(d, (562, y+2), tools, 17, MUTED, mono=True)
        if frame >= 54:
            label(d, (38, 355), "> Keep building. Keep learning. Bring people along.", 21, "#72efb0", mono=True)
        frames.append(im)
    save_loop(frames, "automation-loop", 110, still_frame=-1)


if __name__ == "__main__":
    render_hero()
    render_terminal()
    for path in sorted(OUT.glob("*")):
        print(f"{path.relative_to(ROOT)}: {path.stat().st_size / 1024:.0f} KiB")
