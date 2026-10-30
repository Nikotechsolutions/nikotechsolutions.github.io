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
MALOS = ('canva', 'etsy', 'pinterest', 'facebook', 'instagram', 'alamy', 'shutterstock', 'istockphoto', 'gettyimages', 'dreamstime', '123rf',
         'depositphotos', 'tiktok', 'youtube', 'ytimg', 'twimg')


ALIAS = {'POCO': 'Xiaomi POCO', 'Galaxy': 'Samsung Galaxy'}
CATPAL = {'celulares': 'smartphone', 'tablets': 'tablet', 'portatiles': 'laptop', 'computadores': 'computador', 'monitores': 'monitor',
          'televisores': 'smart tv', 'audio': 'audífonos', 'smartwatch': 'smartwatch', 'cargadores': 'cargador', 'perifericos': '',
          'almacenamiento': '', 'impresion': 'impresora', 'redes': '', 'hogar': '', 'energia': '', 'software': 'licencia caja', 'fundas': 'funda'}


def limpiar(producto, marca, categoria='', nivel=1):
    p = re.sub(r'\(ref\.[^)]*\)', '', producto)
    p = re.sub(r'\((versión CN|variante \d)\)', '', p, flags=re.I)
    p = p.replace('"', ' pulgadas ').replace('”', ' ')
    p = re.sub(r'\s+', ' ', p).strip()
    if marca and marca.lower() not in p.lower():
        p = marca + ' ' + p
    for k, v in ALIAS.items():                      # evita palabras ambiguas (p. ej. "Poco")
        p = re.sub(r'\b%s\b' % re.escape(k), v, p, count=1, flags=re.I) if (k.lower() in p.lower() and v.lower() not in p.lower()) else p
    if nivel >= 2:                                  # búsqueda más simple: sin tipo ni código largo
        p = re.sub(r'^(Celular|Portátil|Tablet|Televisor|Todo en uno|Memoria USB|Disco)\s+', '', p, flags=re.I)
        p = re.sub(r'\b[A-Z]{2,3}-[A-Z0-9]{3,}\b', '', p)
    if nivel >= 3:
        p = ' '.join(p.split()[:4])
    pal = CATPAL.get(categoria, '')
    if pal and pal.lower() not in p.lower(): p += ' ' + pal
    return re.sub(r'\s+', ' ', p).strip()


def buscar(consulta, n=12):
    try:
        from ddgs import DDGS
    except ImportError:
        sys.exit('Falta instalar: pip install -U ddgs pillow requests')
    return DDGS().images(consulta, max_results=n) or []


GENERICAS = {'celular', 'portatil', 'portátil', 'tablet', 'televisor', 'memoria', 'disco', 'para', 'con', 'smartwatch', 'audifonos', 'audífonos',
             'cargador', 'adaptador', 'mouse', 'teclado', 'monitor', 'impresora', 'router', 'switch', 'licencia', 'smart', 'gaming', 'inalambrico'}


def relevante(r, producto, marca=''):
    """El resultado debe mencionar el modelo COMO PALABRA COMPLETA (no dentro de un código al azar) y, si hay marca, la marca."""
    raw = ((r.get('title') or '') + ' ' + (r.get('url') or '') + ' ' + (r.get('image') or '')).lower()
    words = set(re.split(r'[^a-z0-9]+', raw)); joined = raw.replace('-', '').replace(' ', '')
    p = re.sub(r'\(.*?\)', ' ', producto).lower()
    if marca:
        b = re.sub(r'[^a-z0-9]', '', marca.lower())
        if b and b not in joined and not (b == 'xiaomi' and ('redmi' in words or 'poco' in words)): return False
    modelos = [t.replace('-', '') for t in re.findall(r'[a-z0-9\-]*\d[a-z0-9\-]*', p) if len(t.replace('-', '')) >= 2 and not re.fullmatch(r'\d+(gb|tb|w|mah|hz|mm|pulgadas)?', t)]
    if modelos:
        segs = set(modelos)
        for t in re.findall(r'[a-z0-9\-]*\d[a-z0-9\-]*', p):
            for seg in t.split('-'):
                if len(seg) >= 5 and re.search(r'\d', seg) and re.search(r'[a-z]', seg): segs.add(seg)
        for m in segs:
            if len(m) < 5:                     # modelos cortos (s25, a07, c71, 17): solo como palabra completa
                if m in words or any(w.startswith(m) and not w[len(m):len(m)+1].isdigit() for w in words if len(w) <= len(m) + 3 and w.startswith(m)): return True
            elif m in joined: return True
        return False
    palabras = [w for w in re.findall(r'[a-záéíóúñ]{4,}', p) if w not in GENERICAS]
    return sum(1 for w in palabras if w.replace(' ', '') in joined) >= min(2, max(1, len(palabras)))


def candidatos(resultados, producto='', marca='', filtrar=True, exigir=''):
    ok = []
    for r in resultados:
        url = r.get('image') or ''
        host = urlparse(url).netloc.lower()
        if not url.startswith('http') or any(m in host for m in MALOS): continue
        if re.search(r'\.(svg|gif)(\?|$)', url, re.I): continue
        w, h = int(r.get('width') or 0), int(r.get('height') or 0)
        if w and h and (min(w, h) < 350 or not (0.55 <= w / h <= 1.8)): continue
        if filtrar and producto and not relevante(r, producto, marca): continue
        if exigir and not re.search(exigir, ((r.get('title') or '') + ' ' + (r.get('url') or '') + ' ' + (r.get('image') or '')).lower()): continue
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
    ap.add_argument('--sin-filtro', action='store_true', help='aceptar resultados aunque no mencionen el modelo (puede traer fotos equivocadas)')
    ap.add_argument('--forzar', action='store_true', help='reemplazar fotos que ya existen')
    ap.add_argument('--solo-hojas', action='store_true')
    ap.add_argument('--pausa', type=float, default=2.0)
    ap.add_argument('--sufijo', default='', help='palabras extra para la búsqueda, p. ej. --sufijo "celular png"')
    a = ap.parse_args()
    with open(a.csv, newline='', encoding='utf-8-sig') as f:
        filas = [{'archivo': r['archivo (nombre exacto)'], 'producto': r['producto'], 'marca': r['marca'], 'categoria': r['categoria'], 'exigir': (r.get('exigir_color') or '').strip()} for r in csv.DictReader(f, delimiter=';')]
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
            estado = 'sin resultado'; url = pag = ''; q = ''
            for nivel in (1, 2, 3):
                q = limpiar(f['producto'], f['marca'], f['categoria'], nivel) + (' ' + a.sufijo if a.sufijo else '')
                cands = []
                for intento in range(3):
                    try:
                        cands = candidatos(buscar(q), f['producto'], f['marca'], not a.sin_filtro, f.get('exigir', '')); break
                    except Exception as e:
                        estado = 'error de búsqueda: ' + str(e)[:60]; time.sleep(8 * (intento + 1))
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
                if estado == 'ok': break
                time.sleep(1)
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
