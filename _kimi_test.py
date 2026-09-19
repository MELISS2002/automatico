import json, urllib.request
body = json.dumps({"model":"kimi-web","messages":[{"role":"user","content":"Escribe un parrafo de 60 palabras sobre bajar el colesterol de forma natural. Solo el texto, sin titulo."}],"temperature":0.3}).encode()
req = urllib.request.Request("http://127.0.0.1:8767/v1/chat/completions", data=body, headers={"Content-Type":"application/json"})
try:
    r = urllib.request.urlopen(req, timeout=180)
    d = json.loads(r.read().decode())
    c = d["choices"][0]["message"]["content"]
    print("LEN:", len(c))
    print(c[:300])
except Exception as e:
    print("ERR:", repr(e))
