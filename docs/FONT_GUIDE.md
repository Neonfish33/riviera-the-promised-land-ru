# Шрифт: как устроен и как править

## Что это

`Font.png` — лист тайлов **16×12**, каждый тайл **10×10** (4bpp).
В игре используется так:

| Тайлы | Содержимое |
|---|---|
| 0–32 | заглавные А–Я |
| 33–65 | строчные а–я |
| 66–89 | пусто |
| 90–99 | цифры 0–9 |
| 100–125 | латиница A–Z |
| 126–151 | латиница a–z |
| 152–179 | пунктуация |

Тело буквы — индекс палитры **6** (белый), тень — **2** (серый, +1 px вниз-вправо),
фон — **0**. Базовая линия: заглавные — строки 1–7, строчные — 3–7,
выносные элементы — строка 8.

## Текущий способ

Кириллица генерируется из **Arial Narrow Bold 9px** (`build_font3.py`):

```bash
python tools/build_font3.py     # тайлы 0–65 из TTF + автотень, латиница не трогается
python tools/build_widths.py    # ширины глифов (сжатие до уровня латиницы)
printf 'y\n' | python tools/Font_Inserter.py   # вставка в Insert/TPL.gba
```

Особенности:
- `Й → И`, `Ё → Е` — диакритика в 10 px не читается, сделано намеренно.
- Ширины берутся из `Widths.txt` (180 значений, по одному на тайл); игра
  принимает 1–10 px.
- Если правишь `Font.png` вручную (Aseprite/GIMP, индексированные цвета),
  после правки всё равно запусти `build_widths.py` и `Font_Inserter.py`.

## Пересборка текста

```bash
cp Insert/TPL.gba Insert/TPL_translation.gba
for f in Scripts/tpl_script_*.txt; do
  python tools/insert_custom.py Insert/TPL_translation.gba "$f" \
      translations.json Insert/IN.tbl Insert/TPL_translation.gba
done
```
