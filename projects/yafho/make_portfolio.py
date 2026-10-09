"""Yafho-Silicare — portfolio page (one HTML page with every 9:16 video, stories, carousels, plan).

    python projects/yafho/make_portfolio.py      # → output/yafho/portfolio/index.html + media/

Web copies: 720×1280 H.264 (CRF 27) so the whole page stays light enough to share;
posters are JPEG frames at each topic's `cover_at`. Rebuild after re-rendering.
"""

from __future__ import annotations

import html
import json
import subprocess
from pathlib import Path

PROJECT = Path(__file__).resolve().parent
ROOT = PROJECT.parent.parent
SRC = ROOT / "output" / "yafho"
OUT = SRC / "portfolio"
MEDIA = OUT / "media"

# purpose / audience lines (from TOPICS_v1.md, TOPICS_v2.md)
ABOUT = {
    "01": ("Продукт", "мягкий медицинский силикон, прозрачная, многоразовая · CE"),
    "02": ("Все, у кого «рана зажила, а рубец растёт»", "почему рубец уплотняется и где помогает силикон"),
    "03": ("Самый широкий охват", "пять ситуаций — каждый находит свой рубец"),
    "04": ("Кто купил или выбирает", "5 шагов, от которых зависит результат"),
    "05": ("Кто бросил через неделю", "честные сроки: недели → 1–3 мес → 3–6 мес"),
    "06": ("Выбор размера", "рубец + 1 см со всех сторон, 4 размера"),
    "07": ("Кто «пробовал, не помогло»", "3 ошибки — и как правильно"),
    "08": ("Сомневающиеся", "цифры исследований, под каждой — источник"),
    "09": ("Закреп, концовка сторис", "QR и @sil.icare"),
    "10": ("У кого только что сняли швы", "чек-лист «можно начинать / подождите»"),
    "11": ("Кто боится, что 12–23 ч — неудобно", "распорядок суток: две пластины по очереди"),
    "12": ("Доверие", "противопоказания из паспорта продукта"),
    "13": ("Кто выбирает", "4 частых вопроса — ответы из паспорта"),
    "14": ("Таргет: мамы", "шов после кесарева, пластина 5×15"),
    "15": ("Таргет: после операции", "рубец на руке, пластина 4×13"),
    "16": ("Таргет: после ожога", "пластина 10×15"),
    "17": ("Таргет: растяжки", "пластина 10×15"),
}
SERIES = [("Серия 1 · темы ТЗ", ["04", "02", "05", "03", "06", "07", "08", "01"]),
          ("Серия 2 · практика и аудитории", ["10", "11", "12", "13", "14", "15", "16", "17"])]
CAROUSELS = ["04", "03", "07", "13", "08", "10", "11", "12", "06"]


def run(*cmd: str) -> None:
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *cmd], check=True)


def seconds(p: Path) -> float:
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)],
                       capture_output=True, text=True, check=True)
    return float(r.stdout.strip())


def web_copy(src: Path, name: str, poster_at: float) -> tuple[str, str, float]:
    mp4 = MEDIA / f"{name}.mp4"
    jpg = MEDIA / f"{name}.jpg"
    if not mp4.exists() or mp4.stat().st_mtime < src.stat().st_mtime:
        run("-i", str(src), "-vf", "scale=720:-2", "-c:v", "libx264", "-crf", "27", "-preset", "medium",
            "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "96k", "-movflags", "+faststart", str(mp4))
        run("-ss", f"{poster_at:.2f}", "-i", str(src), "-frames:v", "1", "-vf", "scale=540:-2", "-q:v", "4", str(jpg))
    return f"media/{mp4.name}", f"media/{jpg.name}", seconds(src)


def first_title(data: dict) -> str:
    for s in data["scenes"]:
        if s.get("titles"):
            return s["titles"][0]["text"].replace("\n", " ")
        if s.get("chips"):
            return s["chips"]["title"].replace("\n", " ")
        if s.get("cut", {}).get("title"):
            return s["cut"]["title"]
        if s.get("stat"):
            return f"{s['stat']['value']} — {s['stat']['label']}".replace("\n", " ")
        if s.get("cut", {}).get("myth"):
            return s["cut"]["myth"].replace("\n", " ")
    return ""


def card(num: str, data: dict, src: str, poster: str, dur: float, story: str | None) -> str:
    name = data["title"].split("«")[-1].rstrip("»")
    who, what = ABOUT.get(num, ("", ""))
    hook = first_title(data)
    st = f'<a class="story" href="{story}" target="_blank" rel="noopener">Сторис</a>' if story else ""
    return f"""
      <article class="clip" id="t{num}">
        <video controls preload="none" playsinline poster="{poster}" src="{src}" aria-label="{html.escape(name)}"></video>
        <div class="meta">
          <div class="row"><span class="num">{num}</span><span class="len">{dur:.0f} с</span>{st}</div>
          <h3>{html.escape(name)}</h3>
          <p class="hook">«{html.escape(hook)}»</p>
          <p class="what">{html.escape(what)}</p>
          <p class="who">{html.escape(who)}</p>
        </div>
      </article>"""


def main() -> None:
    MEDIA.mkdir(parents=True, exist_ok=True)
    sections = []

    hero = SRC / "v4" / "hero_v4_9x16.mp4"
    if not hero.exists():
        hero = SRC / "v3" / "hero_v3_9x16.mp4"
    hsrc, hposter, hdur = web_copy(hero, "hero", 2.0)

    for title, nums in SERIES:
        cards = []
        for n in nums:
            data = json.loads((PROJECT / "topics" / f"topic_{n}.json").read_text(encoding="utf-8"))
            src = SRC / "topics" / f"topic_{n}_9x16.mp4"
            if not src.exists():
                continue
            v, p, d = web_copy(src, f"topic_{n}", float(data.get("cover_at", 2.0)))
            story = SRC / "topics" / f"topic_{n}_story_S_9x16.mp4"
            s = web_copy(story, f"story_{n}", 1.0)[0] if story.exists() else None
            cards.append(card(n, data, v, p, d, s))
        sections.append(f'<section class="series"><h2>{title}</h2><div class="grid">{"".join(cards)}</div></section>')

    car = []
    for n in CAROUSELS:
        prev = SRC / "carousels" / f"topic_{n}" / "preview.png"
        if prev.exists():
            jpg = MEDIA / f"carousel_{n}.jpg"
            run("-i", str(prev), "-q:v", "4", str(jpg))
            slides = len(list(prev.parent.glob("slide_*.png")))
            name = json.loads((PROJECT / "topics" / f"topic_{n}.json").read_text(encoding="utf-8"))["title"].split("«")[-1].rstrip("»")
            car.append(f'<figure class="car"><div class="strip"><img src="media/{jpg.name}" alt="Карусель «{html.escape(name)}», {slides} слайдов" loading="lazy"></div>'
                       f'<figcaption>{n} · {html.escape(name)} · {slides} слайдов</figcaption></figure>')

    page = TEMPLATE.replace("{{HERO_SRC}}", hsrc).replace("{{HERO_POSTER}}", hposter).replace("{{HERO_LEN}}", f"{hdur:.0f}")
    page = page.replace("{{SERIES}}", "\n".join(sections)).replace("{{CAROUSELS}}", "\n".join(car))
    page = page.replace("{{HERO_NAME}}", "hero v4" if "v4" in str(hero) else "hero v3")
    (OUT / "index.html").write_text(page, encoding="utf-8")
    size = sum(p.stat().st_size for p in MEDIA.iterdir()) / 1e6
    print(f"{(OUT / 'index.html').relative_to(ROOT)} · media {len(list(MEDIA.iterdir()))} files · {size:.0f} MB")


TEMPLATE = """<title>Портфель Yafho-Silicare</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Onest:wght@400;500;700;800&family=JetBrains+Mono:wght@500;700&display=swap">
<style>
/* Layout: brand sheet — navy masthead with the hero reel, then series grids of 9:16 clips, carousels, plan. */
:root {
  --bg: #FBFAF7; --surface: #FFFFFF; --sunk: #ECE6DD; --ink: #0F2440; --muted: #5B6472;
  --accent: #B04408; --accent-line: #D4560F; --teal: #0A7067; --line: #DDD4C8;
  --mast: #0F2440; --mast-ink: #FFFFFF; --mast-muted: #C9D2DE;
  --display: "Onest", system-ui, sans-serif; --body: "Onest", system-ui, sans-serif; --mono: "JetBrains Mono", ui-monospace, monospace;
}
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) {
  --bg: #0B1626; --surface: #13223A; --sunk: #0F1C30; --ink: #EEF1F5; --muted: #A7B2C2;
  --accent: #F08A4B; --accent-line: #E0703A; --teal: #4CC3B5; --line: #24364F;
  --mast: #081120; --mast-ink: #FFFFFF; --mast-muted: #A7B2C2; color-scheme: dark } }
:root[data-theme="dark"] {
  --bg: #0B1626; --surface: #13223A; --sunk: #0F1C30; --ink: #EEF1F5; --muted: #A7B2C2;
  --accent: #F08A4B; --accent-line: #E0703A; --teal: #4CC3B5; --line: #24364F;
  --mast: #081120; --mast-ink: #FFFFFF; --mast-muted: #A7B2C2; color-scheme: dark }
* { box-sizing: border-box }
body { background: var(--bg); color: var(--ink); font-family: var(--body); font-size: 16px; line-height: 1.5; margin: 0 }
.wrap { max-width: 1180px; margin: 0 auto; padding-inline: 20px }
header.mast { background: var(--mast); color: var(--mast-ink) }
.mast .wrap { display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 300px); gap: 40px; padding-block: 44px; align-items: center }
.brand { font-family: var(--display); font-size: 20px; letter-spacing: .01em }
.brand b { font-weight: 800 } .brand span { font-weight: 500 }
.mast h1 { font-family: var(--display); font-weight: 800; font-size: clamp(30px, 5vw, 52px); line-height: 1.08; margin: 18px 0 14px; text-wrap: balance }
.mast p { color: var(--mast-muted); max-width: 60ch; margin: 0 0 10px }
.facts { display: flex; flex-wrap: wrap; gap: 10px; margin-top: 18px; padding: 0; list-style: none }
.facts li { font-family: var(--mono); font-size: 13px; border: 1px solid rgba(255,255,255,.22); border-radius: 999px; padding: 4px 12px }
.hero-clip video { width: 100%; aspect-ratio: 9 / 16; border-radius: 18px; background: #000; display: block }
.hero-clip .cap { font-family: var(--mono); font-size: 12px; color: var(--mast-muted); margin-top: 8px }
.rule { height: 4px; width: 64px; background: var(--accent-line); border-radius: 2px }
main .wrap { display: grid; gap: 56px; padding-block: 48px 72px }
h2 { font-family: var(--display); font-weight: 800; font-size: 26px; margin: 0 0 18px; text-wrap: balance }
.grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 22px }
.clip { display: grid; grid-template-rows: auto 1fr; gap: 10px; min-width: 0 }
.clip video { width: 100%; aspect-ratio: 9 / 16; border-radius: 14px; background: var(--sunk); display: block }
.meta { min-width: 0 }
.row { display: flex; align-items: center; gap: 10px; font-family: var(--mono); font-size: 12px; color: var(--muted) }
.num { color: var(--mast-ink); background: var(--mast); border-radius: 6px; padding: 1px 7px; font-weight: 700 }
.story { margin-left: auto; color: var(--accent); font-weight: 700; text-decoration: none; border-bottom: 1px solid currentColor }
.story:focus-visible, video:focus-visible { outline: 3px solid var(--accent-line); outline-offset: 2px }
.clip h3 { font-family: var(--display); font-weight: 800; font-size: 18px; margin: 6px 0 2px }
.hook { margin: 0; font-weight: 700 }
.what, .who { margin: 4px 0 0; color: var(--muted); font-size: 14px }
.who { font-family: var(--mono); font-size: 12px }
.cars { display: grid; gap: 18px }
.car { margin: 0; min-width: 0 }
.strip { overflow-x: auto; border-radius: 12px; background: var(--sunk) }
.strip img { display: block; height: 220px; width: auto; max-width: none }
.car figcaption { font-family: var(--mono); font-size: 12px; color: var(--muted); margin-top: 6px }
.cols { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 22px }
.panel { background: var(--surface); border: 1px solid var(--line); border-radius: 16px; padding: 20px 22px; min-width: 0 }
.panel h3 { font-family: var(--display); font-weight: 800; font-size: 18px; margin: 0 0 10px }
.panel ul { margin: 0; padding-left: 18px; display: grid; gap: 6px }
table { border-collapse: collapse; width: 100%; font-size: 14px }
.tbl { overflow-x: auto }
th, td { text-align: left; padding: 8px 10px; border-bottom: 1px solid var(--line); vertical-align: top }
th { font-family: var(--mono); font-size: 12px; color: var(--muted); font-weight: 500 }
td.wk { font-family: var(--mono); font-weight: 700; white-space: nowrap }
.ok { color: var(--teal); font-weight: 700 }
footer { color: var(--muted); font-size: 13px; padding-block: 0 40px }
@media (max-width: 760px) { .mast .wrap { grid-template-columns: 1fr } .hero-clip { max-width: 300px } }
@media (prefers-reduced-motion: reduce) { * { scroll-behavior: auto } }
</style>

<header class="mast">
  <div class="wrap">
    <div>
      <div class="brand"><b>Yafho</b><span>-Silicare</span> · @sil.icare</div>
      <h1>Видео-портфель: силиконовые пластины для рубцов</h1>
      <div class="rule"></div>
      <p style="margin-top:16px">Главный ролик и 17 тем: эффект в каждом ролике, крючок в первые три секунды, без голоса — крупные титры и стрелки. Факты только из паспорта продукта, под каждой цифрой — источник.</p>
      <ul class="facts">
        <li>18 роликов × 9:16 · 16:9 · 4:5</li><li>16 сторис 6–9 с</li><li>9 каруселей 4:5</li><li>контент-план на 4 недели</li>
      </ul>
    </div>
    <div class="hero-clip">
      <video controls preload="metadata" playsinline poster="{{HERO_POSTER}}" src="{{HERO_SRC}}" aria-label="Главный ролик"></video>
      <div class="cap">{{HERO_NAME}} · «Один рубец. Два исхода.» · {{HERO_LEN}} с</div>
    </div>
  </div>
</header>

<main>
  <div class="wrap">
    {{SERIES}}

    <section>
      <h2>Карусели для ленты</h2>
      <div class="cars">{{CAROUSELS}}</div>
    </section>

    <section>
      <h2>Как публиковать</h2>
      <div class="tbl"><table>
        <thead><tr><th>Неделя</th><th>Пн · Reels</th><th>Ср · Reels</th><th>Пт · Reels</th><th>Сторис</th></tr></thead>
        <tbody>
          <tr><td class="wk">1</td><td>Главный ролик</td><td>04 Как наклеить</td><td>05 Результат</td><td>05, 04, 08, 13</td></tr>
          <tr><td class="wk">2</td><td>02 Механизм</td><td>03 Показания</td><td>14 После кесарева</td><td>02, 03, 14, 10</td></tr>
          <tr><td class="wk">3</td><td>10 Когда начинать</td><td>06 Подбор размера</td><td>11 День с пластиной</td><td>11, 07, 12, 15</td></tr>
          <tr><td class="wk">4</td><td>07 Мифы и ошибки</td><td>08 Цифры</td><td>15 После операции</td><td>16, 17, 08, 04</td></tr>
        </tbody>
      </table></div>
      <p class="what">Дальше: 12 Когда нельзя · 13 Вопрос-ответ · 16 После ожога · 17 Растяжки. Ролик 09 (5 с, QR и @sil.icare) — закреп в профиле и концовка сторис. Подписи к каждому посту — в <span style="font-family:var(--mono)">CONTENT_PLAN.md</span>.</p>
    </section>

    <section class="cols">
      <div class="panel">
        <h3>Правила, по которым сделано</h3>
        <ul>
          <li>Только «мягче, светлее, ровнее», «снижает риск». Никаких «уберёт», «100%», «навсегда».</li>
          <li>Эффект «до → после» — схема с плашкой «схема», не фото пациента.</li>
          <li>Титр ≤ 6 слов и ≥ 2,5 с на экране; текст с контрастом ≥ 4,5:1.</li>
          <li>Нет лиц, ран и крови. Логотип и текст — только из кода.</li>
          <li><span class="ok">Проверено скриптом:</span> 0 ошибок по всем сценариям.</li>
        </ul>
      </div>
      <div class="panel">
        <h3>Что нужно от заказчика</h3>
        <ul>
          <li>Фон с сайта Yafho — скриншот или ссылка (сейчас льняная заглушка).</li>
          <li>Размеры пластин по упаковке — для тем 06 и 14–17.</li>
          <li>Логотип, если есть (сейчас текст «Yafho-Silicare»).</li>
          <li>По желанию — клипы Kling: каждый сам заменит свой рисованный кадр.</li>
        </ul>
      </div>
    </section>
  </div>
</main>
<footer><div class="wrap">Видео в 720p для просмотра; исходники 1080p и форматы 16:9 / 4:5 — в папке проекта <span style="font-family:var(--mono)">output/yafho/</span>.</div></footer>
"""

if __name__ == "__main__":
    main()
