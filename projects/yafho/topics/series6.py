"""Yafho-Silicare — series «Топ» (topics 24–27), see LISTICLES.md.

    python projects/yafho/topics/series6.py      # writes topics/topic_24.json … topic_27.json

Popular list formats: «5 фактов», «Почему нужна», «5 мифов», «Всегда убедитесь». Each item
is numbered on screen, so the viewer counts along and stays to the end. Facts only from the
passport (TZ §0) and TZ §0.1; every figure carries its source. Titles ≤ 6 words.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from series_lib import acc, end_card, scene, seg, skin, title  # noqa: E402
from series_lib import write as _write  # noqa: E402

HSU_SHORT = "Hsu K-C и др. Wounds 2017;29(5):154–158 · RR 0,41"


def write(num, name, scenes, score, cover_at, story):
    _write(num, name, scenes, score, cover_at, story, "LISTICLES.md")


def three_d(sid, start, end, phase, shot, titles, timeline):
    return {"id": sid, "start": start, "end": end, "kind": "3D", "phase3d": phase, "shot": shot,
            "titles": titles, "timeline": timeline}


def score(total, n_items, first, accent="click"):
    """Calm intro → steady list → lift on the effect → end chord; a click on every item."""
    end = total - 3.5
    return {"bpm": 90, "segments": [seg(0, first, "impact", "Am", "F"), seg(first, end - 3, "light", "C", "G", "Am", "F"),
                                    seg(end - 3, end, "lift", "F", "G"), seg(end, total, "end", "Cadd9")],
            "accents": [acc(0, "impact")] + [acc(t, accent) for t in n_items] + [acc(end - 3, "chime"), acc(end, "chime")]}


# ---------------------------------------------------------------- 24 · 5 фактов
write("24", "5 фактов о пластине", [
    scene("F0", 0, 3, "два исхода одного шва", skin("csection", "compare", progressFrom=0, progressTo=1),
          [title("5 фактов\nо пластине для рубца", lead=0.1)]),
    scene("F1", 3, 6.5, "пластина ложится на рубец", skin("line", "idle", land=True),
          [title("1 · Медицинский\nсиликон")]),
    three_d("F2", 6.5, 11, "seal", "кожа в разрезе: влага остаётся, сигналы реже",
            [title("2 · Держит влагу,\nкислород проходит", lead=0.1)], {"from": 0.45, "to": 0.6, "highlightWindow": True}),
    scene("F3", 11, 14.5, "сравнение через 6 мес", skin("csection", "compare", progressFrom=1, progressTo=1),
          [title("3 · Риск рубца\nниже вдвое", footnote=True)], footnote=HSU_SHORT),
    scene("F4", 14.5, 18, "промыть пластину, наклеить вторую", skin("line", "rinse"),
          [title("4 · Пластина\nмногоразовая")]),
    scene("F5", 18, 21.5, "эффект под пластиной", skin("line", "effect", months=6, skinFrom="hyper"),
          [title("5 · Заметно —\nчерез 1–3 месяца")]),
    end_card("F6", 21.5, 25, "Сохраните,\nчтобы не забыть"),
], score(25, [3, 6.5, 11, 14.5, 18], 3), cover_at=2.6,
    story={"name": "5 фактов", "windows": [["F0", 0, 3], ["F3", 0.3, 3.5], ["F6", 0, 2.6]]})

# ---------------------------------------------------------------- 25 · Почему нужна пластина
write("25", "Почему нужна пластина", [
    scene("P0", 0, 3.5, "плотный заметный шов", skin("csection", "idle", skinState="hyper"),
          [title("Шов зажил. Зачем\nещё пластина?", lead=0.1)]),
    three_d("P1", 3.5, 9, "alarm", "кожа в разрезе: кожа бьёт тревогу, лишний коллаген",
            [title("1 · Без ухода рубец\nуплотняется", lead=0.1)], {"from": 0.55, "to": 0.62}),
    scene("P2", 9, 13, "плотный рубец + цифра", skin("csection", "idle", skinState="hyper", areaTop=0.035, areaBottom=0.5),
          stat={"value": "39–68 %", "label": "гипертрофический рубец\nпосле операций",
                "source": "Hsu K-C, Luan C-W, Tsai Y-W. Wounds 2017;29(5):154–158", "position": "hero_low", "delay": 0.2}),
    scene("P3", 13, 16.5, "сравнение через 6 мес", skin("csection", "compare", progressFrom=1, progressTo=1),
          [title("2 · Риск рубца\nниже вдвое", footnote=True)], footnote=HSU_SHORT),
    scene("P4", 16.5, 20, "эффект под пластиной", skin("line", "effect", months=6, skinFrom="hyper"),
          [title("3 · Рубец мягче,\nсветлее, ровнее")]),
    scene("P5", 20, 25, "чек-лист плана (паспорт: старт, ношение)",
          {"type": "check_list", "title": "Это просто:",
           "checkItems": [{"text": "Сразу после снятия швов"}, {"text": "+1 см за край рубца"},
                          {"text": "12–23 ч в сутки"}]}),
    end_card("P6", 25, 28.5, "Отправьте тому,\nу кого свежий шов"),
], score(28.5, [3.5, 9, 13, 16.5, 20], 3.5), cover_at=3.0,
    story={"name": "Почему нужна", "windows": [["P0", 0, 3.5], ["P3", 0.3, 3.5], ["P6", 0, 2.6]]})

# ---------------------------------------------------------------- 26 · 5 мифов
MYTHS = [("Само\nпройдёт", "Первые месяцы\nрешают"),
         ("Кожа\nне дышит", "Кислород\nпроходит"),
         ("Пару часов\nхватит", "12–23 ч\nв сутки"),
         ("Можно\nна корку", "Только на\nзакрытую кожу"),
         ("Результат —\nза неделю", "Заметно —\n1–3 мес")]
sc = [scene("M0", 0, 3, "плотный рубец", skin("line", "idle", skinState="hyper"), [title("5 мифов\nо рубцах", lead=0.1)])]
t = 3.0
for i, (myth, fact) in enumerate(MYTHS):
    sc.append(scene(f"M{i + 1}", t, t + 3.5, f"✗ {myth} → ✓ {fact}".replace("\n", " "),
                    {"type": "myth_fact", "myth": myth, "fact": fact, "counter": f"{i + 1} / 5"}))
    t += 3.5
sc.append(scene("M6", t, t + 3, "эффект под пластиной", skin("line", "effect", months=6, skinFrom="hyper"),
                [title("Правильно —\nи рубец мягче")]))
t += 3
sc.append(end_card("M7", t, t + 3.5, "Сохраните\nи проверьте себя"))
write("26", "5 мифов о рубцах", sc, score(t + 3.5, [3 + 3.5 * i for i in range(5)], 3), cover_at=4.8,
      story={"name": "5 мифов", "windows": [["M0", 0, 3], ["M1", 0.3, 3.5], ["M7", 0, 2.6]]})

# ---------------------------------------------------------------- 27 · Всегда убедитесь
write("27", "Всегда убедитесь", [
    scene("U0", 0, 3, "рубец перед пластиной", skin("line", "idle"), [title("Перед пластиной\nвсегда убедитесь:", lead=0.1)]),
    scene("U1", 3, 6, "чек-лист старта (паспорт)",
          {"type": "check_list", "title": "1 · Можно начинать:",
           "checkItems": [{"text": "Рана закрылась"}, {"text": "Швы сняты"}]}),
    scene("U2", 6, 9, "очистить и высушить кожу", skin("line", "clean"), [title("2 · Кожа чистая\nи сухая")]),
    scene("U3", 9, 12, "контур +1 см", skin("line", "measure"), [title("3 · Шире рубца\nна 1 см")]),
    scene("U4", 12, 15, "пластина ложится", skin("line", "apply"), [title("4 · Наклеить\nи разгладить")]),
    scene("U5", 15, 19.5, "чек-лист «нельзя» (паспорт)",
          {"type": "check_list", "title": "5 · Не клейте, если:",
           "checkItems": [{"text": "Корки, инфекция", "kind": "no"}, {"text": "Аллергия на силикон", "kind": "no"},
                          {"text": "Дети, беременность:\nсначала к врачу", "kind": "info"}]}),
    scene("U6", 19.5, 22.5, "эффект под пластиной", skin("line", "effect", months=6, skinFrom="hyper"),
          [title("Тогда — мягче,\nсветлее, ровнее")]),
    end_card("U7", 22.5, 26, "Сохраните\nчек-лист"),
], score(26, [3, 6, 9, 12, 15], 3), cover_at=4.6,
    story={"name": "Всегда убедитесь", "windows": [["U0", 0, 3], ["U3", 0.3, 3], ["U7", 0, 2.6]]})
