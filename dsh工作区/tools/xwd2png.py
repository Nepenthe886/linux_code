#!/usr/bin/env python3
"""把 X11 xwd 截图转成 PNG（无需 ImageMagick/netpbm）。

用法: python3 tools/xwd2png.py shot.xwd shot.png
支持 24/32 位 TrueColor（Xvfb/Xorg 默认）。
"""
import struct
import sys

from PIL import Image


def convert(src: str, dst: str) -> None:
    with open(src, "rb") as f:
        data = f.read()
    hdr = struct.unpack(">25I", data[:100])
    (header_size, _ver, pixmap_format, pixmap_depth, width, height,
     _xoff, _byte_order, _bmp_unit, _bmp_bit_order, _bmp_pad, bits_per_pixel,
     bytes_per_line, visual_class, red_mask, green_mask, blue_mask,
     _bits_per_rgb, _cmap_entries, ncolors, _win_w, _win_h, _win_x, _win_y,
     _win_bw) = hdr
    off = header_size + ncolors * 12  # 跳过窗口名与色表
    px = data[off:off + bytes_per_line * height]
    w, h = width, height
    img = Image.new("RGB", (w, h))
    out = img.load()
    bpp_bytes = (bits_per_pixel + 7) // 8
    # 计算各通道移位与位宽
    def channel(mask):
        if mask == 0:
            return 0, 0
        shift = 0
        while not (mask >> shift) & 1:
            shift += 1
        bits = 0
        m = mask >> shift
        while m & 1:
            bits += 1
            m >>= 1
        return shift, bits

    rs, rb = channel(red_mask)
    gs, gb = channel(green_mask)
    bs, bb = channel(blue_mask)
    for y in range(h):
        row = px[y * bytes_per_line:(y + 1) * bytes_per_line]
        for x in range(w):
            i = x * bpp_bytes
            if pixmap_depth == 24 and bpp_bytes == 4:
                v = row[i] | row[i + 1] << 8 | row[i + 2] << 16
            else:
                v = int.from_bytes(row[i:i + bpp_bytes], "little")
            r = ((v & red_mask) >> rs) << (8 - rb) if rb else 0
            g = ((v & green_mask) >> gs) << (8 - gb) if gb else 0
            b = ((v & blue_mask) >> bs) << (8 - bb) if bb else 0
            out[x, y] = (r & 255, g & 255, b & 255)
    img.save(dst)
    print(f"ok {src} {w}x{h} -> {dst}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)
    convert(sys.argv[1], sys.argv[2])
