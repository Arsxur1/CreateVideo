# ТЗ: картинки и видео Yafho SiliSkin (пилот, бесплатно)

Бренд: Yafho SiliSkin (RU) · Аудитория: пациенты + врачи · Звук: музыка + крупные титры-тезисы (без голоса)
Реализм: Kling (картинка → image-to-video, клипы 5 с) · Абстракция и инфографика: код (Remotion) · Финал: @sil.icare
Форматы: 9:16 (основной) → из тех же клипов 16:9, 4:5, Telegram

---

## 0. Паспорт продукта (единственный источник фактов)

- Что: пластина из медицинского силикона, мягкая, прозрачная, многоразовая, CE.
- Как работает: окклюзия → кожа удерживает влагу → сигнал фибробластам ↓ → меньше лишнего коллагена. Кислород проходит.
- Показания: гипертрофические и келоидные рубцы; после операций, кесарева, ожогов; стрии; после косметологических процедур.
- Старт: сразу после закрытия раны и снятия швов.
- Ношение: очистить, высушить, пластина на 1 см шире рубца со всех сторон, 12–23 ч/сут, промывать, чередовать две пластины.
- Результат: первые изменения — недели; заметно — 1–3 мес; ровнее — 3–6 мес регулярного ношения.
- Нельзя: открытая рана, корки, инфекция, аллергия на силикон. Дети, беременность — к врачу.
- Размеры: 4×4, 4×13, 5×15, 10×15 см (СВЕРИТЬ с упаковкой).

Главная мысль: **Силикон держит влагу в рубце — рубец становится мягче, площе, светлее.**

## 0.1 Цифры исследований (тема 08, вместо «Слова врача»)

| Титр на экране | Источник |
|---|---|
| «Силикон — первая линия, „золотой стандарт“ неинвазивной терапии рубцов» | Monstrey S. et al. Updated Scar Management Practical Guidelines. J Plast Reconstr Aesthet Surg, 2014 |
| «Гипертрофический рубец: у 39–68% после операций, 33–91% после ожогов» | Hsu K-C, Luan C-W, Tsai Y-W. Wounds 2017;29(5):154–158 |
| «Силиконовые пластины: риск патологического рубца ниже в ~2 раза (RR 0,41)» | там же, подгруппа silicone gel sheeting |

Правило: под каждой цифрой — мелкий титр источника. Не писать «уберёт рубец», «100%». Качество многих исследований низкое (Cochrane CD003826) — поэтому формулировки «снижает риск», «помогает».

---

## 1. Стиль (вставлять в каждый промпт Kling)

**STYLE:**
```
clean clinical aesthetic, soft natural window light, warm off-white background, accents of deep navy and burnt orange, calm trustworthy medical mood, photorealistic, high detail, shallow depth of field, hands and skin only, no faces, no text
```
**NEGATIVE (поле Negative в Kling):**
```
face, text, letters, logo, watermark, blood, open wound, fresh stitches, gore, pus, distorted hands, extra fingers, plastic skin, oversaturated, neon, cartoon, harsh shadows, cluttered background, needles
```
Правила:
- Одна модель рук во всех кадрах: «Central Asian woman’s hands, light olive skin, short natural nails, no jewelry».
- Рубцы — только зажившие, любой тяжести. Ран нет.
- Коробка — белая без надписей. Логотип Yafho накладывает Remotion.
- Композиция 9:16, главный объект в центральной трети (для 16:9 и 4:5 без потерь).
- Кредиты: сначала 2–3 картинки на кадр → выбрать лучшую → только её оживлять (5 с, Standard).

Цвета для кода: navy #0F2440 · оранжевый #D4560F · teal #0D9488 · off-white #FBFAF7 · беж #ECE6DD. Шрифт Onest, цифры JetBrains Mono.

---

## 2. ПИЛОТ — hero-ролик 50 с

R = Kling, C = код (Remotion). Файлы класть в `projects/yafho/assets/kling/` с этими именами.

| # | Время | Тип | Что в кадре | Титр |
|---|---|---|---|---|
| H01 | 0–5 | R | рука касается рубца на предплечье | Рубец остался. Плотный и заметный |
| H02 | 5–14 | C | кожа в разрезе: хаотичный коллаген | Под кожей — лишний коллаген |
| H03 | 14–22 | C | пластина ложится, влага, волокна выравниваются | Силикон держит влагу → сигнал ↓ |
| H04 | 22–27 | R | руки достают пластину из белой коробки | Yafho SiliSkin · медицинский силикон |
| H05 | 27–32 | R | очистить и высушить | 1 · Очистить |
| H06 | 32–37 | R | линейка, +1 см | 2 · +1 см за край |
| H07 | 37–41 | R | наклеить, разгладить | 3 · 12–23 ч в сутки |
| H08 | 41–46 | R | рубец светлеет (старт → финиш кадр) | Через месяцы — мягче, светлее |
| H09 | 46–50 | C | эндкард navy | @sil.icare |

### H01 — рубец
Image:
```
Close-up of a woman's forearm with a healed raised red hypertrophic linear scar, about 8 cm, her other hand's fingertips gently touching it, sitting by a window in a light room, Central Asian woman's hands, light olive skin, short natural nails, no jewelry, vertical 9:16, subject centered, [STYLE]
```
Motion:
```
fingertips slowly glide along the scar and lift away, subtle breathing movement, static camera, soft light flicker from window
```

### H04 — продукт
Image:
```
Hands opening a plain white matte box with no text, pulling out a translucent soft silicone gel sheet, the sheet bending softly, light table, macro detail of smooth matte silicone with a gentle reflection, vertical 9:16, centered, [STYLE]
```
Motion:
```
hands lift the silicone sheet out of the box, it bends and springs back, slow push-in camera
```

### H05 — очистить
Image:
```
Hands washing skin around a healed scar on the forearm under a gentle stream of water at a white bathroom sink, then patting dry with a white towel, vertical 9:16, [STYLE]
```
Motion:
```
water flows over the forearm, hand patting dry with towel, static camera
```

### H06 — +1 см
Image:
```
A small transparent ruler placed next to a healed scar on the forearm, a translucent silicone sheet held above it, the sheet clearly wider than the scar by about one centimeter on each side, top-down view, vertical 9:16, [STYLE]
```
Motion:
```
the silicone sheet lowers slowly over the scar, aligned with the ruler, static top-down camera
```
(Оранжевый контур «+1 см» рисует Remotion поверх.)

### H07 — наклеить
Image:
```
Fingers smoothing a translucent silicone sheet onto a healed forearm scar from center to edges, the sheet fully covering the scar with margin, macro, vertical 9:16, [STYLE]
```
Motion:
```
fingers press and smooth the sheet from center outward, the sheet settles flat with a soft sheen
```

### H08 — результат (Kling: Start frame + End frame)
Start image = H01 без руки:
```
Same forearm, healed raised red hypertrophic linear scar, no hands, top-down, vertical 9:16, [STYLE]
```
End image:
```
Same forearm, same position and light, the scar is now flat, pale pink-white and thin, vertical 9:16, [STYLE]
```
Motion:
```
the scar gradually flattens and fades over time, completely static camera, lighting unchanged
```
(Счётчик «2 нед → 1 мес → 3 мес → 6 мес» — Remotion.)

---

## 3. Отдельные темы (после пилота)

Каждая — ролик 10–20 с + картинка-пост. Реальные кадры (R) берутся из пилота или делаются по тем же шаблонам.

**01 Продукт** — 10 с. R: H04 + макро текстуры (нажатие пальцем, пластина пружинит). Титры: «Медицинский силикон · многоразовая · CE».

**02 Механизм** — 15–20 с, C полностью. Кожа в разрезе (эпидермис, дерма, волокна коллагена оранжевым) → пластина → плёнка влаги → пульсы сигналов замедляются → волокна выравниваются → поверхность ровная. Подписи: «влага ↑», «сигнал ↓», «коллаген».

**03 Показания** — карусель 4 + видео 12 с. R, 4 кадра:
```
Healed pink linear surgical scar on forearm, fingertips touching it, [STYLE]
Healed horizontal C-section scar on lower abdomen, high-waist underwear, hand resting nearby, [STYLE]
Healed burn scar on the back of a hand, other hand gently holding it, [STYLE]
Small raised keloid on the shoulder, fingertip pointing near it, [STYLE]
```
Motion для всех: `fingertips gently touch the scar and move away, static camera`. Титры: «После операций · Кесарево · Ожоги · Келоиды».

**04 Как наклеить** — 20 с. R: H05→H06→H07 + 2 кадра:
```
Forearm with a rolled-down shirt sleeve, person typing on a laptop, sheet invisible under sleeve, [STYLE]
Silicone sheet being rinsed with mild soap under tap, then laid on a clean white towel next to a second sheet, [STYLE]
```
Титры: «1 Очистить · 2 +1 см · 3 Наклеить · 4 12–23 ч · 5 Промыть, чередовать две».

**05 Результат** — 15 с. R: H08. C: линейный график «с силиконом» (оранжевая, вниз) vs «без» (серая пунктир), метки 7/14/21/28 дн. Титр: «Регулярность = результат · 3–6 мес».

**06 Подбор размера** — 8 с, C. Четыре пластины падают на силуэты зон: 4×4 → лицо/мелкий, 4×13 → рука, 5×15 → живот, 10×15 → ожог. Титры с размерами.

**07 Мифы и ошибки** — 15 с. R + красный/зелёный тинт в коде:
```
Silicone sheet on skin with a dark crust — WRONG frame, [STYLE]
Silicone sheet on fully healed pale scar with margin — RIGHT frame, [STYLE]
```
Пары: «✗ на корки → ✓ на закрытую кожу», «✗ пару часов → ✓ 12–23 ч», «✗ без мытья → ✓ промыть, две по очереди».

**08 Цифры исследований** — 12 с, C. Три стат-карточки из таблицы 0.1, под каждой — источник.

**09 CTA** — 4 с, C. Navy, вращающаяся пластина (кадр H04 крупно), логотип, @sil.icare, QR.

---

## 4. План

1. Пилот: H01, H04–H08 в Kling (≈ 6 картинок × 2–3 варианта + 6 клипов по 5 с). Код: H02, H03, H09. Сборка 9:16 → 16:9.
2. Оценить: читаются ли титры без звука, похожи ли руки между кадрами.
3. Темы 04, 02, 05 (самые полезные), затем 03, 06, 07, 08, 01.
4. Позже — облако/API: те же промпты, пакетная генерация.

## 5. Проверка перед публикацией
- Нет «уберёт рубец», «100%», «навсегда» — только «мягче, светлее, ровнее», «снижает риск».
- Нет ран, крови, лиц.
- Логотип и текст — только из кода.
- Источник под каждой цифрой.
- Размеры сверены с упаковкой.
