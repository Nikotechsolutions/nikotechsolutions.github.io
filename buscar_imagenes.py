#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BUSCAR IMÁGENES DE PRODUCTOS - NikotechSolutions
================================================
Lee LISTA_IMAGENES_PENDIENTES.csv, busca una foto por producto en internet,
la convierte a 640x640 (fondo blanco, formato webp) y la guarda en img/<archivo>.

USO (en la terminal de GitHub Codespaces, dentro de la carpeta del repositorio):
  pip install -U ddgs pillow requests
  python buscar_imagenes.py --limite 10          # PRUEBA con 10 productos
  python buscar_imagenes.py                      # todos los pendientes
  python buscar_imagenes.py --categoria celulares
  python buscar_imagenes.py --ids 295,301 --intento 2 --forzar   # otra foto distinta
  python buscar_imagenes.py --solo-hojas         # solo regenerar hojas de revisión

Después de cada corrida revisa las hojas en  revision/hoja_XX.jpg
Borra de img/ las fotos que estén mal y repite con --ids ... --intento 2.
Las fuentes quedan anotadas en revision/imagenes_log.csv.
"""
import argparse, csv, io, os, random, re, sys, time
from urllib.parse import urlparse
import requests
from PIL import Image, ImageChops, ImageDraw

SIZE = 640
OUT = 'img'
REV = 'revision'
LOG = os.path.join(REV, 'imagenes_log.csv')
UA = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36'}
MALOS = ('pinterest', 'facebook', 'instagram', 'alamy', 'shutterstock', 'istockphoto', 'gettyimages', 'dreamstime', '123rf',
         'depositphotos', 'tiktok', 'youtube', 'ytimg', 'twimg')


def limpiar(producto, marca):
    p = re.sub(r'\(ref\.[^)]*\)', '', producto)
    p = re.sub(r'\((versión CN|variante \d)\)', '', p, flags=re.I)
    p = p.replace('"', ' pulgadas ').replace('”', ' ')
    p = re.sub(r'\s+', ' ', p).strip()
    if marca and marca.lower() not in p.lower():
        p = marca + ' ' + p
    return p


def buscar(consulta, n=12):
    try:
        from ddgs import DDGS
    except ImportError:
        sys.exit('Falta instalar: pip install -U ddgs pillow requests')
    return DDGS().images(consulta, max_results=n) or []


def candidatos(resultados):
    ok = []
    for r in resultados:
        url = r.get('image') or ''
        host = urlparse(url).netloc.lower()
        if not url.startswith('http') or any(m in host for m in MALOS): continue
        if re.search(r'\.(svg|gif)(\?|$)', url, re.I): continue
        w, h = int(r.get('width') or 0), int(r.get('height') or 0)
        if w and h and (min(w, h) < 350 or not (0.55 <= w / h <= 1.8)): continue
        ok.append(r)
    return ok


def descargar(url):
    resp = requests.get(url, headers=UA, timeout=15, stream=True)
    resp.raise_for_status()
    if 'image' not in resp.headers.get('content-type', ''): raise ValueError('no es imagen')
    datos = resp.raw.read(8 * 1024 * 1024 + 1, decode_content=True)
    if len(datos) > 8 * 1024 * 1024: raise ValueError('muy pesada')
    im = Image.open(io.BytesIO(datos)); im.load()
    return im


def procesar(im):
    if im.mode in ('RGBA', 'LA', 'P'):
        im = im.convert('RGBA'); fondo = Image.new('RGB', im.size, 'white'); fondo.paste(im, mask=im.split()[3]); im = fondo
    else:
        im = im.convert('RGB')
    w, h = im.size
    k = max(4, min(w, h) // 40)
    esq = [im.getpixel(p) for p in ((2, 2), (w - 3, 2), (2, h - 3), (w - 3, h - 3))]
    base = esq[0]
    if all(max(abs(c[i] - base[i]) for i in range(3)) < 30 for c in esq) and min(base) > 200:
        bb = ImageChops.difference(im, Image.new('RGB', im.size, base)).convert('L').point(lambda p: 255 if p > 14 else 0).getbbox()
        if bb:
            mw, mh = int((bb[2] - bb[0]) * .06) + 4, int((bb[3] - bb[1]) * .06) + 4
            im = im.crop((max(0, bb[0] - mw), max(0, bb[1] - mh), min(w, bb[2] + mw), min(h, bb[3] + mh)))
    cw, ch = im.size
    esc = min(SIZE * .92 / cw, SIZE * .92 / ch)
    im = im.resize((max(1, int(cw * esc)), max(1, int(ch * esc))), Image.LANCZOS)
    lienzo = Image.new('RGB', (SIZE, SIZE), 'white')
    lienzo.paste(im, ((SIZE - im.width) // 2, (SIZE - im.height) // 2))
    return lienzo


def hojas(filas, por=30):
    os.makedirs(REV, exist_ok=True)
    hechas = [f for f in filas if os.path.exists(os.path.join(OUT, f['archivo']))]
    for n in range(0, len(hechas), por):
        grupo = hechas[n:n + por]; cols = 6; t = 200
        filasn = (len(grupo) + cols - 1) // cols
        hoja = Image.new('RGB', (cols * t, filasn * (t + 34)), 'white'); d = ImageDraw.Draw(hoja)
        for i, f in enumerate(grupo):
            x, y = (i % cols) * t, (i // cols) * (t + 34)
            try: hoja.paste(Image.open(os.path.join(OUT, f['archivo'])).convert('RGB').resize((t, t)), (x, y))
            except Exception: pass
            d.rectangle([x, y + t, x + t, y + t + 34], fill=(245, 245, 245))
            d.text((x + 4, y + t + 3), f['archivo'].replace('.webp', ''), fill=(200, 0, 0))
            d.text((x + 4, y + t + 17), f['producto'][:34], fill=(0, 0, 0))
        hoja.save(os.path.join(REV, 'hoja_%02d.jpg' % (n // por + 1)), quality=85)
    return len(hechas)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--csv', default='LISTA_IMAGENES_PENDIENTES.csv')
    ap.add_argument('--limite', type=int, default=0)
    ap.add_argument('--ids', default='')
    ap.add_argument('--categoria', default='')
    ap.add_argument('--intento', type=int, default=1, help='usar el N-ésimo resultado válido (2 = la segunda foto)')
    ap.add_argument('--forzar', action='store_true', help='reemplazar fotos que ya existen')
    ap.add_argument('--solo-hojas', action='store_true')
    ap.add_argument('--pausa', type=float, default=2.0)
    a = ap.parse_args()
    with open(a.csv, newline='', encoding='utf-8-sig') as f:
        filas = [{'archivo': r['archivo (nombre exacto)'], 'producto': r['producto'], 'marca': r['marca'], 'categoria': r['categoria']} for r in csv.DictReader(f, delimiter=';')]
    os.makedirs(OUT, exist_ok=True); os.makedirs(REV, exist_ok=True)
    if a.solo_hojas:
        print('Hojas generadas con', hojas(filas), 'fotos en', REV); return
    ids = {i.strip().zfill(3) for i in a.ids.split(',') if i.strip()}
    sel = [f for f in filas if (not ids or f['archivo'].split('.')[0] in ids) and (not a.categoria or f['categoria'] == a.categoria)]
    if not a.forzar: sel = [f for f in sel if not os.path.exists(os.path.join(OUT, f['archivo']))]
    if a.limite: sel = sel[:a.limite]
    print(f'{len(sel)} productos por procesar.\n')
    nuevo = not os.path.exists(LOG)
    log = open(LOG, 'a', newline='', encoding='utf-8-sig'); w = csv.writer(log, delimiter=';')
    if nuevo: w.writerow(['archivo', 'producto', 'consulta', 'url_imagen', 'pagina_origen', 'estado'])
    ok = 0
    try:
        for i, f in enumerate(sel, 1):
            q = limpiar(f['producto'], f['marca']); estado = 'sin resultado'; url = pag = ''
            for intento in range(3):
                try:
                    cands = candidatos(buscar(q)); break
                except Exception as e:
                    cands = []; estado = 'error de búsqueda: ' + str(e)[:60]; time.sleep(8 * (intento + 1))
            usados = 0
            for c in cands:
                usados += 1
                if usados < a.intento: continue
                try:
                    im = descargar(c['image']); out = procesar(im)
                    out.save(os.path.join(OUT, f['archivo']), 'WEBP', quality=82, method=6)
                    url, pag, estado = c['image'], c.get('url', ''), 'ok'; ok += 1; break
                except Exception as e:
                    estado = 'no se pudo descargar: ' + str(e)[:50]
            host = urlparse(url).netloc if url else '-'
            print(f"[{i}/{len(sel)}] {f['archivo']:10} {f['producto'][:44]:44} {'✓ ' + host if estado == 'ok' else '✗ ' + estado}")
            w.writerow([f['archivo'], f['producto'], q, url, pag, estado]); log.flush()
            time.sleep(a.pausa + random.random())
    except KeyboardInterrupt:
        print('\nInterrumpido; lo ya descargado se conserva.')
    finally:
        log.close()
    n = hojas(filas)
    print(f'\nListo: {ok} fotos nuevas. Hojas de revisión en {REV}/ ({n} fotos en total). Fuentes en {LOG}')


if __name__ == '__main__':
    main()
