# Yafho-Silicare — кадры Kling для hero v2 «Окно перестройки» и hero v3 «Один рубец — два исхода»

**Этап 4 из 5.** Реальные кадры генерирует заказчик вручную в Kling. Всё остальное — 3D, титры, стрелки, шкала, логотип и эндкард — делается кодом. Этот документ — техническое задание на 6 клипов: что снять, зачем этот кадр сюжету, как он стыкуется с 3D и как выбрать лучший дубль.

Куда класть готовые файлы: `projects/yafho/assets/kling/` с именами из таблицы (`H01.mp4`, `H04.mp4` …). При следующей сборке клип встаёт на место заглушки «нужен H0X» сам — ничего настраивать не нужно.

---

## 0. Сводная таблица

| Файл | Сцена | Акт | Слот в ролике | Что генерировать в Kling | Режим | Ключевое требование |
|---|---|---|---|---|---|---|
| `H01.mp4` | S01 | 1 · Крючок | 0:00–0:05 · **5 с** | рука касается рубца → наезд в макро | image → video, 5 с | **последние ~1,5 с — макро кожи** (для «ныряния» в 3D) |
| `H04.mp4` | S09 | 5 · Решение | 0:45–0:49 · **4 с** | руки достают пластину из белой коробки и **опускают её вниз** | image → video, 5 с | **в конце пластина движется вниз** (переход в 3D-пластину) |
| `H05.mp4` | S11a | 6 · Как | 0:55–0:58 · **3 с** | очистить и промокнуть кожу | image → video, 5 с | действие читается за 3 с |
| `H06.mp4` | S11b | 6 · Как | 0:58–1:01 · **3 с** | линейка и пластина над рубцом, вид сверху | image → video, 5 с | **статичная камера сверху**, рубец по центру (под контур «+1 см») |
| `H07.mp4` | S11c | 6 · Как | 1:01–1:05 · **4 с** | пальцы разглаживают пластину от центра к краям | image → video, 5 с | пластина целиком закрывает рубец с запасом |
| `H08.mp4` | S12 | 7 · Результат | 1:05–1:12,5 · **7,5 с** | рубец со временем бледнеет и уплощается | **start + end frame, 10 с** | **камера и свет неподвижны**, меняется только рубец |

Итого: 6 клипов. Используется около 26,5 с реального видео из 77,5 с ролика, остальное — 3D и графика.

---

## 1. Общие правила для всех кадров

### 1.1 Стиль — добавлять в конец **каждого** промпта картинки
```
clean clinical aesthetic, soft natural window light, warm off-white background, accents of deep navy and burnt orange, calm trustworthy medical mood, photorealistic, high detail, shallow depth of field, hands and skin only, no faces, no text
```

### 1.2 Negative — в поле Negative **каждой** генерации (и картинки, и видео)
```
face, text, letters, logo, watermark, blood, open wound, fresh stitches, gore, pus, distorted hands, extra fingers, plastic skin, oversaturated, neon, cartoon, harsh shadows, cluttered background, needles, jewelry, rings, nail polish, tattoo, camera shake, fast motion
```
К исходному NEGATIVE из ТЗ добавлены `jewelry, rings, nail polish, tattoo` — чтобы руки были одинаковыми во всех кадрах — и `camera shake, fast motion`, потому что ролик спокойный.

### 1.3 Одна и та же модель рук
Во всех промптах дословно:
```
Central Asian woman's hands, light olive skin, short natural nails, no jewelry
```
**Как добиться одинаковых рук между кадрами:**
1. Сначала сгенерируйте **H01** и выберите лучший кадр.
2. Для остальных кадров используйте его как **референс** (Image Reference / Elements / «по образцу» — в зависимости от версии Kling). Сила влияния референса — средняя: рука та же, композиция новая.
3. Держите одинаковое соотношение 9:16 и одно и то же предплечье (левое, рубец примерно посередине).

### 1.4 Рубец — один и тот же во всех кадрах
- Выпуклый гипертрофический **зажившие** рубец длиной около 8 см, вертикально вдоль внутренней стороны **левого предплечья**.
- Цвет — розово-красный, поверхность слегка блестящая. **Никаких** швов, корок и ран.
- В H08 финальный кадр — тот же рубец, но плоский, бледно-розовый, тонкий.

### 1.5 Композиция под три формата
- Генерировать в **9:16**.
- Главный объект (рубец, пластина, руки в действии) — в **центральной трети по вертикали**, то есть примерно между 30 % и 70 % высоты кадра. Тогда 4:5 вырезается из центра без потерь.
- Сверху ~20 % и снизу ~25 % кадра — спокойный фон. Там будут шкала и титры.

### 1.6 Технические параметры
| Параметр | Значение |
|---|---|
| Соотношение | 9:16 |
| Длительность | 5 с (H08 — 10 с, если доступно; если нет — 5 с, сборка замедлит) |
| Качество | Standard для проб → Professional/High для финального дубля выбранного кадра |
| Движение камеры | только то, что указано в промпте; по умолчанию статичная |
| Звук | не нужен (в ролике без голоса играет музыка) |
| Формат файла | mp4 (H.264), как отдаёт Kling. Перекодировать не нужно |

### 1.7 Экономия кредитов
1. На каждый кадр — **2–3 картинки** по промпту изображения.
2. Выбрать **одну** лучшую по чек-листу из раздела 3.
3. Оживлять **только её**: сначала Standard, финал — High.

---

## 2. Кадры

### H01 — «Рубец остался» (S01, 0:00–0:05)

**Роль в сюжете.** Первые 5 секунд решают, досмотрят ли ролик. Зритель узнаёт себя: рана давно зажила, а рубец остался. Титр поверх: «Рана зажила. А рубец остался.» Последние полторы секунды — медленный наезд в текстуру рубца. Из этого макро сборка делает «ныряние» в 3D-разрез кожи (сцена S02).

**Картинка (start frame):**
```
Close-up of a woman's left forearm resting on a light linen surface by a window, a healed raised pink-red hypertrophic linear scar about 8 cm long running vertically along the inner forearm, the fingertips of her other hand gently touching the scar, Central Asian woman's hands, light olive skin, short natural nails, no jewelry, vertical 9:16, scar in the central third of the frame, calm empty space above and below, [STYLE]
```

**Движение (motion prompt):**
```
the fingertips slowly glide along the scar and lift away, then the camera slowly pushes in toward the scar until its skin texture fills the frame, gentle and smooth, soft window light, no camera shake
```

**Обязательно:**
- в **последней 1–1,5 с** в кадре должно быть **макро кожи и рубца**, без пальцев и фона. Это стык с 3D;
- рука уходит из кадра до наезда.

**Если наезд не получается** (Kling иногда игнорирует движение камеры): сделайте обычный клип с касанием. Наезд и «ныряние» сборка сделает кодом — цифровым приближением последних кадров. Оно чуть мягче, но работает.

---

### H04 — «Решение» (S09, 0:45–0:49)

**Роль в сюжете.** Поворот истории: после 3D-«замирания» и титра «Этот — можно направить» впервые появляется продукт. Титр поверх: «Yafho-Silicare · медицинский силикон», логотип — кодом. Последнее движение — **пластина уходит вниз**. В следующем кадре (S10) 3D-пластина продолжает это же движение и ложится на кожу в разрезе. Это и есть переход по совпадению.

**Картинка:**
```
Hands holding a plain white matte box with no text, lid open, lifting out a translucent soft medical silicone gel sheet with rounded corners, the sheet gently bending, light linen table by a window, macro detail of the smooth matte silicone with a soft reflection, Central Asian woman's hands, light olive skin, short natural nails, no jewelry, vertical 9:16, sheet in the central third of the frame, [STYLE]
```

**Движение:**
```
the hands lift the silicone sheet out of the box, it bends softly and springs back, then the hands slowly lower the sheet downward out of the bottom of the frame, slow push-in camera, smooth motion
```

**Обязательно:**
- коробка **без надписей**: логотип добавляется кодом;
- в **последние ~0,7 с** пластина движется **вниз**;
- пластина полупрозрачная, матовая, со скруглёнными углами — как в 3D (там она светлая, почти бесцветная).

---

### H05 — «1 · Очистить» (S11a, 0:55–0:58)

**Роль в сюжете.** Первый из трёх быстрых шагов. На экране всего 3 секунды, поэтому действие должно читаться сразу. Титр: «1 · Очистить».

**Картинка:**
```
A forearm with a healed raised linear scar held under a gentle stream of water at a white bathroom sink, the other hand washing the skin around the scar, clean white towel nearby, Central Asian woman's hands, light olive skin, short natural nails, no jewelry, vertical 9:16, scar in the central third, [STYLE]
```

**Движение:**
```
water flows gently over the forearm, the hand rinses the skin, then pats it dry with the white towel, static camera, calm pace
```

**Обязательно:** главное действие — вода или полотенце — происходит в **первые 3 секунды** клипа. Сборка берёт начало клипа.

---

### H06 — «2 · +1 см за край» (S11b, 0:58–1:01)

**Роль в сюжете.** Правило размера. Поверх кадра код рисует оранжевый контур пластины и подписи «+1 см» слева и справа. Поэтому важны **неподвижная камера и рубец строго по центру**. Титр: «2 · +1 см за край».

**Картинка:**
```
Top-down view of a forearm on a light table, a healed raised linear scar running vertically in the exact center of the frame, a small transparent ruler placed alongside the scar, a translucent silicone gel sheet held just above the scar, clearly wider than the scar by about one centimeter on every side, Central Asian woman's hands, light olive skin, short natural nails, no jewelry, vertical 9:16, [STYLE]
```

**Движение:**
```
the silicone sheet lowers slowly and evenly over the scar, aligned with the ruler, completely static top-down camera
```

**Обязательно:**
- камера **сверху и неподвижна**;
- рубец — **вертикально по центру кадра**, около 30–35 % высоты кадра. Контур подстраивается под реальный рубец (параметр `scarBox` в сборке), но чем ближе к центру, тем меньше правки.

---

### H07 — «3 · 12–23 ч в сутки» (S11c, 1:01–1:05)

**Роль в сюжете.** Пластина на месте. Титр несёт главную инструкцию по ношению: «3 · 12–23 ч в сутки».

**Картинка:**
```
Fingers smoothing a translucent silicone gel sheet onto a healed forearm scar, pressing from the center toward the edges, the sheet fully covering the scar with a margin on every side, macro, Central Asian woman's hands, light olive skin, short natural nails, no jewelry, vertical 9:16, sheet in the central third, [STYLE]
```

**Движение:**
```
the fingers press and smooth the sheet from the center outward, the sheet settles flat with a soft sheen, the hand lifts away, static camera
```

**Обязательно:** в конце пластина лежит ровно, без пузырей. Рука уходит — кадр «отдыхает» под титр.

---

### H08 — «Мягче, светлее, ровнее» (S12, 1:05–1:12,5)

**Роль в сюжете.** Развязка. Поверх кадра курсор шкалы проходит отметки «2 нед → 1 мес → 3 мес → 6 мес». Синхронно с ним рубец на видео должен **постепенно** бледнеть и уплощаться. Титры: «Начать сразу после снятия швов» → «Мягче, светлее, ровнее» (с источником).

**Режим Kling: Start frame + End frame.** Длительность **10 с**, если доступно. Если только 5 с, сборка растянет клип на 7,5 с.

**Start image** (тот же рубец, что в H01, без рук):
```
The same left forearm resting on the same light linen surface by the window, healed raised pink-red hypertrophic linear scar about 8 cm long running vertically along the inner forearm, no hands touching, top-down view, vertical 9:16, scar in the central third, [STYLE]
```

**End image** (то же самое, но рубец «через полгода»):
```
The same left forearm, exactly the same position, framing and light, the scar is now flat, thin and pale pink-white, blending softly into the surrounding skin, top-down view, vertical 9:16, [STYLE]
```

**Движение:**
```
the scar gradually flattens and fades over time, completely static camera, lighting unchanged, no other changes in the frame
```

**Обязательно:**
- камера, рука, свет, фон — **неподвижны**. Меняется только рубец;
- изменение **плавное и равномерное** на всю длину клипа, без скачка в конце;
- финальный рубец — **заметен, но мягче**. Не «исчез». Это требование ТЗ: никаких обещаний «уберёт рубец».

**Как получить одинаковые start и end:** сначала сделайте start image. End image получите из него в режиме **image-to-image / «изменить»** с промптом end и силой изменения 0,3–0,45 — так поза и свет сохранятся.

---

## 3. Чек-лист выбора дубля

Перед тем как оживлять картинку и перед тем как класть готовый клип в папку:

- [ ] Нет лица, крови, ран, швов, корок, игл.
- [ ] Нет текста, букв, логотипов, водяных знаков — на коробке тоже.
- [ ] Пять пальцев на каждой руке, пальцы не «плавятся» в движении.
- [ ] Руки «те же»: оливковая кожа, короткие натуральные ногти, без украшений и лака.
- [ ] Рубец — вертикальный, на внутренней стороне левого предплечья, примерно по центру кадра.
- [ ] Свет мягкий, оконный. Нет пересветов и неоновых оттенков.
- [ ] Верх и низ кадра спокойные: туда встанут шкала и титры.
- [ ] H01: в конце макро кожи без пальцев.
- [ ] H04: в конце пластина движется вниз.
- [ ] H06: камера сверху и неподвижна.
- [ ] H08: меняется только рубец, финальный рубец бледный, но видимый.

---

## 4. Что происходит после того, как клипы на месте

1. Положить файлы в `projects/yafho/assets/kling/` (`H01.mp4`, `H04.mp4`, `H05.mp4`, `H06.mp4`, `H07.mp4`, `H08.mp4`).
2. Запустить сборку (раздел «Финальная сборка» в `projects/yafho/README.md`). Скрипт сам найдёт клипы и поставит их вместо заглушек.
3. Проверить контур «+1 см» на H06. Если он не совпал с рубцом, поправить `scarBox` в `hero_v2.json`, у сцены S11b.
4. Проверить стыки: H01 → 3D («ныряние») и H04 → 3D (пластина вниз).

Можно класть клипы по одному: каждый новый просто заменяет свою заглушку.

---

## 5. Дополнительные кадры для нарезок и постов (по желанию, после hero)

Для тем из раздела 3 ТЗ (показания, ошибки, подбор размера) пригодятся те же руки и тот же стиль. Промпты к ним уже есть в `TZ.md`, раздел 3. Генерировать их лучше после hero, используя H01 как референс рук.

---

## 6. Hero v3: дополнительные кадры аудиторий (P01–P03)

Hero v3 использует те же **H04–H07**, что и v2 (H01 и H08 в v3 не нужны: крючок и эффект сделаны 3D-сравнением). Для **нарезок по аудиториям** нужны ещё три коротких кадра. В нарезке на экране 3,5 с, поверх кадра — титр под аудиторию. Промпты взяты из ТЗ, раздел 3, тема 03 «Показания», с добавлением модели рук.

| Файл | Нарезка | Титр поверх |
|---|---|---|
| `P01.mp4` | O «После операции» | «Рубец после операции ещё формируется» |
| `P02.mp4` | K «После кесарева» | «Шов после кесарева меняется ещё месяцы» |
| `P03.mp4` | B «После ожога» | «Ожог зажил — рубец ещё растёт» |

**P01 — после операции**
```
Healed pink linear surgical scar on the inner forearm, fingertips gently touching it, Central Asian woman's hands, light olive skin, short natural nails, no jewelry, vertical 9:16, scar in the central third, [STYLE]
```

**P02 — после кесарева**
```
Healed horizontal C-section scar on the lower abdomen, high-waist light underwear, a hand resting gently nearby, no face, Central Asian woman, light olive skin, short natural nails, no jewelry, vertical 9:16, scar in the central third, [STYLE]
```

**P03 — после ожога**
```
Healed burn scar on the back of a hand, the other hand gently holding it, Central Asian woman's hands, light olive skin, short natural nails, no jewelry, vertical 9:16, scar in the central third, [STYLE]
```

**Движение для всех трёх:**
```
fingertips gently touch the scar and move away, static camera, soft window light
```

Чек-лист тот же (раздел 3). Для P02 дополнительно: бельё светлое и закрытое, кадр спокойный и деликатный — только живот и рука, без лица.
