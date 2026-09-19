import json, urllib.request
prompt = "Eres redactor web. Escribe en espanol un articulo de 400 palabras titulado TRUCOS CASEROS PARA BAJAR EL COLESTEROL. Devuelve SOLO el texto del articulo, sin markdown."
body = json.dumps({"model":"kimi-web","messages":[{"role":"user","content":prompt}],"temperature":0.4}).encode()
req = urllib.request.Request("http://127.0.0.1:8767/v1/chat/completions", data=body, headers={"Content-Type":"application/json"})
try:
    r = urllib.request.urlopen(req, timeout=240)
    d = json.loads(r.read().decode())
    c = d["choices"][0]["message"]["content"]
    print("LEN:", len(c))
    print(c[:400])
except Exception as e:
    print("KIMI ERR:", repr(e))
