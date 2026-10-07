# Yafho-Silicare — контент-портфель

## Документы
| Файл | Что это |
|---|---|
| `TZ.md` | исходное ТЗ: факты, промпты, раскадровка пилота (название в нём устарело — см. `CLAUDE.md`) |
| `CLAUDE.md` | правила работы над проектом |
| `SCRIPT_hero_v2.md` | сценарий hero v2 «Окно перестройки» (утверждён; без голоса — титры и стрелки) |
| `hero_v2.json` | данные сцен: тайминг, титры, 3D-фазы, шкала, стрелки, форматы — **источник правды для сборки** |
| `KLING_SHOTS_v2.md` | ТЗ на 6 реальных кадров Kling (H01, H04–H08) |
| `CREDITS.md` | музыка, шрифты, лицензии |

## Что положить
| Куда | Что |
|---|---|
| `assets/kling/H01.mp4`, `H04.mp4` … `H08.mp4` | клипы Kling по `KLING_SHOTS_v2.md` (без файла — заглушка «нужен H0X») |
| `assets/logo.png` | логотип (без файла — текстовый «Yafho-Silicare») |
| `assets/music/` | музыка; по умолчанию собственный трек из `make_music.py` |

## Сборка hero v2
```bash
cd remotion-composer && npm ci && cd ..
pip install qrcode numpy
python projects/yafho/make_music.py                 # музыка под сюжет (≈10 с)
python projects/yafho/build_v2.py --final           # 9:16, 16:9, 4:5 (≈50 мин на формат: 3D на CPU)
python projects/yafho/build_v2.py --final --formats 9x16
python projects/yafho/make_cuts.py                  # 3 нарезки по 15 с из готовых роликов
```
Черновые режимы: `--animatic` (неподвижные кадры + плашки) и `--draft` (живое 3D без музыки).

Результат — `output/yafho/v2/`:
`hero_v2_9x16.mp4`, `hero_v2_16x9.mp4`, `hero_v2_4x5.mp4` + `*_sheet.png`,
`cut_A_*.mp4` «Почему рубец остаётся», `cut_B_*.mp4` «Как работает силикон», `cut_C_*.mp4` «Как наклеить».

Когда появятся клипы Kling — положить в `assets/kling/` и запустить `build_v2.py --final` и `make_cuts.py` заново.
Контур «+1 см» подгоняется под реальный H06 в `hero_v2.json` → сцена `S11b` → `margin.scarBox`.

## Закрытые сети
Если нет доступа к fonts.gstatic.com или remotion.media:
`REMOTION_OFFLINE_GOOGLE_FONTS=1 REMOTION_BROWSER_EXECUTABLE=/path/to/headless_shell python projects/yafho/build_v2.py --final`.
Шрифты Yafho лежат локально в `remotion-composer/public/fonts/yafho`. 3D рендерится через `REMOTION_GL=angle` (ставится автоматически).

## Hero v1 (пилот 50 с, по разделу 2 ТЗ)
`python projects/yafho/build_hero.py` → `output/yafho/hero_*.mp4`.
