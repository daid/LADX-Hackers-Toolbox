import PIL.Image
import backgroundEditor


def exportMap(rom, filename):
    tiles = []
    for idx in range(0x80):
        tile = bytearray(0x100)
        data = rom.banks[0x2C][0x3800+idx*0x10:0x3810+idx*0x10]
        for y in range(8):
            a = data[y * 2 + 0]
            b = data[y * 2 + 1]
            for x in range(8):
                c = 0
                if a & (0x80 >> x):
                    c |= 1
                if b & (0x80 >> x):
                    c |= 2
                tile[x + y * 8] = c
        tiles.append(tile)

    palette_addr = 0x386E
    palette = []
    for n in range(8 * 4):
        p0 = rom.banks[0x21][palette_addr]
        p1 = rom.banks[0x21][palette_addr + 1]
        pal = p0 | p1 << 8
        palette_addr += 2
        r = (pal & 0x1F) << 3
        g = ((pal >> 5) & 0x1F) << 3
        b = ((pal >> 10) & 0x1F) << 3
        palette += [r, g, b]

    result = PIL.Image.new("P", (16*8, 16*8))
    result.putpalette(palette)
    tile_data = rom.banks[0x20][0x168B:0x178B]
    attr_data = rom.banks[0x20][0x178B:0x188B]
    for y in range(16):
        for x in range(16):
            idx = tile_data[x + y * 16]
            idx = idx + 0x10 if idx < 0xF0 else idx - 0xF0
            attr = attr_data[x + y * 16]
            result.paste(PIL.Image.frombytes("P", (8, 8), bytes([i + attr * 4 for i in tiles[idx]])), (x*8, y*8))
    result.save(filename)


def importMap(rom, filename):
    try:
        image = PIL.Image.open(filename)
    except:
        return
    tiles = []
    attrs = []
    for y in range(16):
        for x in range(16):
            tile = bytearray(16)
            pals = {}
            for yn in range(8):
                a = 0
                b = 0
                for xn in range(8):
                    c = image.getpixel((x*8+xn, y*8+yn))
                    if c & 1:
                        a |= 0x80 >> xn
                    if c & 2:
                        b |= 0x80 >> xn
                    pals[c >> 2] = pals.get(c >> 2, 0) + 1
                tile[yn * 2 + 0] = a
                tile[yn * 2 + 1] = b
            tiles.append(bytes(tile))
            attrs.append(sorted(pals.items(), key=lambda n: n[1])[-1][0])

    tile_index = 0x0A
    known_tiles = {}
    for index, (tile, attr) in enumerate(zip(tiles, attrs)):
        if tile not in known_tiles:
            rom.banks[0x2C][0x3800 + tile_index * 0x10:0x3810 + tile_index * 0x10] = tile
            known_tiles[tile] = tile_index
            tile_index += 1
            while tile_index in {0x0C, 0x3C, 0x4B, 0x4C, 0x5B, 0x5C, 0x5D, 0x5E, 0x5F, 0x60, 0x61, 0x62, 0x63}:
                tile_index += 1
        rom.banks[0x20][0x168B + index] = known_tiles[tile] - 0x10 if known_tiles[tile] >= 0x10 else known_tiles[tile] + 0xF0
        rom.banks[0x20][0x178B + index] = attr
    assert tile_index <= 0x80
