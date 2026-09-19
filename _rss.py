import urllib.request, re, json
url = "https://news.google.com/rss?gl=PE&hl=es-419&ceid=PE:es-419"
req = urllib.request.Request(url, headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
try:
    data = urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "ignore")
    titles = re.findall(r"<title><!\[CDATA\[(.*?)\]\]></title>", data)
    titles = [t for t in titles if "Google" not in t][:12]
    print("TEMAS:", len(titles))
    for t in titles:
        print("-", t)
    json.dump(titles, open("public/_temas_rss_hoy.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
except Exception as e:
    print("RSS FAIL:", repr(e))
