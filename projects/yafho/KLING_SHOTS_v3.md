# Yafho-Silicare — кадры Kling v3: что заменяет каждый клип

**Все ролики уже готовы без Kling**: каждый кадр нарисован кодом. Реальный клип — улучшение. Положите файл `assets/kling/<ID>.mp4`, пересоберите ролик, и клип сам встанет на место рисунка. Титры и стрелки остаются, для кадра «+1 см» (H06) поверх клипа появляется оранжевый контур.

Общие правила — стиль, negative, одна модель рук, композиция 9:16, кредиты — в `KLING_SHOTS_v2.md`, раздел 1. Здесь только сводка и промпты новых кадров.

## 1. Сводная таблица

| ID | Что в кадре | Заменяет рисунок в | Есть промпт |
|---|---|---|---|
| **H04** | руки достают пластину из белой коробки и опускают вниз | hero v4 V06 · тема 01 P1 | v2, §2 |
| **H05** | очистить и промокнуть кожу | hero v4 V09a · тема 04 T2 | v2, §2 |
| **H06** | пластина над рубцом, вид сверху (под контур «+1 см») | hero v4 V09b · тема 04 T3 | v2, §2 |
| **H07** | пальцы разглаживают пластину от центра | hero v4 V09c · тема 04 T4 | v2, §2 |
| **H09** | рукав опущен, человек печатает на ноутбуке — пластины не видно | тема 04 T5 · 11 D1 · 15 A4 | ниже, §2 |
| **H10** | пластину промывают под краном, вторая лежит на полотенце | тема 04 T6 · 11 D3 · 01 P3 | ниже, §2 |
| **H11** | пластина на полностью зажившем бледном рубце, с запасом по краям | тема 03 I7 · 12 N3 | ниже, §2 |
| **P01** | заживший рубец на предплечье после операции | тема 03 I2 · hero v4 карточка AUD_O | v2, §6 |
| **P02** | заживший шов после кесарева | тема 03 I3 · hero v4 карточка AUD_K | v2, §6 |
| **P03** | заживший ожог на тыльной стороне кисти | тема 03 I4 · hero v4 карточка AUD_B | v2, §6 |
| **P04** | небольшой келоид на плече | тема 03 I5 | ниже, §2 |
| **P05** | растяжки на боку живота / бедре | тема 03 I6 | ниже, §2 |

**Минимальный набор с наибольшей отдачей:** H04, H05, H06, H07. Они закрывают hero v4 и тему 04 — самые смотрибельные ролики.

**Что намеренно остаётся рисунком:**
- **Эффект «до → после»** (кожа сверху, сравнение, 3D) — с плашкой «схема». Сгенерированный «до/после» (H08) зритель может принять за фото пациента, поэтому в серии его нет. Если нужен H08, ставьте его только с подписью «иллюстрация».
- **Кадр «на корку»** (ТЗ, тема 07, WRONG frame). Правило «нет ран», поэтому ошибка показана только текстом.

## 2. Промпты новых кадров

Подставьте `[STYLE]` и Negative из `KLING_SHOTS_v2.md`, §1.1–1.2. Руки во всех кадрах одни и те же — используйте H05 или P01 как референс.

**H09 — «Под одеждой не видно»** (ТЗ, тема 04)
```
Forearm with a rolled-down light knit sleeve resting on a laptop keyboard, person typing, the silicone sheet invisible under the sleeve, Central Asian woman's hands, light olive skin, short natural nails, no jewelry, vertical 9:16, hands in the central third, no screen content visible, [STYLE]
```
Движение: `hands type calmly, sleeve stays down, static camera`

**H10 — «Промыть, чередовать две»** (ТЗ, тема 04)
```
Transparent silicone sheet being rinsed with mild soap under a gentle tap stream, a second identical sheet lying on a clean white towel nearby, Central Asian woman's hands, light olive skin, short natural nails, no jewelry, vertical 9:16, sheet in the central third, [STYLE]
```
Движение: `water runs over the sheet, fingers gently rub it, then lay it next to the second sheet, static camera`

**H11 — «Только на зажившую кожу»** (ТЗ, тема 07, RIGHT frame)
```
Transparent silicone sheet lying flat on a fully healed pale linear scar on the inner forearm, the sheet extends about 1 cm beyond the scar on every side, Central Asian woman's forearm, light olive skin, vertical 9:16, sheet in the central third, [STYLE]
```
Движение: `fingertip gently smooths the sheet edge once, static camera`

**P04 — келоид** (ТЗ, тема 03, кадр 4)
```
Small raised keloid scar on the shoulder, healed, fingertip pointing near it without touching, Central Asian woman, light olive skin, no face, vertical 9:16, scar in the central third, [STYLE]
```

**P05 — растяжки** (паспорт: показания — стрии)
```
Healed silvery-pink stretch marks on the side of the lower abdomen, fingertips gently touching them, Central Asian woman, light olive skin, high-waist light underwear, no face, vertical 9:16, marks in the central third, [STYLE]
```

Движение для P04, P05 (как P01–P03): `fingertips gently touch the scar and move away, static camera, soft window light`

## 3. Как поставить клипы

```bash
cp ~/Downloads/H05.mp4 projects/yafho/assets/kling/
bash projects/yafho/build_topics.sh 9x16,16x9,4x5 04            # тема 04 с реальным H05
python projects/yafho/build_v2.py --data projects/yafho/hero_v4.json --final   # hero v4
```

Если клип короче слота, сборка его замедлит. Если длиннее — обрежет. Можно класть по одному: каждый клип заменяет только свои сцены. `check_rules.py` перестаёт предупреждать о заглушках по мере появления файлов.
