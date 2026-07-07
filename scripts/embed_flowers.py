# -*- coding: utf-8 -*-
"""data/flowers.json の内容を index.html の埋め込み FLOWERS 変数に反映しなおす。
data/flowers.json を編集した後は、このスクリプトを実行してから index.html をコミットしてください。
"""
import json
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent
idx = PROJECT / "index.html"
flowers = json.loads((PROJECT / "data" / "flowers.json").read_text(encoding="utf-8"))

html = idx.read_text(encoding="utf-8")

start_marker = "/* ---------- 365日ぶんの花データ(data/flowers.json を同梱) ---------- */\nvar FLOWERS = "
end_idx_marker = ";\n\n/* ---------- ガチャの中身 ---------- */"

si = html.index(start_marker)
ei = html.index(end_idx_marker, si)

compact = json.dumps(flowers, ensure_ascii=False, separators=(",", ":"))
new_block = start_marker + compact

html = html[:si] + new_block + html[ei:]
idx.write_text(html, encoding="utf-8")
print("Re-embedded FLOWERS into index.html. Days:", len(flowers))
