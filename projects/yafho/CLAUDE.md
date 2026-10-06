# Yafho SiliSkin — инструкция для Claude Code

Работаешь в репозитории OpenMontage (Arsxur1/CreateVideo), ветка `claude/portfolio-spec-vwosry`. Задача — собирать ролики про силиконовые пластыри Yafho SiliSkin по `projects/yafho/TZ.md`. Это пилот: только бесплатные инструменты, без платных API.

## Источники правды
- `projects/yafho/TZ.md` — факты, тексты титров, раскадровка, промпты. Факты не придумывать.
- `PROJECT_CONTEXT.md`, `AGENT_GUIDE.md`, `remotion-composer/SCENE_TYPES.md` — как устроен репозиторий.

## Разделение труда
- Реалистичные кадры (R): пользователь генерирует вручную в Kling (картинка → image-to-video, 5 с) и кладёт в `projects/yafho/assets/kling/` с именами `H01.mp4`, `H04.mp4`… Ты их НЕ генерируешь. Если файла нет — ставь `text_card` с подписью «нужен H0X» и продолжай.
- Абстракция, инфографика, титры, логотип, эндкард (C): делаешь кодом в `remotion-composer/`.
- Музыка: бесплатная (Pixabay Music / YouTube Audio Library), спокойный эмбиент 80–95 BPM, громкость 0.08–0.12. Файл → `projects/yafho/assets/music/`. Записать название и лицензию в `projects/yafho/CREDITS.md`.
- Голоса нет. Только крупные титры-тезисы (≤ 6 слов, ≥ 64 px при 1080×1920, держать ≥ 2.5 с).

## Порядок работ
1. Создать `styles/yafho-clinical.yaml` по схеме `schemas/styles/playbook.schema.json` (за образец — `styles/clean-professional.yaml`): primary #0F2440, accent #D4560F / #0D9488, background #FBFAF7, шрифт Onest (заголовки 800, тело 500), цифры JetBrains Mono; движения fade/slide 0.4 с, без bounce; `image_prompt_prefix` и `image_negative_prompt` — STYLE и NEGATIVE из TZ.md.
2. Новые компоненты в `remotion-composer/src/components/` (зарегистрировать в `index.ts`, `Explainer.tsx`, `SCENE_TYPES.md`):
   - `SkinCrossSection` — слои кожи, волокна коллагена (оранжевые, хаотичные → ровные), пластина опускается, плёнка влаги, пульсы сигналов замедляются. Пропсы: `phase` ("scar" | "sealed" | "healed"), подписи.
   - `MarginOverlay` — оранжевый контур «+1 см» поверх видео.
   - `TimeCounter` — «2 нед → 1 мес → 3 мес → 6 мес» поверх H08.
   - `SizeGuide` — 4 пластины на силуэты зон (тема 06).
   - `EndCard` — navy, логотип (`projects/yafho/assets/logo.png`, если нет — текст «Yafho SiliSkin»), @sil.icare, QR (сгенерировать на https://instagram.com/sil.icare).
   Для стат-карточек и графика использовать существующие `stat_card` и `line_chart`.
3. Пилот: собрать hero 50 с (таблица раздела 2 в TZ.md) в `edit_decisions` → рендер 1080×1920.
4. Из тех же клипов сделать 16:9 (1920×1080): вертикальный клип по центру/слева, справа — титр на #FBFAF7; и 4:5 (1080×1350) с кадрированием по центру.
5. Выход: `output/yafho/hero_9x16.mp4`, `hero_16x9.mp4`, `hero_4x5.mp4` + превью-кадры.

## Жёсткие правила
- Никаких обещаний «уберёт рубец», «100%», «навсегда». Только «мягче, светлее, ровнее», «снижает риск».
- Под каждой цифрой исследования — мелкий титр источника (из TZ.md 0.1).
- Нет лиц, ран, крови. Логотип и текст — только из кода, не из Kling.
- Контраст текста ≥ 4.5:1. Без градиентов и неона в графике и титрах. Исключение (решение заказчика): 3D-сцены (`skin_cross_section_3d`) — реалистичный свет и тени, палитра бренда сохраняется.
- Бюджет $0: платный инструмент — не вызывать. `build_hero.py` использует только локальные Remotion и ffmpeg. (Глобальный `config.yaml` не трогаем — его дефолт закреплён тестами и общий для других проектов.)
- После каждого этапа — показать пользователю превью и ждать одобрения (checkpoint policy guided).
