from PIL import Image, ImageDraw
import random

S = 96  # tile size in px

def shade(base, v):
    return (max(0, min(255, base[0]+v)), max(0, min(255, base[1]+v)), max(0, min(255, base[2]+v)), 255)

def tile(base, seed, speckles=260, pebbles=40, cracks=0):
    random.seed(seed)
    im = Image.new('RGBA', (S, S), base + (255,))
    d = ImageDraw.Draw(im)
    # granular noise
    for _ in range(speckles):
        x, y = random.randrange(S), random.randrange(S)
        d.point((x, y), fill=shade(base, random.randint(-28, 28)))
    # pebbles / dots
    for _ in range(pebbles):
        x, y = random.randrange(S-6), random.randrange(S-6)
        d.ellipse((x, y, x+random.randint(2,5), y+random.randint(2,5)), fill=shade(base, random.randint(-45, 45)))
    # cracks (rock)
    for _ in range(cracks):
        x, y = random.randrange(S), random.randrange(S)
        pts = [(x, y)]
        for _ in range(random.randint(3, 6)):
            x += random.randint(-14, 14); y += random.randint(-14, 14)
            x = max(0, min(S-1, x)); y = max(0, min(S-1, y))
            pts.append((x, y))
        d.line(pts, fill=shade(base, -60), width=1)
    # inner edge shading for depth (darker border inside the tile)
    edge = 6
    for i in range(edge):
        a = 255 - int(40 * (i / edge))
        d.rectangle((i, i, S-1-i, S-1-i), outline=(0, 0, 0, 60 - int(50*(i/edge))))
    return im

tile((74, 140, 74),   seed=1, speckles=200, pebbles=25).save('/workspace/tiles/tile_open.png')     # green
tile((214, 183, 92), seed=2, speckles=320, pebbles=55).save('/workspace/tiles/tile_sand.png')     # sandy, lots of dots
tile((112, 112, 116), seed=3, speckles=280, pebbles=35, cracks=7).save('/workspace/tiles/tile_rock.png')  # gray + cracks
tile((86, 198, 214), seed=4, speckles=160, pebbles=15).save('/workspace/tiles/tile_charger.png')  # cyan
print('tiles written')
