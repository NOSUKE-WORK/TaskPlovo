"""
generate_icon.py - TaskPlovo オリジナルアイコン（スケジュール表デザイン）
"""
import os
from PIL import Image, ImageDraw


def draw_icon(size: int) -> Image.Image:
    s   = size
    img = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d   = ImageDraw.Draw(img)

    m  = max(2, s // 14)
    r  = max(3, s // 9)

    # 背景（白・角丸）
    d.rounded_rectangle([m, m, s-m, s-m], radius=r, fill="#FFFFFF")

    # ヘッダーバー（濃い水色）
    hh = max(5, int(s * 0.22))
    d.rounded_rectangle([m, m, s-m, m+hh], radius=r, fill="#1565C0")
    # 下半分の角丸を消す（矩形で上書き）
    if m + r < m + hh:
        d.rectangle([m, m+r, s-m, m+hh], fill="#1565C0")

    # リングバインダードット（ヘッダー内）
    if s >= 32:
        dot_y = m + hh // 2
        dot_r = max(1, s // 22)
        for dx in [s//4, s//2, 3*s//4]:
            d.ellipse([dx-dot_r-1, dot_y-dot_r-1,
                       dx+dot_r+1, dot_y+dot_r+1], fill="#FFFFFF")
            ir = max(1, dot_r - 1)
            d.ellipse([dx-ir, dot_y-ir, dx+ir, dot_y+ir], fill="#1565C0")

    # グリッドエリアの境界
    pad  = max(2, s // 18)
    gt   = m + hh + pad
    gb   = s - m - pad
    gl   = m + pad
    gr   = s - m - pad

    # グリッドが描けるサイズか確認
    if gr - gl < 6 or gb - gt < 6:
        return img

    cols, rows = 3, 3
    cw = (gr - gl) / cols
    rh = (gb - gt) / rows

    cell_colors = [
        ["#E3F2FD", "#1565C0", "#E3F2FD"],
        ["#E3F2FD", "#E3F2FD", "#42A5F5"],
        ["#42A5F5", "#E3F2FD", "#E3F2FD"],
    ]
    check_cells = {(1, 1), (2, 0)}

    for row in range(rows):
        for col in range(cols):
            gap = max(1, s // 64)
            x0 = int(gl + col * cw) + gap
            y0 = int(gt + row * rh) + gap
            x1 = int(gl + (col+1) * cw) - gap
            y1 = int(gt + (row+1) * rh) - gap
            if x1 <= x0 or y1 <= y0:
                continue
            cr = max(1, s // 40)
            d.rounded_rectangle([x0, y0, x1, y1],
                                  radius=cr, fill=cell_colors[row][col])

            # チェックマーク
            if (row, col) in check_cells and (x1-x0) >= 4:
                cx = (x0 + x1) / 2
                cy = (y0 + y1) / 2
                cs = min(x1-x0, y1-y0) * 0.25
                lw = max(1, s // 48)
                pts = [
                    (cx - cs,       cy),
                    (cx - cs*0.15,  cy + cs*0.75),
                    (cx + cs,       cy - cs*0.6),
                ]
                d.line(pts, fill="#FFFFFF", width=lw)

    # 全体外枠
    d.rounded_rectangle([m, m, s-m, s-m], radius=r,
                         outline="#1565C0", width=max(1, s//36), fill=None)
    return img


def make_icon():
    os.makedirs("assets", exist_ok=True)
    sizes  = [256, 128, 64, 48, 32, 16]
    images = [draw_icon(sz) for sz in sizes]
    images[0].save("assets/icon.ico", format="ICO",
                   sizes=[(sz, sz) for sz in sizes],
                   append_images=images[1:])
    images[0].save("assets/icon.png", format="PNG")
    print("[OK] assets/icon.ico and assets/icon.png generated.")


if __name__ == "__main__":
    try:
        make_icon()
    except Exception as e:
        print(f"[ERROR] {e}")
        raise
