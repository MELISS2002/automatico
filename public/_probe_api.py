# -*- coding: utf-8 -*-
import json, urllib.request
url = "http://127.0.0.1:8765/v1/chat/completions"
body = json.dumps({"model": "deepseek-web", "messages": [{"role": "user", "content": "Responde solo: OK"}], "stream": False}).encode("utf-8")
req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"})
try:
    with urllib.request.urlopen(req, timeout=60) as r:
        print("STATUS", r.status)
        print(r.read().decode("utf-8", "replace")[:500])
except Exception as e:
    print("ERROR", repr(e))
