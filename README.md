# 第一カード商会 — アドウォールLP

アドウォール（ポイント還元広告）経由の流入ユーザー向けランディングページ。
静的な HTML / CSS / JS 構成で、サーバー不要。`index.html`（未ログインユーザー用）/
`login.html`（ログイン済みユーザー用）をブラウザで開けば確認できます。

`login.html` は `index.html` をベースに、ヒーロー見出し・バッジ・フッターCTA文言のみ
会員向けトーン（「いつもご利用ありがとうございます」「今日も無料でポイントGET!」）に
差し替えたもので、それ以外の構成・CSS・CTA遷移先は共通です。

## ファイル構成

```
landingpage/
├─ index.html        … ページ本体（未ログインユーザー用）
├─ login.html        … ページ本体（ログイン済みユーザー用／会員向けトーン）
├─ css/style.css     … スタイル（デザイントークンは :root で定義／両ページ共通）
├─ js/main.js        … リンク差し替え・追従CTA・FAQ開閉・フェードイン（両ページ共通）
├─ assets/
│  ├─ logo.jpg              … 支給ロゴ原本（400x400）
│  ├─ logo-mark.png        … ロゴのシンボルマークのみ（ヘッダーで使用）
│  ├─ logo-full.png        … ロゴのフル版（マーク＋社名。予備）
│  ├─ character-hero.png    … 手を振るキャラ（ヒーロー右／フッターCTA）
│  └─ character-point.png   … ピースするキャラ（「アドウォールとは？」左）
├─ export/
│  ├─ html.txt          … index.html を画像埋め込み＋JSインライン化した完全なHTML文書（エディター貼り付け用）
│  ├─ login-html.txt    … login.html を同様に変換した完全なHTML文書（エディター貼り付け用）
│  ├─ css.txt           … CSS（エディターのCSS欄に貼り付け用／両ページ共通）
│  └─ build-export.py   … 上記3ファイルを再生成するスクリプト（要 Pillow）
└─ README.md
```

## ブラウザエディターへの貼り付け（export/）

- `export/html.txt`（未ログイン用）/ `export/login-html.txt`（ログイン済み用） …
  エディターのHTML欄に全文貼り付け。`<!DOCTYPE html>` から始まる完全な文書で、
  ロゴ・キャラ画像は base64 埋め込み、`main.js` は末尾の `<script>` にインライン済み。
- `export/css.txt` … エディターのCSS欄に全文貼り付け（両ページ共通）。
- 遷移先URLは貼り付け後、HTML内の `<script>` の `CONFIG.ctaUrl` を書き換える。
- 元ファイル（index.html / login.html / css / js / assets）を編集したら
  `python export/build-export.py` で両ページ分を再生成。

## 差し替え箇所

### 1. 遷移先URL（必須）
`js/main.js` 冒頭の `CONFIG` を編集（`export/html.txt` を使う場合はHTML内 `<script>` の同じ箇所）：

```js
var CONFIG = {
  ctaUrl: 'https://example.com/adwall'   // 「ポイントを獲得する」ボタン
};
```

アドウォールのトラッキングパラメータが必要な場合も `ctaUrl` に付与してください。

### 2. キャラクター画像（配置済み）

- `character-hero.png` … 手を振るキャラ。ヒーロー右側とフッターCTAで使用（背景透過PNG）
- `character-point.png` … ピースするキャラ。「アドウォールとは？」左側で使用（背景透過PNG）

別の画像に差し替える場合は同名で上書き。無い場合は自動で非表示になります
（ヒーロー／アドウォール説明はプレースホルダー枠、フッターは消える）。
ファイル名や枚数を変える場合は `index.html` の該当 `<img>` を編集。

### 3. ロゴ
支給ロゴ（`assets/logo.jpg`）からシンボルマークを切り出した `assets/logo-mark.png`
をヘッダーで使用。社名テキストは HTML 側で表示。
差し替える場合は `assets/logo-mark.png` を置き換えるか、
`index.html` の `<img class="brand-logo" src="...">` を編集。

### 4. カラー
`css/style.css` の `:root` で一括管理：

| 変数 | 用途 | 現在値 |
|------|------|--------|
| `--pink` / `--pink-deep` | メインのピンク | `#f0509e` / `#e5388c` |
| `--teal` / `--teal-dark` | 見出し帯のティール | `#33b4a0` / `#2a9d8a` |
| `--gold` | コイン・ポイント数 | `#f4b21e` |

### 5. 文言・ポイント数
「獲得ポイント例」「よくある質問」「ご利用前の注意」などは
`index.html` に直接記載。案件条件に合わせて編集してください。

## 注意
- ページには `noindex,nofollow` を設定済み（広告用LGのため検索除外）。
- フォントは Google Fonts（M PLUS Rounded 1c）をCDN読み込み。
  オフライン運用する場合はローカルへ同梱してください。
