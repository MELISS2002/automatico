import sys, os
sys.path.insert(0, r"C:\Users\dza\Desktop\automatico-main\public")
import crear_lote_api as L
L.ARTICULOS = [("Trucos caseros para bajar el colesterol alto de forma natural", "salud", "trucos-caseros-bajar-colesterol-natural")]
def bp(t):
    return ("Eres redactor web. Crea un articulo HTML sobre " + chr(34)+t+chr(34) + " (900 palabras) con datos reales. Usa exactamente src=\"imagen1.jpg\", src=\"imagen2.jpg\", src=\"imagen3.jpg\" (locales). CSS atractivo. NO backticks.\nTITLE: ...\nEXCERPT: ...\n===HTML_START===\n(HTML)\n===HTML_END===\nTHUMBNAIL: imagen1.jpg\n")
L.build_prompt = bp
import auto1
auto1.GIT_ACTIVO = False
r = L.call_api(L.build_prompt(L.ARTICULOS[0][0]))
print("CHARS:", len(r))
print(r[:200])
