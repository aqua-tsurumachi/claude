#!/usr/bin/env python3
"""
export/html.txt・export/login-html.txt と export/css.txt を生成するスクリプト。

- index.html(未ログイン用)・login.html(ログイン済み用) それぞれを元に、
  画像(ロゴ・キャラクター)を base64 データURIとして埋め込み、
  js/main.js を末尾の <script> にインライン展開する。
- css/style.css はそのまま css.txt にコピー(両ページ共通)。

使い方:  landingpage/ ディレクトリで  python export/build-export.py

必要: Pillow  (pip install Pillow)
"""
import base64, io, pathlib
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"

PAGES = [
    ("index.html", "html.txt"),
    ("login.html", "login-html.txt"),
]


def datauri(path, width, colors=0):
    im = Image.open(path).convert("RGBA")
    if im.width > width:
        h = round(im.height * width / im.width)
        im = im.resize((width, h), Image.LANCZOS)
    if colors:
        alpha = im.getchannel("A")
        im = im.convert("RGB").quantize(colors=colors, method=Image.Quantize.MEDIANCUT).convert("RGBA")
        im.putalpha(alpha)
    buf = io.BytesIO()
    im.save(buf, "PNG", optimize=True)
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()


def build_html(src_name, out_name, logo, hero, foot, point, js):
    html = (ROOT / src_name).read_text(encoding="utf-8")

    html = html.replace(
        '<link rel="stylesheet" href="css/style.css">',
        '<!-- ▼ CSSは別ファイル「css.txt」の中身をエディターのCSS欄に貼り付けてください ▼ -->',
    )
    html = html.replace(
        '<img class="footer-cta-illust" src="assets/character-hero.png" alt="" aria-hidden="true"',
        f'<img class="footer-cta-illust" src="{foot}" alt="" aria-hidden="true"',
    )
    html = html.replace('src="assets/character-hero.png"', f'src="{hero}"')
    html = html.replace('src="assets/character-point.png"', f'src="{point}"')
    html = html.replace('src="assets/logo-mark.png"', f'src="{logo}"')
    html = html.replace('<script src="js/main.js"></script>', "<script>\n" + js.strip() + "\n</script>")

    (ROOT / "export" / out_name).write_text(html, encoding="utf-8")


def main():
    logo  = datauri(ASSETS / "logo-mark.png", 130)
    hero  = datauri(ASSETS / "character-hero.png", 440, colors=128)
    foot  = datauri(ASSETS / "character-hero.png", 260, colors=128)   # フッターは小さいサイズで十分
    point = datauri(ASSETS / "character-point.png", 380, colors=128)
    js    = (ROOT / "js" / "main.js").read_text(encoding="utf-8")

    for src_name, out_name in PAGES:
        build_html(src_name, out_name, logo, hero, foot, point, js)

    css_header = (
        "/* ============================================================\n"
        "   第一カード商会 アドウォールLP ― CSS\n"
        "   ブラウザエディターの「CSS」欄にこのファイルの中身をそのまま貼り付けてください。\n"
        "   (index.html / login.html 共通)\n"
        "   ============================================================ */\n\n"
    )
    css = (ROOT / "css" / "style.css").read_text(encoding="utf-8")
    (ROOT / "export" / "css.txt").write_text(css_header + css, encoding="utf-8")

    files = [out_name for _, out_name in PAGES] + ["css.txt"]
    for f in files:
        p = ROOT / "export" / f
        print(f"{f:14} {p.stat().st_size / 1024:8.1f} KB")


if __name__ == "__main__":
    main()
