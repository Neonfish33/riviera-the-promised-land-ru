# Riviera: The Promised Land — русский перевод (GBA)

Незавершённый проект другого автора ([343github/Riviera_ThePromisedLand](https://github.com/343github/Riviera_ThePromisedLand))
доведён до рабочего состояния: полный перевод текста, импорт шрифта и собственный
вставщик, обходящий переполнение Atlas.

## Что сделано

- **Перевод**: 12 452 из 12 557 строк (99,2%) — сюжет, меню, бой, справочники,
  предметы, умения. Не переведены титры (сырые байты), логотип (графика) и
  несколько плейсхолдеров.
- **Шрифт**: кириллица импортирована из Arial Narrow Bold 9px в тайлы 0–65
  (10×10, автотень), латиница остаётся в тайлах 90–179. `Й→И`, `Ё→Е`
  (намеренное упрощение, чтобы не рисовать диакритику в 10px).
- **Вставка текста**: `tools/insert_custom.py` кодирует строки по `IN.tbl`,
  **дедуплицирует** одинаковые строки и пишет 24-битные указатели прямо в ROM —
  это обходит переполнение штатного Atlas.
- **Ширины**: `tools/build_widths.py` считает ширины из атласа и сжимает
  кириллицу до уровня латиницы (иначе русские строки не влезают в рамки).

## Сборка

Нужны: своя копия ROM `Riviera - Promised Land (U) [!].gba`, Python 3 + Pillow,
Arial Narrow Bold (`C:\Windows\Fonts\arialnb.ttf`).

```bash
# 1. извлечь оригинальный шрифт из ROM в Font.png
python tools/Font_Extractor.py

# 2. нарисовать кириллицу (импорт TTF) и пересчитать ширины
python tools/build_font3.py
python tools/build_widths.py

# 3. вставить шрифт и патчи в Insert/TPL.gba
python tools/Font_Inserter.py

# 4. вставить перевод во все 40 скриптов
cp Insert/TPL.gba Insert/TPL_translation.gba
for f in Scripts/tpl_script_*.txt; do
  python tools/insert_custom.py Insert/TPL_translation.gba "$f" translations.json Insert/IN.tbl Insert/TPL_translation.gba
done
```

Результат — `Insert/TPL_translation.gba`.

## Документация

- [docs/REVERSE_ENGINEERING.md](docs/REVERSE_ENGINEERING.md) — карта проекта, форматы, адреса патчей и план порта на Android.
- [docs/FONT_GUIDE.md](docs/FONT_GUIDE.md) — формат шрифта и правка атласа.
- [docs/glossary.md](docs/glossary.md) — глоссарий перевода.

## Структура

```
tools/        сборка шрифта, ширин, вставка текста, рендер-превью
docs/         гайд по шрифту и глоссарий
Scripts/      Atlas-скрипты (оригинальный текст игры из upstream-репозитория)
translations.json   перевод: {английская строка: русская строка}
Insert/IN.tbl таблица символов (русские буквы -> байты AA..EB)
Widths.txt    ширины глифов (180 значений)
```

## Известные проблемы

- Часть плашек/меню может обрезаться: переносы строк в переводе ручные (`<line>`),
  шрифт шире оригинального. Правка — в `translations.json` (перенести слово).
- Титры и логотип не переведены (не текст).
- Стиль кириллицы отличается от оригинальной латиницы (импорт TTF, не ручная
  пиксель-графика).

## Благодарности

- [343github/Riviera_ThePromisedLand](https://github.com/343github/Riviera_ThePromisedLand) —
  Atlas-скрипты, извлечение/вставка шрифта, исходная структура проекта.

## Правовой статус

ROM и графика игры не входят в репозиторий. `Scripts/` — текстовые скрипты из
upstream-проекта. Перевод — работа участников этого проекта. Используйте только
со своей легальной копией игры.

## Лицензия

Код этого репозитория — MIT (см. LICENSE). Код upstream-инструментов сохраняет
авторство 343github; лицензия upstream не указана.
