# -*- coding: utf-8 -*-
"""data/flowers.json の wiki フィールドをもとに Wikimedia Commons から花の写真を収集する。
PD/CC0/CC BY/CC BY-SA のみ採用し、images/MMDD.jpg (長辺640px) と
data/credits_manifest.json / data/collect_summary.json を更新する。
"""
import json, time, io, sys
import urllib.request, urllib.parse, urllib.error
from pathlib import Path
from PIL import Image

PROJECT = Path(__file__).resolve().parent.parent
DATA = PROJECT / "data" / "flowers.json"
IMAGES = PROJECT / "images"
IMAGES.mkdir(exist_ok=True)

UA = "hanagoyomi-flower-app/1.0 (personal hobby project) Python-urllib"

ACCEPTABLE_LICENSES = {
    "pd", "public domain", "cc0", "cc0 1.0",
    "cc-by-4.0", "cc-by-3.0", "cc-by-2.5", "cc-by-2.0", "cc-by-1.0",
    "cc-by-sa-4.0", "cc-by-sa-3.0", "cc-by-sa-2.5", "cc-by-sa-2.0", "cc-by-sa-1.0",
}

def api_get(host, params):
    url = f"https://{host}/w/api.php?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.loads(r.read().decode("utf-8"))

def get_page_image_filename(title):
    j = api_get("ja.wikipedia.org", {
        "action": "query", "titles": title, "prop": "pageimages",
        "piprop": "name", "redirects": 1, "format": "json", "formatversion": 2,
    })
    pages = j.get("query", {}).get("pages", [])
    if not pages:
        return None
    p = pages[0]
    if p.get("missing"):
        return None
    return p.get("pageimage")

def get_imageinfo(filename):
    j = api_get("ja.wikipedia.org", {
        "action": "query", "titles": f"File:{filename}", "prop": "imageinfo",
        "iiprop": "extmetadata|url|size", "iiurlwidth": 900,
        "format": "json", "formatversion": 2,
    })
    pages = j.get("query", {}).get("pages", [])
    if not pages:
        return None
    p = pages[0]
    infos = p.get("imageinfo")
    if not infos:
        return None
    return infos[0]

def license_ok(extmeta):
    lic = (extmeta.get("LicenseShortName", {}).get("value")
           or extmeta.get("License", {}).get("value") or "").strip().lower()
    lic_norm = lic.replace(" ", "-")
    if lic_norm in ACCEPTABLE_LICENSES:
        return True, lic
    if "public domain" in lic or lic == "pd":
        return True, lic
    return False, lic

def strip_html(s):
    import re
    return re.sub("<[^>]+>", "", s or "").strip()

def download(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()

def main():
    flowers = json.loads(DATA.read_text(encoding="utf-8"))
    keys = sorted(flowers.keys())
    if len(sys.argv) > 1:
        keys = keys[:int(sys.argv[1])]
    results = {"ok": [], "no_image": [], "no_license": [], "error": []}
    credits = {}

    for i, key in enumerate(keys):
        entry = flowers[key]
        title = entry["wiki"]
        mmdd = key.replace("-", "")
        try:
            fn = get_page_image_filename(title)
            time.sleep(0.15)
            if not fn:
                results["no_image"].append([key, entry["name"], title])
                continue
            info = get_imageinfo(fn)
            time.sleep(0.15)
            if not info:
                results["no_image"].append([key, entry["name"], title])
                continue
            extmeta = info.get("extmetadata", {})
            ok, lic = license_ok(extmeta)
            if not ok:
                results["no_license"].append([key, entry["name"], title, lic])
                continue
            src = info.get("thumburl") or info.get("url")
            raw = download(src)
            img = Image.open(io.BytesIO(raw))
            img = img.convert("RGB")
            w, h = img.size
            longest = max(w, h)
            if longest > 640:
                scale = 640 / longest
                img = img.resize((max(1, int(w * scale)), max(1, int(h * scale))), Image.LANCZOS)
            out_path = IMAGES / f"{mmdd}.jpg"
            img.save(out_path, "JPEG", quality=85)
            artist = strip_html(extmeta.get("Artist", {}).get("value", ""))
            credits[key] = {
                "date": key, "name": entry["name"], "wiki": title,
                "file": fn, "artist": artist or "不明",
                "license": lic, "descriptionurl": info.get("descriptionurl", ""),
            }
            results["ok"].append(key)
        except Exception as e:
            results["error"].append([key, entry["name"], title, str(e)])
        if i % 20 == 0:
            print(f"progress {i+1}/{len(keys)} ok={len(results['ok'])} noimg={len(results['no_image'])} nolic={len(results['no_license'])} err={len(results['error'])}", flush=True)

    (PROJECT / "data" / "credits_manifest.json").write_text(
        json.dumps(credits, ensure_ascii=False, indent=1, sort_keys=True), encoding="utf-8")
    (PROJECT / "data" / "collect_summary.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=1), encoding="utf-8")
    print("DONE")
    print("ok:", len(results["ok"]))
    print("no_image:", len(results["no_image"]))
    print("no_license:", len(results["no_license"]))
    print("error:", len(results["error"]))

if __name__ == "__main__":
    main()
