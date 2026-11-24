# Land texture tiles

96x96 RGBA PNG tiles for the Graphics1300 rover map, generated with PIL (`make_tiles.py`):

- `tile_open.png` — green open ground (also used for hidden sample sites)
- `tile_sand.png` — sandy with heavy speckle dots (terrain `~`)
- `tile_rock.png` — gray with cracks (terrain `#`)
- `tile_charger.png` — cyan with white helipad H (terrain `C`)

Each tile has granular noise, pebbles, and inner edge shading. Regenerate with:
`python3 make_tiles.py`

Use in WorldView: load each as `Image` once in the constructor, then per cell
`Sprite s(tile, cellToPixel(cell), cellSize, cellSize); s.draw(window);`
and draw the cell outline on top (transparent-fill Rectangle + outline color).
