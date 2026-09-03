// functions/api/viral-views/[id].js
// Contador de vistas para la app viral. Usa KV si hay binding (VIEWS_KV),
// con fallback a un mapa en memoria (no persiste entre instancias/redeploys).
// GET  /api/viral-views/:id  -> lee el contador
// POST /api/viral-views/:id  -> incrementa y lo devuelve
const KV = typeof VIEWS_KV !== 'undefined' ? VIEWS_KV : null;

// fallback en memoria por instancia
const mem = new Map();

async function getCount(id) {
  if (KV) {
    const v = await KV.get(id, { type: 'json' });
    return (v && typeof v === 'number') ? v : 0;
  }
  return mem.get(id) || 0;
}

async function setCount(id, n) {
  if (KV) {
    await KV.put(id, n);
    return;
  }
  mem.set(id, n);
}

function json(obj, status = 200) {
  return new Response(JSON.stringify(obj), {
    status,
    headers: {
      'Content-Type': 'application/json; charset=utf-8',
      'Access-Control-Allow-Origin': '*',
      'Cache-Control': 'no-store',
    },
  });
}

export async function onRequest(context) {
  const id = (context.params.id || '').toString().slice(0, 120);
  if (!id) return json({ error: 'missing id' }, 400);

  try {
    if (context.request.method === 'POST') {
      const cur = await getCount(id);
      await setCount(id, cur + 1);
      return json({ id, views: cur + 1 });
    }
    // GET
    const views = await getCount(id);
    return json({ id, views });
  } catch (e) {
    return json({ error: String(e && e.message) }, 500);
  }
}

export const onRequestGet = (ctx) => onRequest(ctx);
export const onRequestPost = (ctx) => onRequest(ctx);