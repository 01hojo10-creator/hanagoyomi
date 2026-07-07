# -*- coding: utf-8 -*-
import json, html
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent
credits = json.loads((PROJECT / "data" / "credits_manifest.json").read_text(encoding="utf-8"))

LICENSE_LABEL = {
    "cc by 2.0": "CC BY 2.0", "cc by 3.0": "CC BY 3.0", "cc by 4.0": "CC BY 4.0",
    "cc by-sa 2.0": "CC BY-SA 2.0", "cc by-sa 3.0": "CC BY-SA 3.0", "cc by-sa 4.0": "CC BY-SA 4.0",
    "cc0": "CC0", "public domain": "パブリックドメイン", "pd": "パブリックドメイン",
}

rows = []
for key in sorted(credits.keys()):
    c = credits[key]
    mm, dd = key.split("-")
    lic = c["license"].strip().lower()
    lic_label = LICENSE_LABEL.get(lic, c["license"])
    rows.append({
        "date": f"{int(mm)}/{int(dd)}",
        "sortkey": key,
        "name": c["name"],
        "artist": c["artist"] or "不明",
        "license": lic_label,
        "url": c["descriptionurl"],
        "file": c["file"],
    })

row_html = []
for r in rows:
    row_html.append(
        "<tr>"
        f'<td class="d">{html.escape(r["date"])}</td>'
        f'<td class="n">{html.escape(r["name"])}</td>'
        f'<td class="a">{html.escape(r["artist"])}</td>'
        f'<td class="l">{html.escape(r["license"])}</td>'
        f'<td class="u"><a href="{html.escape(r["url"])}" target="_blank" rel="noopener">Wikimedia Commons</a></td>'
        "</tr>"
    )

html_out = f"""<!DOCTYPE html>
<html lang="ja"><head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>はなごよみ - 写真クレジット</title>
<style>
  :root{{--ink:#3D3550;--sub:#8E84A8;--pink:#FF4D8D;--purple:#9B5CF6;--card:#FFFFFF}}
  *{{box-sizing:border-box}}
  body{{
    font-family:"Hiragino Maru Gothic ProN","Zen Maru Gothic","BIZ UDGothic","Yu Gothic UI",sans-serif;
    background:linear-gradient(200deg,#FFD6E8,#FFE9C9,#D6F5FF,#EBD9FF);
    color:var(--ink); margin:0; padding:20px 12px 40px;
  }}
  h1{{
    text-align:center;font-size:22px;margin:8px 0 4px;
    background:linear-gradient(135deg,var(--pink),var(--purple));
    -webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent;
  }}
  .lead{{text-align:center;color:var(--sub);font-size:13px;margin-bottom:18px}}
  .backlink{{display:block;text-align:center;margin-bottom:18px;color:var(--purple);font-weight:bold;text-decoration:none}}
  .wrap{{max-width:900px;margin:0 auto;background:var(--card);border-radius:18px;padding:8px 4px;
    box-shadow:0 10px 26px rgba(155,92,246,.15);overflow-x:auto}}
  table{{border-collapse:collapse;width:100%;font-size:13px}}
  th,td{{padding:7px 10px;text-align:left;border-bottom:1px solid #F0EAFA;white-space:nowrap}}
  th{{color:var(--sub);font-size:12px;position:sticky;top:0;background:var(--card)}}
  td.n{{font-weight:bold}}
  a{{color:var(--pink)}}
  .note{{max-width:900px;margin:16px auto 0;font-size:12px;color:var(--sub);line-height:1.7}}
</style>
</head>
<body>
<h1>📷 写真のクレジット・出典一覧</h1>
<div class="lead">「はなごよみ」で使用している花の写真は、すべて Wikimedia Commons のフリー素材(パブリックドメイン / CC0 / CC BY / CC BY-SA)です。</div>
<a class="backlink" href="index.html">← はなごよみ に もどる</a>
<div class="wrap">
<table>
<thead><tr><th>日付</th><th>花</th><th>作者</th><th>ライセンス</th><th>出典</th></tr></thead>
<tbody>
{"".join(row_html)}
</tbody>
</table>
</div>
<div class="note">
  ※ 写真が用意できなかった日は、アプリ内でイラスト表示に自動で切り替わります(全366日中{len(rows)}日分の写真を掲載)。<br>
  ※ 各画像はオリジナルを長辺640pxにリサイズしたものを使用しています。作者名は Wikimedia Commons のファイルページに記載の情報をもとに表示しています。
</div>
</body></html>
"""

(PROJECT / "credits.html").write_text(html_out, encoding="utf-8")
print("wrote credits.html, rows:", len(rows))
