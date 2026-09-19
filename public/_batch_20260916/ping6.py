import json, urllib.request, time
body = json.dumps({"model":"deepseek-web","messages":[{"role":"user","content":"Responde solo: OK"}],"temperature":0.7}).encode("utf-8")
req = urllib.request.Request("http://127.0.0.1:8765/v1/chat/completions", data=body, headers={"Content-Type":"application/json"})
t0=time.time()
try:
    with urllib.request.urlopen(req, timeout=75) as r:
        d = json.loads(r.read().decode("utf-8"))
    print("OK", round(time.time()-t0,1), "s ->", d["choices"][0]["message"]["content"][:200])
except Exception as e:
    print("FAIL", round(time.time()-t0,1), "s ->", repr(e))
