"""Yafho-Silicare — series 2 scene files (topics 10–17), see TOPICS_v2.md.

    python projects/yafho/topics/series2.py      # writes topics/topic_10.json … topic_17.json

Facts come only from the product passport (TZ §0). Titles ≤ 6 words.
"""

from __future__ import annotations

import copy
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
FORMATS = {
    "9x16": {"profile": "instagram_reels", "layout": "full"},
    "16x9": {"profile": "youtube_landscape", "layout": "split",
             "cut_overrides": {"skin_demo": {"areaTop": 0.035, "areaBottom": 0.965},
                               "result_curve": {"areaTop": 0.035, "areaBottom": 0.965}}},
    "4x5": {"profile": "instagram_portrait", "layout": "full", "cut3d": {"centerY": 0.42, "fitFrac": 0.9}},
}


def skin(shape: str, step: str, **kw) -> dict:
    return {"type": "skin_demo", "skinShape": shape, "skinStep": step, **kw}


def scene(sid: str, start: float, end: float, shot: str, cut: dict | None = None, titles=(), **kw) -> dict:
    s = {"id": sid, "start": start, "end": end, "kind": "CUT" if cut else "C", "shot": shot, "titles": list(titles)}
    if cut:
        s["cut"] = cut
    s.update(kw)
    return s


def title(text: str, at: float = 0, lead: float = 0, **kw) -> dict:
    return {"text": text, "at": at, "lead": lead, **kw}


def end_card(sid: str, start: float, end: float, cta: str) -> dict:
    return scene(sid, start, end, "эндкард", cta=cta)


# 6–10 s stories (9:16) cut from the rendered video by make_cuts.py: hook + effect + end card
STORIES = {
    "10": {"name": "Швы сняли", "windows": [["S1", 0, 3], ["S2", 1.5, 5], ["S5", 0, 2.6]]},
    "11": {"name": "12–23 ч реально", "windows": [["D1", 0, 3.5], ["D2", 7.5, 10], ["D5", 0, 2.6]]},
    "12": {"name": "Не клейте, если", "windows": [["N1", 0.3, 4.8], ["N4", 0, 2.6]]},
    "13": {"name": "Видно под одеждой?", "windows": [["Q1", 0.3, 3.5], ["Q6", 0, 2.6]]},
}
for _n in ("14", "15", "16", "17"):
    STORIES[_n] = {"name": "Два исхода", "windows": [["A1", 0, 4], ["A5", 0, 3], ["A6", 0, 2.6]]}


def write(num: str, name: str, scenes: list[dict], score: dict, cover_at: float) -> None:
    d = {
        "title": f"Yafho-Silicare — тема {num} «{name}»",
        "plan": f"projects/yafho/TOPICS_v2.md#{num}",
        "brand": "Yafho-Silicare",
        "output_dir": "output/yafho/topics",
        "public_dir": "yafho-topics",
        "duration": scenes[-1]["end"],
        "backdrop": "linen",
        "cover_at": cover_at,
        "audio": "no voice — titles + arrows + music",
        "music": {"file": f"yafho_topic_{num}.wav", "volume": 1.0, "fadeInSeconds": 0.05, "fadeOutSeconds": 1.5},
        "scenes": scenes,
        "score": score,
        "formats": copy.deepcopy(FORMATS),
        "cut_prefix": f"topic_{num}_story",
        "cuts": {"S": STORIES[num]},
    }
    (HERE / f"topic_{num}.json").write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"topic_{num}.json · {d['duration']} s · «{name}»")


def seg(start, end, mood, *chords):
    return {"start": start, "end": end, "mood": mood, "chords": list(chords)}


def acc(t, kind):
    return {"t": t, "kind": kind}


# ---------------------------------------------------------------- 10 Когда начинать
write("10", "Когда начинать", [
    scene("S1", 0, 3, "кожа сверху: шов после кесарева без ухода / с силиконом, 0 → 6 мес",
          skin("csection", "compare", progressFrom=0, progressTo=1), [title("Швы сняли.\nЧто дальше?", lead=0.1)]),
    scene("S2", 3, 8, "чек-лист ✓ (паспорт: старт)",
          {"type": "check_list", "title": "Можно начинать, если:",
           "checkItems": [{"text": "Рана закрылась"}, {"text": "Швы сняты"}, {"text": "Нет корок"}, {"text": "Нет воспаления"}]}),
    scene("S3", 8, 11, "чек-лист ✗ / ! (паспорт: нельзя)",
          {"type": "check_list", "title": "Подождите, если:",
           "checkItems": [{"text": "Рана открыта", "kind": "no"}, {"text": "Есть корки", "kind": "no"},
                          {"text": "Дети, беременность:\nсначала к врачу", "kind": "info"}]}),
    scene("S4", 11, 15, "эффект под пластиной",
          skin("csection", "effect", months=6, skinFrom="hyper"), [title("Первые месяцы —\nглавные")]),
    end_card("S5", 15, 18.5, "Начните, пока\nрубец молодой"),
], {"bpm": 88, "segments": [seg(0, 3, "impact", "Am", "F"), seg(3, 11, "light", "C", "G", "Am"),
                            seg(11, 15, "lift", "F", "G"), seg(15, 18.5, "end", "Cadd9")],
    "accents": [acc(0, "impact"), acc(3, "click"), acc(8, "click"), acc(11, "chime"), acc(15, "chime")]},
    cover_at=2.4)

# ---------------------------------------------------------------- 11 День с пластиной
write("11", "День с пластиной", [
    scene("D1", 0, 3.5, "часы 0 → 23 ч, рукав закрывает пластину",
          skin("line", "wear"), [title("12–23 ч в сутки —\nэто реально", lead=0.1)], kling="H09"),
    scene("D2", 3.5, 13.5, "сутки по кругу: две пластины по очереди (вывод из паспорта)",
          {"type": "day_clock"}),
    scene("D3", 13.5, 16.5, "промыть A, наклеить B",
          skin("line", "rinse"), [title("Две пластины —\nбез перерыва")], kling="H10"),
    scene("D4", 16.5, 19.5, "эффект под пластиной (ТЗ: регулярность = результат)",
          skin("line", "effect", months=6, skinFrom="hyper"), [title("Регулярность =\nрезультат")]),
    end_card("D5", 19.5, 23, "Сохраните\nсвой распорядок"),
], {"bpm": 88, "segments": [seg(0, 3.5, "lift", "F", "G"), seg(3.5, 13.5, "light", "C", "G", "Am", "F"),
                            seg(13.5, 16.5, "resolve", "C", "G"), seg(16.5, 19.5, "lift", "F", "G"),
                            seg(19.5, 23, "end", "Cadd9")],
    "accents": [acc(0, "chime"), acc(2.2, "whoosh"), acc(4.2, "click"), acc(9.0, "click"), acc(13.5, "click"),
                acc(16.5, "chime"), acc(19.5, "chime")]},
    cover_at=11.5)

# ---------------------------------------------------------------- 12 Когда нельзя
write("12", "Когда нельзя", [
    scene("N1", 0, 6, "чек-лист ✗ (паспорт: нельзя)",
          {"type": "check_list", "title": "Не клейте, если:",
           "checkItems": [{"text": "Открытая рана", "kind": "no"}, {"text": "Корки", "kind": "no"},
                          {"text": "Инфекция", "kind": "no"}, {"text": "Аллергия на силикон", "kind": "no"}]}),
    scene("N2", 6, 9, "чек-лист ! (паспорт: дети, беременность — к врачу)",
          {"type": "check_list", "title": "Сначала к врачу:",
           "checkItems": [{"text": "Ребёнок", "kind": "info"}, {"text": "Беременность", "kind": "info"}]}),
    scene("N3", 9, 12, "пластина ложится на заживший рубец, рубец смягчается",
          skin("line", "idle", land=True, soften=True), [title("Только на\nзажившую кожу")], kling="H11"),
    end_card("N4", 12, 15.5, "Отправьте тому,\nкому это важно"),
], {"bpm": 88, "segments": [seg(0, 9, "hold", "Dm", "Am", "F"), seg(9, 12, "resolve", "C", "G"),
                            seg(12, 15.5, "end", "Cadd9")],
    "accents": [acc(0, "click"), acc(6, "click"), acc(10.2, "land"), acc(12, "chime")]},
    cover_at=3.2)

# ---------------------------------------------------------------- 13 Вопрос-ответ
qa = [("Видно\nпод одеждой?", "Нет: мягкая\nи прозрачная"),
      ("Сколько носить?", "12–23 ч\nв сутки"),
      ("Можно мыть?", "Да: промыть,\nчередовать две"),
      ("Когда результат?", "Заметно — 1–3 мес,\nровнее — 3–6 мес")]
sc = []
t = 0.0
for i, (q, a) in enumerate(qa):
    sc.append(scene(f"Q{i + 1}", t, t + 3.5, f"? {q} → {a}".replace("\n", " "),
                    {"type": "myth_fact", "mythVariant": "qa", "myth": q, "fact": a, "counter": f"{i + 1} / 4"}))
    t += 3.5
sc.append(scene("Q5", t, t + 3, "эффект под пластиной", skin("line", "effect", months=6, skinFrom="hyper"),
                [title("Мягче, светлее,\nровнее")]))
t += 3
sc.append(end_card("Q6", t, t + 3.5, "Сохраните\nответы"))
write("13", "Вопрос-ответ", sc, {"bpm": 88, "segments": [seg(0, 14, "light", "C", "G", "Am", "F"), seg(14, 17, "lift", "F", "G"),
                                                         seg(17, 20.5, "end", "Cadd9")],
    "accents": [acc(i * 3.5 + 1.0, "click") for i in range(4)] + [acc(14, "chime"), acc(17, "chime")]},
    cover_at=2.8)

# ---------------------------------------------------------------- 14–17 аудитории
AUD = [
    ("14", "После кесарева", "csection", "Шов после кесарева:\nдва исхода", "5×15", "Сразу после\nснятия швов",
     "Через 3–6 мес —\nмягче, ровнее", "Отправьте той,\nкому это нужно"),
    ("15", "После операции", "line", "Рубец после операции:\nдва исхода", "4×13", "Сразу после\nснятия швов",
     "Через 3–6 мес —\nмягче, ровнее", "Отправьте тому,\nкому это нужно"),
    ("16", "После ожога", "burn", "Рубец после ожога:\nдва исхода", "10×15", "Когда кожа\nполностью закрылась",
     "Через 3–6 мес —\nмягче, ровнее", "Отправьте тому,\nкому это нужно"),
    ("17", "Растяжки", "stria", "Растяжки:\nдва исхода", "10×15", "На чистую\nсухую кожу",
     "Через 3–6 мес —\nсветлее, ровнее", "Отправьте той,\nкому это нужно"),
]
for num, name, shape, hook, size, when, effect, cta in AUD:
    write(num, name, [
        scene("A1", 0, 4, f"кожа сверху: {name.lower()}, без ухода / с силиконом, 0 → 6 мес",
              skin(shape, "compare", progressFrom=0, progressTo=1), [title(hook, lead=0.1)]),
        scene("A2", 4, 7, f"контур +1 см, пластина {size} (сверить с упаковкой)",
              skin(shape, "measure"), [title(f"Пластина {size} —\n+1 см за край")]),
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
