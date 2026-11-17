# -*- coding: utf-8 -*-
"""把 Gazebo 正俯视截图裁剪并拼成与规则图 2 的对比图。

前置（在 competition_ws/src/maps/zhirong_maps 下）::

    source ../../../tools/gazebo_env.sh
    export GAZEBO_MASTER_URI=http://127.0.0.1:11391
    export GAZEBO_MODEL_PATH="$PWD/models:$GAZEBO_MODEL_PATH"
    Xvfb :99 -screen 0 1280x1280x24 -ac &
    unset DISPLAY; gzserver worlds/zhirong_arena.world &
    DISPLAY=:99 LIBGL_ALWAYS_SOFTWARE=1 gzclient &
    DISPLAY=:99 xwd -root -out preview/scene/render_raw.xwd
    python3 tools/xwd2png.py preview/scene/render_raw.xwd preview/scene/render_raw.png

然后运行本脚本：``python3 preview/scene/render_topdown.py``
输出：render_topdown.png（裁剪后渲染）、compare_topdown.png（左图2 / 右仿真）。
"""

import os
import sys

from PIL import Image, ImageDraw, ImageFont

WS = "/home/nepenthe/zmf/linux_code/dsh工作区"
HERE = os.path.join(WS, "preview/scene")
FIG2 = os.path.join(WS, "preview/docx_media/image2.png")
FONT = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"

# 1280×1280 截图中 3D 视口范围（去掉左侧属性面板 / 顶部工具栏 / 底部状态栏）
VIEWPORT = (285, 75, 1280, 1170)


def main():
    raw_path = os.path.join(HERE, "render_raw.png")
    if not os.path.exists(raw_path):
        sys.exit("缺少 %s：请先按脚本头部说明完成 Xvfb + gzclient 截图" % raw_path)
    raw = Image.open(raw_path).convert("RGB")
    crop = raw.crop(VIEWPORT)
    crop.save(os.path.join(HERE, "render_topdown.png"))

    fig2 = Image.open(FIG2).convert("RGB").crop((15, 15, 960, 1025))
    H = 1300

    def fit(im, h):
        return im.resize((int(round(im.width * h / im.height)), h), Image.LANCZOS)

    left, right = fit(fig2, H), fit(crop, H)
    f_title = ImageFont.truetype(FONT, 44)
    f_note = ImageFont.truetype(FONT, 26)
    f_small = ImageFont.truetype(FONT, 22)

    pad, head, foot = 36, 66, 96
    width = pad * 3 + left.width + right.width
    canvas = Image.new("RGB", (width, head + H + foot + pad), "white")
    canvas.paste(left, (pad, head))
    canvas.paste(right, (pad * 2 + left.width, head))
    dr = ImageDraw.Draw(canvas)
    dr.text((pad, 14), "规则图 2（Word 原图）", fill="black", font=f_title)
    dr.text((pad * 2 + left.width, 14),
            "Gazebo 俯视渲染（v3 微调；↑北 →东，与图 2 同方向）",
            fill="black", font=f_title)
    dr.text((pad, head + H + 10),
            "左：规则图 2；右：zhirong_arena.world 在 Gazebo Classic 11 中的正俯视渲染（软件渲染 Xvfb + llvmpipe）。"
            "对比要点：16 单元格、黄/桔/红三区、斜坡/橙区已按图 2 椭圆缩小、", fill="#333333", font=f_note)
    dr.text((pad, head + H + 46),
            "L/Z/T/工型墙位置与开向、斜坡1（中右）/斜坡2（中下）、红边界不规则折线及东偏北入口 / 西中部出口缺口。"
            "透视俯视会让墙顶略向外倾，属相机透视，非布局偏差。", fill="#333333", font=f_note)
    dr.text((pad, head + H + 84),
            "生成：Xvfb :99 + DISPLAY=:99 LIBGL_ALWAYS_SOFTWARE=1 gzclient → xwd 截图 → render_topdown.py",
            fill="#777777", font=f_small)
    out = os.path.join(HERE, "compare_topdown.png")
    canvas.save(out)
    print("render_topdown.png,", out, canvas.size)


if __name__ == "__main__":
    main()
