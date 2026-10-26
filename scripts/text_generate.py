#!/usr/bin/env python3
"""
text_generate.py: generate a batch of images via fal.ai openai/gpt-image-2.

Reads a JSON batch file: a list of {"prompt": str, "size": "WxH"|preset, "out": path,
"quality": "low"|"medium" (default medium), "image": path or [paths] (optional)}.
Items with "image" go to the /edit endpoint (riff on a reference image).
Use this for the 12-draft run, with every item on quality "low".
Relative paths resolve against the current folder. FAL_KEY comes from the skill folder's .env.

Usage:
  python scripts/text_generate.py --batch drafts.json
"""
import argparse, json, os, sys, pathlib, urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed

SKILL = pathlib.Path(__file__).resolve().parents[1]

def load_env():
    envf = SKILL / ".env"
    if envf.exists():
        for line in envf.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())
    if not os.environ.get("FAL_KEY"):
        sys.exit(f"FAL_KEY missing. Add it to {envf} (see .env.example).")

def parse_size(s):
    if isinstance(s, str) and "x" in s.lower():
        w, h = s.lower().split("x")
        return {"width": int(w), "height": int(h)}
    return s

def gen(item):
    import fal_client
    args = {"prompt": item["prompt"], "quality": item.get("quality", "medium")}
    if item.get("size"):
        args["image_size"] = parse_size(item["size"])
    endpoint = "openai/gpt-image-2"
    refs = item.get("image") or []
    if refs:
        refs = [refs] if isinstance(refs, str) else refs
        args["image_urls"] = [fal_client.upload_file(str(pathlib.Path(p).resolve())) for p in refs]
        endpoint += "/edit"
    result = fal_client.subscribe(endpoint, arguments=args, with_logs=False)
    imgs = result.get("images") or []
    if not imgs:
        return (item["out"], f"ERROR: no image returned: {result}")
    out = pathlib.Path(item["out"]).resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    urllib.request.urlretrieve(imgs[0]["url"], out)
    return (str(out), "ok")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--batch", required=True)
    a = ap.parse_args()
    load_env()
    items = json.loads(pathlib.Path(a.batch).read_text())
    with ThreadPoolExecutor(max_workers=min(6, len(items))) as ex:
        futs = {ex.submit(gen, it): it["out"] for it in items}
        for f in as_completed(futs):
            try:
                out, status = f.result()
            except Exception as e:
                out, status = futs[f], f"ERROR: {e}"
            print(f"[{status}] {out}", flush=True)

if __name__ == "__main__":
    main()
