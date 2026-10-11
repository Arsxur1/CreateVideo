"""Yafho-Silicare — series 3 scene files (topics 18–21), see TOPICS_v3.md.

    python projects/yafho/topics/series3.py      # writes topics/topic_18.json … topic_21.json

Passport items series 1–2 left without their own video: keloid scars, scars after
cosmetic procedures, «oxygen passes» and the second TZ audience — doctors.
Facts come only from the product passport (TZ §0) and the study table (TZ §0.1). Titles ≤ 6 words.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from series_lib import acc, end_card, scene, seg, skin, title  # noqa: E402
from series_lib import write as _write  # noqa: E402

HSU = "Hsu K-C, Luan C-W, Tsai Y-W. Wounds 2017;29(5):154–158"
MONSTREY = "Monstrey S. et al. Updated Scar Management Practical Guidelines. J Plast Reconstr Aesthet Surg, 2014"

STORIES = {
    "18": {"name": "Два исхода", "windows": [["A1", 0, 4], ["A5", 0, 3], ["A6", 0, 2.6]]},
    "19": {"name": "Два исхода", "windows": [["A1", 0, 4], ["A5", 0, 3], ["A6", 0, 2.6]]},
    "20": {"name": "Кожа дышит?", "windows": [["B1", 0.3, 3.5], ["B2", 0.5, 3.5], ["B5", 0, 2.6]]},
    "21": {"name": "Врачу", "windows": [["V1", 0.3, 4], ["V4", 0.6, 4], ["V6", 0, 2.6]]},
}


def write(num: str, name: str, scenes: list[dict], score: dict, cover_at: float) -> None:
    _write(num, name, scenes, score, cover_at, STORIES[num], "TOPICS_v3.md")


# ---------------------------------------------------------------- 18–19 аудитории (шаблон тем 14–17)
# No sheet size in A2: the passport sizes are «сверить с упаковкой», and a small keloid or a
# post-procedure scar may need 4×4 or 4×13 — so the title says the rule, not the size.
AUD = [
    ("18", "Келоидный рубец", "keloid", "Келоидный рубец:\nдва исхода", "Только на\nзажившую кожу",
     "Через 3–6 мес —\nмягче, ровнее", "Отправьте тому,\nкому это нужно"),
    ("19", "После косметологии", "line", "Рубец после процедуры:\nдва исхода", "Когда кожа\nполностью закрылась",
     "Через 3–6 мес —\nмягче, ровнее", "Отправьте тому,\nкому это нужно"),
]
for num, name, shape, hook, when, effect, cta in AUD:
    write(num, name, [
        scene("A1", 0, 4, f"кожа сверху: {name.lower()}, без ухода / с силиконом, 0 → 6 мес",
              skin(shape, "compare", progressFrom=0, progressTo=1), [title(hook, lead=0.1)]),
        scene("A2", 4, 7, "контур +1 см со всех сторон", skin(shape, "measure"), [title("Пластина на 1 см\nшире рубца")]),
        scene("A3", 7, 10, "пластина ложится", skin(shape, "apply"), [title(when)]),
        scene("A4", 10, 15, "часы 0 → 23 ч, рукав (по 2,5 с на титр)", skin(shape, "wear"),
              [title("12–23 ч\nв сутки"), title("Под одеждой\nне видно", at=0.5)],
              **({"kling": "H09"} if shape == "line" else {})),
        scene("A5", 15, 18, "эффект под пластиной", skin(shape, "effect", months=6, skinFrom="hyper"), [title(effect)]),
        end_card("A6", 18, 21.5, cta),
    ], {"bpm": 88, "segments": [seg(0, 4, "impact", "Am", "F"), seg(4, 15, "light", "C", "G", "Am", "F"),
                                seg(15, 18, "lift", "F", "G"), seg(18, 21.5, "end", "Cadd9")],
        "accents": [acc(0, "impact"), acc(4, "click"), acc(7, "click"), acc(8.6, "land"), acc(10, "click"),
                    acc(12.9, "whoosh"), acc(15, "chime"), acc(18, "chime")]},
        cover_at=3.0)

# ---------------------------------------------------------------- 20 Кожа дышит?
# Passport: «окклюзия → кожа удерживает влагу → сигнал фибробластам ↓ … Кислород проходит.»
write("20", "Кожа дышит?", [
    scene("B1", 0, 3.5, "пластина ложится на рубец", skin("line", "idle", land=True),
          [title("Под пластиной\nкожа не дышит?", lead=0.1)]),
    scene("B2", 3.5, 7, "✗ миф → ✓ паспорт: кислород проходит",
          {"type": "myth_fact", "myth": "Кожа\nне дышит", "fact": "Кислород\nпроходит"}),
    {"id": "B3", "start": 7, "end": 12.5, "kind": "3D", "phase3d": "seal",
     "shot": "кожа в разрезе: пластина держит влагу, сигналы замедляются",
     "titles": [title("Влага остаётся\nв рубце", lead=0.1), title("Сигнал ↓ —\nколлаген ровнее", at=0.5)],
     "timeline": {"from": 0.42, "to": 0.6, "highlightWindow": True}},
    scene("B4", 12.5, 15.5, "эффект под пластиной", skin("line", "effect", months=6, skinFrom="hyper"),
          [title("Мягче, светлее,\nровнее")]),
    end_card("B5", 15.5, 19, "Отправьте тому,\nкто сомневается"),
], {"bpm": 88, "segments": [seg(0, 3.5, "impact", "Am", "F"), seg(3.5, 7, "hold", "Dm", "Am"),
                            seg(7, 12.5, "resolve", "C", "G", "F"), seg(12.5, 15.5, "lift", "F", "G"),
                            seg(15.5, 19, "end", "Cadd9")],
    "accents": [acc(0, "impact"), acc(1.4, "land"), acc(3.5, "click"), acc(5.2, "chime"), acc(7, "whoosh"),
                acc(12.5, "chime"), acc(15.5, "chime")]},
    cover_at=5.5)

# ---------------------------------------------------------------- 21 Врачу: памятка
# The second TZ audience. Same facts as the patient videos, in one 24 s memo with sources.
write("21", "Врачу: памятка", [
    {"id": "V1", "start": 0, "end": 4, "kind": "CHIPS", "shot": "показания (паспорт)",
     "chips": {"title": "Кому рекомендовать\nсиликон?",
               "items": ["Гипертрофический рубец", "Келоидный рубец", "После операций, кесарева", "После ожогов",
                         "Стрии", "После косметологии"]},
     "titles": []},
    scene("V2", 4, 8.5, "чек-лист ✓ (паспорт: старт, ношение)",
          {"type": "check_list", "title": "Схема:",
           "checkItems": [{"text": "Сразу после снятия швов"}, {"text": "+1 см за край рубца"},
                          {"text": "12–23 ч в сутки"}, {"text": "Промывать, чередовать две"}]}),
    scene("V3", 8.5, 12.5, "чек-лист ✗ / ! (паспорт: нельзя)",
          {"type": "check_list", "title": "Не применять:",
           "checkItems": [{"text": "Открытая рана, корки", "kind": "no"}, {"text": "Инфекция", "kind": "no"},
                          {"text": "Аллергия на силикон", "kind": "no"},
                          {"text": "Дети, беременность:\nпо решению врача", "kind": "info"}]}),
    scene("V4", 12.5, 16.5, "кожа сверху: сравнение через 6 мес",
          skin("csection", "compare", progressFrom=1, progressTo=1, areaTop=0.035, areaBottom=0.5),
          stat={"value": "≈ в 2 раза", "label": "ниже риск\nпатологического рубца", "source": f"{HSU} · RR 0,41",
                "position": "hero_low", "delay": 0.4}),
    scene("V5", 16.5, 20.5, "кожа сверху: пластина на рубце",
          skin("line", "effect", months=6, reveal=False, skinFrom="hyper", areaTop=0.035, areaBottom=0.5),
          stat={"value": "1-я линия", "label": "«золотой стандарт»\nнеинвазивной терапии рубцов", "source": MONSTREY,
                "position": "hero_low", "delay": 0.4}),
    end_card("V6", 20.5, 24, "Отправьте\nпациенту"),
], {"bpm": 88, "segments": [seg(0, 4, "light", "C", "G"), seg(4, 12.5, "light", "Am", "F", "C"),
                            seg(12.5, 20.5, "lift", "F", "G", "C"), seg(20.5, 24, "end", "Cadd9")],
    "accents": [acc(0, "chime"), acc(4, "click"), acc(8.5, "click"), acc(12.9, "chime"), acc(16.9, "chime"),
                acc(20.5, "chime")]},
    cover_at=14.5)
