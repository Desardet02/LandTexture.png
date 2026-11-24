# Generates the 96x96 RGBA terrain tiles for the Graphics1300 rover map.
# Run: python3 make_tiles.py   (needs: pip install pillow)
from PIL import Image, ImageDraw
import random

S = 96  # tile size in px
OUT = '.'  # output directory

def shade(base, v):
    return (max(0, min(255, base[0]+v)), max(0, min(255, base[1]+v)), max(0, min(255, base[2]+v)), 255)

def tile(base, seed, speckles=260, pebbles=40, cracks=0):
    random.seed(seed)
    im = Image.new('RGBA', (S, S), base + (255,))
    d = ImageDraw.Draw(im)
    for _ in range(speckles):                       # granular noise
        x, y = random.randrange(S), random.randrange(S)
        d.point((x, y), fill=shade(base, random.randint(-28, 28)))
    for _ in range(pebbles):                        # pebbles / dots
        x, y = random.randrange(S-6), random.randrange(S-6)
        d.ellipse((x, y, x+random.randint(2, 5), y+random.randint(2, 5)), fill=shade(base, random.randint(-45, 45)))
    for _ in range(cracks):                         # cracks (rock)
        x, y = random.randrange(S), random.randrange(S)
        pts = [(x, y)]
        for _ in range(random.randint(3, 6)):
            x = max(0, min(S-1, x + random.randint(-14, 14)))
            y = max(0, min(S-1, y + random.randint(-14, 14)))
            pts.append((x, y))
        d.line(pts, fill=shade(base, -60), width=1)
    for i in range(6):                              # inner edge shading
        d.rectangle((i, i, S-1-i, S-1-i), outline=(0, 0, 0, 60 - int(50*(i/6))))
    return im

def draw_H(im):
    """White helipad 'H' with dark outline, centered."""
    d = ImageDraw.Draw(im)
    cx = cy = S // 2
    w, t = 46, 10
    x0, x1 = cx - w//2, cx + w//2
    y0, y1 = cy - w//2, cy + w//2
    dark = (15, 60, 70, 255)
    white = (245, 250, 250, 255)
    for col, tt in ((dark, t+4), (white, t)):       # outline pass, then fill pass
        d.rectangle((x0-tt//2, y0-tt//2, x0+tt//2, y1+tt//2), fill=col)  # left bar
        d.rectangle((x1-tt//2, y0-tt//2, x1+tt//2, y1+tt//2), fill=col)  # right bar
        d.rectangle((x0-tt//2, cy-tt//2, x1+tt//2, cy+tt//2), fill=col)  # crossbar

tile((74, 140, 74),    seed=1, speckles=200, pebbles=25).save(OUT + '/tile_open.png')     # green
tile((214, 183, 92),   seed=2, speckles=320, pebbles=55).save(OUT + '/tile_sand.png')     # sandy
tile((112, 112, 116),  seed=3, speckles=280, pebbles=35, cracks=7).save(OUT + '/tile_rock.png')   # gray + cracks
ch = tile((86, 198, 214), seed=4, speckles=160, pebbles=15)                                # cyan
draw_H(ch)
ch.save(OUT + '/tile_charger.png')                                                        # helipad H
print('tiles written to', OUT)
