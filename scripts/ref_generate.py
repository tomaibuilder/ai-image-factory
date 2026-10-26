#!/usr/bin/env python3
"""
ref_generate.py: make one image from one or more reference images
via gpt-image-2 image-to-image, on fal.ai (/edit) or Kie.ai.

Usage:
  python scripts/ref_generate.py \
      --image drafts/07.png \
      --prompt "Keep this exact design, layout and text. Re-render it cleanly at full fidelity." \
      --size 1536x1024 \
      --out final_01.png

- --image can be repeated (style reference + your logo, for example).
- --size accepts WxH (e.g. 1536x1024) or a fal preset (square_hd, landscape_16_9, portrait_16_9, ...).
- --provider auto (default): Kie for finals (quality medium) when KIE_API_KEY is set,
  fal for drafts (--quality low) or when there is no Kie key. Kie has no quality setting
  ($0.03 flat at 1K). It only takes set aspect ratios, so the output is cropped to --size.
- Relative paths resolve against the current folder. Keys come from the skill folder's .env.
"""
import argparse, os, sys, pathlib, urllib.request

SKILL = pathlib.Path(__file__).resolve().parents[1]

def load_env():
    envf = SKILL / ".env"
    if envf.exists():
        for line in envf.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())

def parse_size(s):
    if "x" in s.lower():
        w, h = s.lower().split("x")
        return {"width": int(w), "height": int(h)}
    return s  # named preset

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--image", action="append", required=True, help="reference image path (repeatable)")
    ap.add_argument("--prompt", required=True)
    ap.add_argument("--size", default="1536x1024")
    ap.add_argument("--out", required=True)
    ap.add_argument("--quality", default="medium", choices=["low", "medium", "high"])
    ap.add_argument("--provider", choices=["auto", "fal", "kie"], default="auto")
    a = ap.parse_args()

    load_env()
    provider = a.provider
    if provider == "auto":
        provider = "kie" if a.quality != "low" and os.environ.get("KIE_API_KEY") else "fal"
    key = "KIE_API_KEY" if provider == "kie" else "FAL_KEY"
    if not os.environ.get(key):
        sys.exit(f"{key} missing. Add it to {SKILL / '.env'} (see .env.example).")

    paths = []
    for p in a.image:
        path = pathlib.Path(p).resolve()
        if not path.exists():
            sys.exit(f"reference not found: {path}")
        paths.append(path)
    out = pathlib.Path(a.out).resolve()
    out.parent.mkdir(parents=True, exist_ok=True)

    if provider == "kie":
        sys.path.insert(0, str(SKILL / "scripts"))
        import kie
        print(f"generating on Kie ({kie.aspect(a.size)}, 1K) ...", flush=True)
        urllib.request.urlretrieve(kie.edit(paths, a.prompt, a.size), out)
        if "x" in a.size.lower():  # Kie snaps to a ratio, so crop to the exact posting size
            from PIL import Image, ImageOps
            w, h = (int(x) for x in a.size.lower().split("x"))
            ImageOps.fit(Image.open(out), (w, h), Image.LANCZOS).save(out)
        print(f"saved {out}")
        return

    import fal_client
    urls = []
    for path in paths:
        print(f"uploading {path.name} ...", flush=True)
        urls.append(fal_client.upload_file(str(path)))
    args = {"image_urls": urls, "prompt": a.prompt, "quality": a.quality}
    if a.size:
        args["image_size"] = parse_size(a.size)
    print(f"generating on fal (/edit, quality {a.quality}) ...", flush=True)
    result = fal_client.subscribe("openai/gpt-image-2/edit", arguments=args, with_logs=False)
    imgs = result.get("images") or []
    if not imgs:
        sys.exit(f"no image returned: {result}")
    urllib.request.urlretrieve(imgs[0]["url"], out)
    print(f"saved {out}")

if __name__ == "__main__":
    main()
