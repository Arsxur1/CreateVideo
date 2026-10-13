"""Yafho-Silicare — topic 23 «Доверие: у вас есть план», see MARKETING.md.

    python projects/yafho/topics/series5.py      # writes topics/topic_23.json

Marketing arc (StoryBrand-style): the viewer's pain → «we hear your questions» → the brand
as a guide → how it works → proof with a source → why trust the product → a simple plan →
the result → an invitation to ask. Facts only from the passport (TZ §0) and TZ §0.1.
Titles ≤ 6 words. The 15 s ad cut is the `cuts.S` window set (make_cuts.py).
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from series_lib import acc, end_card, scene, seg, skin, title  # noqa: E402
from series_lib import write as _write  # noqa: E402

HSU = "Hsu K-C, Luan C-W, Tsai Y-W. Wounds 2017;29(5):154–158"
LOW = dict(areaTop=0.035, areaBottom=0.5)

# 15 s ad / story: pain → proof → result → invitation
AD = {"name": "Реклама 15 с", "windows": [["T1", 0, 3.5], ["T5", 0.4, 4], ["T8", 0, 3.5], ["T9", 0, 3.2]]}

_write("23", "Доверие: у вас есть план", [
    # 1 pain — the viewer's own scar, dense and visible
    scene("T1", 0, 3.5, "кожа сверху: плотный заметный шов", skin("csection", "idle", skinState="hyper"),
          [title("Шов зажил.\nА рубец — нет?", lead=0.1)]),
    # 2 empathy — the questions nobody answered
    {"id": "T2", "start": 3.5, "end": 7.5, "kind": "CHIPS", "shot": "вопросы пациента",
     "chips": {"title": "Знакомые вопросы?",
               "items": ["Это нормально?", "Что делать дома?", "Сколько носить?", "Когда станет лучше?"]},
     "titles": []},
    # 3 the guide
    scene("T3", 7.5, 10.5, "пластина ложится на рубец", skin("line", "idle", land=True),
          [title("Мы собрали ответы\nв один план")]),
    # 4 how it works (passport: окклюзия → влага → сигнал ↓ → меньше лишнего коллагена)
    {"id": "T4", "start": 10.5, "end": 16.5, "kind": "3D", "phase3d": "seal",
     "shot": "кожа в разрезе: пластина держит влагу, волокна ровнее",
     "titles": [title("Силикон\nдержит влагу", lead=0.1), title("Сигнал ↓ —\nколлаген ровнее", at=0.5)],
     "timeline": {"from": 0.42, "to": 0.6, "highlightWindow": True}},
    # 5 proof — one figure, with its source
    scene("T5", 16.5, 20.5, "сравнение через 6 мес + цифра",
          skin("csection", "compare", progressFrom=1, progressTo=1, **LOW),
          stat={"value": "≈ в 2 раза", "label": "ниже риск\nпатологического рубца", "source": f"{HSU} · RR 0,41",
                "position": "hero_low", "delay": 0.4}),
    # 6 why trust the product (passport: что)
    {"id": "T6", "start": 20.5, "end": 24, "kind": "CHIPS", "shot": "паспорт продукта",
     "chips": {"title": "Yafho-Silicare —\nэто:", "items": ["Медицинский силикон", "Мягкая и прозрачная", "Многоразовая", "CE"]},
     "titles": []},
    # 7 the plan
    scene("T7", 24, 30, "чек-лист плана (паспорт: старт, ношение)",
          {"type": "check_list", "title": "Ваш план:",
           "checkItems": [{"text": "Сразу после снятия швов"}, {"text": "+1 см за край рубца"},
                          {"text": "12–23 ч в сутки"}, {"text": "Промывать, чередовать две"}]}),
    # 8 the result
    scene("T8", 30, 33.5, "эффект под пластиной", skin("csection", "effect", months=6, skinFrom="hyper"),
          [title("Через 3–6 мес —\nмягче, ровнее")]),
    # 9 invitation — the brand answers
    end_card("T9", 33.5, 37.5, "Остались вопросы?\nНапишите нам"),
], {"bpm": 86, "segments": [seg(0, 7.5, "hold", "Am", "F", "Dm"), seg(7.5, 16.5, "resolve", "C", "G", "F"),
                            seg(16.5, 30, "lift", "F", "G", "C", "Am"), seg(30, 33.5, "lift", "F", "G"),
                            seg(33.5, 37.5, "end", "Cadd9")],
    "accents": [acc(0, "impact"), acc(3.5, "click"), acc(8.9, "land"), acc(10.5, "whoosh"), acc(16.9, "chime"),
                acc(20.5, "click"), acc(24, "click"), acc(30, "chime"), acc(33.5, "chime")]},
    cover_at=2.6, story=AD, plan="MARKETING.md")
