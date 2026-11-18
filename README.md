# Az ókori Róma térképe – Ancient Rome map

Interaktív térkép az ókori Róma városáról és a Római Birodalomról, magyarul és angolul.

Élő oldal: https://eidmar-roma.netlify.app

## Mi hol van

- `docs/` – a kész, közzétett térkép, ugyanaz, ami a weboldalon fut. Építés nem kell hozzá, statikus fájlok.
  - `index.html` (magyar), `en.html` (angol) – Róma városa
  - `imperium.html`, `imperium_en.html` – a Római Birodalom térképe
  - `imp_*`, `tiles/`, `imp_info/`, `imp_img/`, `imp_st/`, `st_*.json` – a birodalmi térkép adatai, csempéi, adatlapjai és statisztikái
  - `rm_img_0.json`, `rm_img_1.json` – a római épületkártyák fényképei (Wikimedia Commons, szerzővel és licenccel)
  - `lt_*.webp`, `nolli_v.webp`, `relief*.{json,webp}` – a háttérrétegek
- `epites/` – az építési lánc: a Róma-térkép forrása (`body.html`, `body_en.html`, `style.css`), a kártyák számításai témánként, a birodalmi térkép építői (`epites/imperium/build_page.py`, `page_tpl.html`, `data/*.py`).

A letöltött nyers adatbázisok (DARE, Pleiades, Itiner-e, AWMC, SITAR, OSM stb.) és a régi, kerületenkénti építés szkriptjei nincsenek a repóban. Az adatforrásokat és a módszertant a térkép kártyái és a módszertani dokumentum sorolják fel.

## Helyi megnyitás

A `docs/` mappát bármilyen statikus webszerverrel ki lehet szolgálni, például:

```
cd docs
python3 -m http.server 8000
```

Utána: http://localhost:8000/index.html

## Források és licencek

A térkép adatai nyilvános tudományos adatbázisokból és szakirodalomból származnak; a források minden kártyán közvetlenül az adat alatt szerepelnek. A fényképek a Wikimedia Commonsról valók, a képaláírásban a szerzővel és a licenccel.
