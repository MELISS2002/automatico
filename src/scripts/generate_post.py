from transformers import pipeline
from datetime import datetime
import os

# 1. Configurar modelo de resumen (gratis)
summarizer = pipeline("summarization", model="t5-small")

# 2. Texto fuente (ejemplo)
raw_text = """
En un emocionante partido de la Premier League, 
Manchester United derrotó 3-2 al Liverpool con un gol 
de último minuto de Marcus Rashford.
"""

# 3. Generar resumen
summary = summarizer(raw_text, max_length=100)[0]['summary_text']

# 4. Crear nombre de archivo
today = datetime.now().strftime("%Y-%m-%d")
filename = f"../posts/{today}-manutd-liverpool.md"

# 5. Formato Markdown para React
content = f"""---
title: "Resumen: Manchester United vs Liverpool"
date: "{today}"
---

{summary}

**Detalles Clave**:
- Goles: 3-2
- MVP: Marcus Rashford
- Estadio: Old Trafford
"""

# 6. Guardar archivo
with open(filename, "w") as f:
    f.write(content)