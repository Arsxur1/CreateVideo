# Yafho SiliSkin — контент-портфель

- `TZ.md` — ТЗ (единственный источник фактов и титров), `CLAUDE.md` — правила работы.
- `build_hero.py` — hero 50 с: собирает `artifacts/edit_decisions_hero.json` и рендерит
  `output/yafho/hero_9x16.mp4`, `hero_16x9.mp4`, `hero_4x5.mp4` + `output/yafho/previews/`.
- Стиль: `styles/yafho-clinical.yaml`. Компоненты: `remotion-composer/SCENE_TYPES.md`.

## Что положить
| Куда | Что |
|---|---|
| `assets/kling/H01.mp4`, `H04.mp4` … `H08.mp4` | клипы Kling по промптам TZ §2 (без файла — заглушка «нужен H0X») |
| `assets/music/<трек>.mp3` | один бесплатный эмбиент-трек 80–95 BPM → вписать в `CREDITS.md` |
| `assets/logo.png` | логотип (без файла — текстовый «Yafho SiliSkin») |

## Рендер
```bash
cd remotion-composer && npm ci && cd ..
pip install qrcode
python projects/yafho/build_hero.py              # все форматы
python projects/yafho/build_hero.py --only 9x16  # один формат
python projects/yafho/build_hero.py --cross-section 2d  # плоская схема вместо 3D (быстрее)
```
В закрытых сетях (нет доступа к fonts.gstatic.com / remotion.media):
`REMOTION_OFFLINE_GOOGLE_FONTS=1 REMOTION_BROWSER_EXECUTABLE=/path/to/headless_shell python projects/yafho/build_hero.py`.
Шрифты Yafho лежат локально в `remotion-composer/public/fonts/yafho`.

Положение контура «+1 см» (H06) подгоняется под реальный клип: `scarBox`/`marginPx` в `build_hero.py`.
