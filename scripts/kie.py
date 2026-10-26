"""
kie.py: Kie.ai gpt-image-2 image-to-image. Flat 6 credits ($0.03) per 1K image, no quality setting.
Used by ref_generate.py for reference-image finals. Key: KIE_API_KEY in the skill folder's .env.
"""
import base64, json, mimetypes, os, time, urllib.request

API = "https://api.kie.ai/api/v1"
UPLOAD = "https://kieai.redpandaai.co/api/file-base64-upload"  # uploads expire after 3 days
RATIOS = {"1:1": 1, "3:2": 1.5, "2:3": 2/3, "4:3": 4/3, "3:4": 0.75, "5:4": 1.25, "4:5": 0.8,
          "16:9": 16/9, "9:16": 9/16, "2:1": 2, "1:2": 0.5, "3:1": 3, "1:3": 1/3, "21:9": 21/9, "9:21": 9/21}
PRESETS = {"square_hd": "1:1", "square": "1:1", "landscape_4_3": "4:3", "portrait_4_3": "3:4",
           "landscape_16_9": "16:9", "portrait_16_9": "9:16"}

def _call(method, url, body=None):
    req = urllib.request.Request(url, method=method, data=json.dumps(body).encode() if body else None,
                                 headers={"Authorization": f"Bearer {os.environ['KIE_API_KEY']}",
                                          "Content-Type": "application/json"})
    r = json.loads(urllib.request.urlopen(req, timeout=120).read())
    if r.get("code") != 200:  # Kie returns HTTP 200 on errors too
        raise RuntimeError(f"Kie {url}: {r.get('code')} {r.get('msg')}")
    return r["data"]

def aspect(size):
    """WxH or a fal preset -> nearest Kie aspect ratio. Kie 1K picks its own pixel size for that ratio."""
    if size in PRESETS:
        return PRESETS[size]
    w, h = (int(x) for x in size.lower().split("x"))
    return min(RATIOS, key=lambda k: abs(RATIOS[k] - w / h))

def upload(path):
    mime = mimetypes.guess_type(str(path))[0] or "image/png"
    data = f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode()
    d = _call("POST", UPLOAD, {"base64Data": data, "uploadPath": "image-factory", "fileName": path.name})
    return d.get("downloadUrl") or d.get("fileUrl") or d["url"]

def edit(paths, prompt, size):
    """Returns the result image URL. Polls every 4s, gives up after 5 minutes."""
    inp = {"prompt": prompt, "input_urls": [upload(p) for p in paths],
           "aspect_ratio": aspect(size), "resolution": "1K"}
    task = _call("POST", f"{API}/jobs/createTask", {"model": "gpt-image-2-image-to-image", "input": inp})["taskId"]
    for _ in range(75):
        d = _call("GET", f"{API}/jobs/recordInfo?taskId={task}")
        if d["state"] == "success":
            return json.loads(d["resultJson"])["resultUrls"][0]
        if d["state"] == "fail":
            raise RuntimeError(f"Kie task failed: {d.get('failCode')} {d.get('failMsg')}")
        time.sleep(4)
    raise TimeoutError(f"Kie task {task} still running after 5 minutes")

if __name__ == "__main__":
    assert aspect("1536x1024") == "3:2"
    assert aspect("1536x640") == "21:9"
    assert aspect("1024x1536") == "2:3"
    assert aspect("landscape_16_9") == "16:9"
    print("ok")
