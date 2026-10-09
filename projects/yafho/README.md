# Yafho-Silicare — контент-портфель

## Документы
| Файл | Что это |
|---|---|
| `TZ.md` | исходное ТЗ: факты, промпты, раскадровка пилота (название в нём устарело — см. `CLAUDE.md`) |
| `CLAUDE.md` | правила работы над проектом |
| `CONCEPT_v3.md` | **hero v3 «Один рубец — два исхода»** — основная версия: крючок-эффект, смысл, охват, нарезки по аудиториям |
| `hero_v3.json` | данные сцен v3 (тайминг, титры, сравнение, плашки, музыка, карточки и нарезки аудиторий) |
| `SCRIPT_hero_v2.md` | сценарий hero v2 «Окно перестройки» — длинная версия (YouTube, врачи) |
| `hero_v2.json` | данные сцен: тайминг, титры, 3D-фазы, шкала, стрелки, форматы — **источник правды для сборки** |
| `KLING_SHOTS_v2.md` | ТЗ на 6 реальных кадров Kling (H01, H04–H08) |
| `TOPICS_v1.md` | **серия тем 01–09 (ТЗ §3)**: крючок, смысл, охват и раскадровка каждого ролика |
| `TOPICS_v2.md` | **серия 2 (темы 10–17)**: когда начинать, день с пластиной, когда нельзя, вопрос-ответ, 4 ролика под аудитории; сторис 6–10 с |
| `topics/topic_NN.json` | данные сцен каждой темы (тот же формат, что `hero_v3.json`); серию 2 пишет `topics/series2.py` |
| `CONTENT_PLAN.md` | порядок публикаций на 4 недели, подписи к постам, интерактив для сторис |
| `CREDITS.md` | музыка, шрифты, лицензии |

## Что положить
| Куда | Что |
|---|---|
| `assets/kling/H01.mp4`, `H04.mp4` … `H08.mp4` | клипы Kling по `KLING_SHOTS_v2.md` (без файла — заглушка «нужен H0X») |
| `assets/logo.png` | логотип (без файла — текстовый «Yafho-Silicare») |
| `assets/music/` | музыка; по умолчанию собственный трек из `make_music.py` |
| `assets/brand/` | фон бренда с сайта Yafho (`backdrop.png` или по форматам) |
| `assets/kling/P01.mp4` … `P03.mp4` | кадры аудиторий для нарезок v3 (`KLING_SHOTS_v2.md`, раздел 6) |

## Сборка hero v3 (основная)
```bash
python projects/yafho/make_backdrop.py                                   # фон бренда (пока — лён)
python projects/yafho/make_music.py --data projects/yafho/hero_v3.json   # музыка под v3
python projects/yafho/build_v2.py  --data projects/yafho/hero_v3.json --final          # 9:16, 16:9, 4:5
python projects/yafho/build_v2.py  --data projects/yafho/hero_v3.json --cards          # карточки аудиторий
python projects/yafho/make_cuts.py --data projects/yafho/hero_v3.json                  # нарезки K, O, B, G по 15 с
```
Результат — `output/yafho/v3/`: `hero_v3_<формат>.mp4`, `cut_<K|O|B|G>_<формат>.mp4`.

**Фон бренда.** Положите картинку с сайта Yafho в `assets/brand/backdrop.png` (или `backdrop_1080x1920.png`, `backdrop_1920x1080.png`, `backdrop_1080x1350.png` под каждый формат) — сборка возьмёт её вместо сгенерированного льна.

## Сборка серии тем 01–09
```bash
bash projects/yafho/build_topics.sh                        # все темы, 9:16
bash projects/yafho/build_topics.sh 9x16,16x9,4x5          # все форматы
bash projects/yafho/build_topics.sh 9x16,16x9,4x5 04 05    # выбранные темы
```
Результат — `output/yafho/topics/`: `topic_<NN>_<формат>.mp4`, контактный лист `_sheet.png` и картинка-пост `_cover.png`.
Сторис 6–10 с: `python projects/yafho/make_cuts.py --data projects/yafho/topics/topic_NN.json --formats 9x16` → `topic_NN_story_S_9x16.mp4`.
Музыка каждой темы — `assets/music/yafho_topic_<NN>.wav` (`make_music.py --data topics/topic_<NN>.json`).
Кожа сверху (`skin_demo`) рисуется кодом: `make_skin.py` генерирует фото-текстуры кожи с рубцами один раз (≈ 1,5 мин), сборка вызывает его сама.
Кадры Kling для тем не обязательны: каждый шаг уже нарисован. Чтобы поставить реальный кадр вместо рисунка, замените у сцены `"kind": "CUT"` на `"kind": "R"` и `"kling": "H05"` (файл в `assets/kling/`).

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
