"""Yafho-Silicare — topic 22 «Зачем пластина: наука простыми словами», see SCIENCE.md.

    python projects/yafho/topics/series4.py      # writes topics/topic_22.json

The patient's question «зачем пластина, если рана зажила, и насколько она помогает»
answered in one 60 s chain: how often scars grow → why (3D) → what silicone changes →
how much it helps (study table, TZ §0.1, every figure with its source) → when to expect
what → what to do at home. Facts only from the passport (TZ §0) and TZ §0.1. Titles ≤ 6 words.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from series_lib import acc, end_card, scene, seg, skin, title  # noqa: E402
from series_lib import write as _write  # noqa: E402

HSU = "Hsu K-C, Luan C-W, Tsai Y-W. Wounds 2017;29(5):154–158"
MONSTREY = "Monstrey S. et al. Updated Scar Management Practical Guidelines. J Plast Reconstr Aesthet Surg, 2014"
LOW = dict(areaTop=0.035, areaBottom=0.5)  # skin card above a hero stat badge

STORY = {"name": "Зачем пластина", "windows": [["W1", 0.3, 4], ["W6", 0.5, 4.5], ["W8", 0.6, 4], ["W12", 0, 2.6]]}


def three_d(sid: str, start: float, end: float, phase: str, shot: str, titles: list[dict], timeline: dict) -> dict:
    return {"id": sid, "start": start, "end": end, "kind": "3D", "phase3d": phase, "shot": shot,
            "titles": titles, "timeline": timeline}


_write("22", "Зачем пластина: наука простыми словами", [
    # hook — the patient's own question over the two outcomes
    scene("W1", 0, 4, "кожа сверху: шов без ухода / с силиконом, 0 → 6 мес",
          skin("csection", "compare", progressFrom=0, progressTo=1), [title("Рана зажила.\nЗачем пластина?", lead=0.1)]),
    # how often — study table (TZ §0.1)
    scene("W2", 4, 8, "кожа сверху: плотный рубец + цифра", skin("csection", "idle", skinState="hyper", **LOW),
          stat={"value": "39–68 %", "label": "гипертрофический рубец\nпосле операций", "source": HSU,
                "position": "hero_low", "delay": 0.2}),
    scene("W3", 8, 12, "кожа сверху: рубец после ожога + цифра", skin("burn", "idle", skinState="hyper", **LOW),
          stat={"value": "33–91 %", "label": "гипертрофический рубец\nпосле ожогов", "source": HSU,
                "position": "hero_low", "delay": 0.2}),
    # why — passport: окклюзия → влага → сигнал фибробластам ↓ → меньше лишнего коллагена
    three_d("W4", 12, 18, "drying", "кожа в разрезе: молодой рубец теряет влагу",
            [title("1 · Рубец\nтеряет влагу", lead=0.1)], {"from": 0.45, "to": 0.55}),
    three_d("W5", 18, 24.5, "alarm", "кожа в разрезе: сигналы тревоги, лишний коллаген",
            [title("2 · Кожа\nбьёт тревогу"), title("3 · Лишний коллаген —\nплотный рубец", at=0.5)],
            {"from": 0.55, "to": 0.62}),
    # what silicone changes
    three_d("W6", 24.5, 31, "seal", "кожа в разрезе: пластина держит влагу, сигналы реже, волокна ровнее",
            [title("Силикон\nдержит влагу", lead=0.1), title("Сигнал ↓ —\nколлаген ровнее", at=0.5)],
            {"from": 0.42, "to": 0.6, "highlightWindow": True}),
    scene("W7", 31, 34, "пластина ложится на рубец", skin("line", "idle", land=True),
          [title("Кислород проходит,\nвлага остаётся")]),
    # how much — study table, each figure with its source
    scene("W8", 34, 38.5, "сравнение через 6 мес + цифра",
          skin("csection", "compare", progressFrom=1, progressTo=1, **LOW),
          stat={"value": "≈ в 2 раза", "label": "ниже риск\nпатологического рубца", "source": f"{HSU} · RR 0,41",
                "position": "hero_low", "delay": 0.4}),
    scene("W9", 38.5, 43, "эффект под пластиной + цифра",
          skin("line", "effect", months=6, reveal=False, skinFrom="hyper", **LOW),
          stat={"value": "1-я линия", "label": "«золотой стандарт»\nнеинвазивной терапии рубцов", "source": MONSTREY,
                "position": "hero_low", "delay": 0.4}),
    # when — passport: недели → 1–3 мес → 3–6 мес
    scene("W10", 43, 49, "схема по срокам из инструкции", {"type": "result_curve", "months": 6},
          [title("Что и когда\nвы увидите")]),
    # what to do at home — the care details patients ask for
    scene("W11", 49, 55, "чек-лист ухода (паспорт: ношение)",
          {"type": "check_list", "title": "Уход дома:",
           "checkItems": [{"text": "Очистить и высушить кожу"}, {"text": "+1 см за край рубца"},
                          {"text": "12–23 ч в сутки"}, {"text": "Промывать, чередовать две"}]}),
    end_card("W12", 55, 58.5, "Сохраните\nпамятку ухода"),
], {"bpm": 88, "segments": [seg(0, 4, "impact", "Am", "F"), seg(4, 12, "hold", "Dm", "Am"),
                            seg(12, 24.5, "hold", "Am", "F", "Dm", "Am"), seg(24.5, 34, "resolve", "C", "G", "F"),
                            seg(34, 43, "lift", "F", "G", "C"), seg(43, 55, "light", "C", "G", "Am", "F"),
                            seg(55, 58.5, "end", "Cadd9")],
    "accents": [acc(0, "impact"), acc(4.2, "click"), acc(8.2, "click"), acc(12, "whoosh"), acc(18, "click"),
                acc(21.2, "click"), acc(24.5, "chime"), acc(31.4, "land"), acc(34.4, "chime"), acc(38.9, "chime"),
                acc(43, "click"), acc(49, "click"), acc(55, "chime")]},
    cover_at=36.5, story=STORY, plan="SCIENCE.md")
