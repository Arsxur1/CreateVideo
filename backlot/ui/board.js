// Backlot project board — renders BoardState and stays live via SSE.

import {
  STAGE_ICONS, el, fmtAgo, fmtClock, fmtDuration, fmtMoney,
  getJSON, mediaURL, subscribe, thumbURL, waveBars,
} from "/ui/lib.js";

const rawProjectPath = location.pathname.split("/p/")[1] || "";
const projectId = decodeURIComponent(rawProjectPath);
const encodedProjectId = encodeURIComponent(projectId);
const app = document.getElementById("app");
const modal = document.getElementById("modal");
const player = document.getElementById("player");

const THEME_KEY = "backlot.theme";
let currentTheme = localStorage.getItem(THEME_KEY) === "light" ? "light" : "dark";
let state = null;
let selectedStage = null;   // stage drawer open for this stage name
let activeRender = 0;
let replay = null;          // {t0, t1, t, playing} — replay mode when non-null
let firstPaint = true;

function applyTheme(theme) {
  currentTheme = theme === "light" ? "light" : "dark";
  document.documentElement.dataset.theme = currentTheme;
  localStorage.setItem(THEME_KEY, currentTheme);
}

function renderThemeToggle() {
  const next = currentTheme === "light" ? "dark" : "light";
  return el("button", {
    class: "theme-toggle",
    type: "button",
    title: `Switch to ${next} theme`,
    "aria-label": `Switch to ${next} theme`,
    "aria-pressed": currentTheme === "light" ? "true" : "false",
    onclick: () => {
      applyTheme(next);
      render();
    },
  }, el("span", { class: "theme-toggle-icon", "aria-hidden": "true" }, currentTheme === "light" ? "☾" : "☀"));
}

applyTheme(currentTheme);

// ---------------------------------------------------------------------------
// header slate
// ---------------------------------------------------------------------------

function renderSlate(s) {
  const board = s.storyboard;
  const chips = [
    el("span", { class: "chip" }, `${s.pipeline.pipeline_type} pipeline`),
    board && board.total_duration_seconds
      ? el("span", { class: "chip" }, `${board.scenes.length} scenes · ${fmtDuration(board.total_duration_seconds)}`)
      : null,
    s.style_playbook ? el("span", { class: "chip" }, s.style_playbook) : null,
  ];

  const awaiting = s.stages.find((x) => x.status === "awaiting_human");
  const inProgress = s.stages.find((x) => x.status === "in_progress");
  const stalled = s.stages.find((x) => x.stalled);
  let liveEl;
  if (awaiting) {
    liveEl = el("span", { class: "live" }, el("span", { class: "dot" }), "◈ AWAITING YOU");
  } else if (stalled) {
    liveEl = el("span", { class: "live", style: "color:var(--red)" },
      el("span", { class: "dot", style: "background:var(--red);animation:none" }), "⚠ STALLED?");
  } else if (s.live || inProgress) {
    liveEl = el("span", { class: "live" }, el("span", { class: "dot" }), "LIVE");
  } else {
    liveEl = el("span", { class: "live idle" }, el("span", { class: "dot" }),
      `IDLE${s.last_activity ? " · " + fmtAgo(s.last_activity).toUpperCase() : ""}`);
  }

  const cost = el("div", { class: "cost" });
  if (s.cost) {
    const spent = s.cost.total_spent_usd ?? 0;
    const budget = spent + (s.cost.budget_remaining_usd ?? 0);
    const hasBudget = s.cost.budget_remaining_usd != null;
    const pct = hasBudget && budget > 0 ? Math.min(100, (spent / budget) * 100) : 0;
    cost.append(el("div", { class: "nums" }, el("b", {}, fmtMoney(spent)),
      hasBudget ? el("span", {}, ` / ${fmtMoney(budget)}`) : ""));
    if (hasBudget) {
      cost.append(el("div", { class: "bar" }, el("i", {
        class: pct > 90 ? "crit" : pct > 75 ? "warn" : "", style: `width:${pct}%`,
      })));
    }
    cost.append(el("div", { class: "label" }, "generation spend"));
  }

  return el("header", { class: "slate" },
    el("div", { class: "clapper" }),
    el("div", {},
      el("a", { class: "wordmark", href: "/", style: "text-decoration:none" }, "Backlot"),
      el("h1", {}, s.title),
    ),
    ...chips,
    el("div", { class: "spacer" }),
    renderThemeToggle(),
    liveEl,
    cost,
  );
}

// ---------------------------------------------------------------------------
// stage rail
// ---------------------------------------------------------------------------

function stageSub(st) {
  if (st.status === "awaiting_human") return "awaiting your approval\nreply in chat to continue";
  if (st.status === "in_progress" && st.stalled) {
    return `stalled? no activity for ${st.stalled_minutes}m\nask the agent for status`;
  }
  if (st.status === "in_progress" && st.partial_progress) {
    const done = st.partial_progress.completed_scene_ids;
    if (Array.isArray(done)) return `${done.length} scene${done.length === 1 ? "" : "s"} done`;
    return "in progress";
  }
  if (st.status === "in_progress") return "in progress";
  if (st.status === "failed") return st.error ? String(st.error).slice(0, 60) : "failed";
  if (st.timestamp) {
    const approved = st.gated && st.human_approved ? " · approved" : "";
    return fmtClock(st.timestamp) + approved;
  }
  return "";
}

function renderRail(s) {
  const rail = el("nav", { class: "rail" });
  let pendingIndex = 1;
  for (const st of s.stages) {
    const cls = st.status === "completed" ? "done"
      : st.status === "in_progress" ? (st.stalled ? "active stalled" : "active")
      : st.status === "awaiting_human" ? "await"
      : st.status === "failed" ? "failed" : "";
    const icon = STAGE_ICONS[st.status] || String(pendingIndex);
    if (!STAGE_ICONS[st.status]) pendingIndex += 1;
    const node = el("div", {
      class: `stage ${cls}${selectedStage === st.name ? " selected" : ""}${st.undeclared ? " undeclared" : ""}`,
      title: st.undeclared ? `"${st.name}" ran but isn't declared by this pipeline's manifest` : null,
      onclick: () => toggleDrawer(st.name),
    },
      el("span", { class: "line" }),
      el("span", { class: "node" }, icon),
      el("span", { class: "name" }, st.name),
      el("span", { class: "sub", style: "white-space:pre-line" },
        st.undeclared ? `${stageSub(st)}\nunlisted`.trim() : stageSub(st)),
    );
    rail.append(node);
  }
  return rail;
}

function toggleDrawer(stageName) {
  selectedStage = selectedStage === stageName ? null : stageName;
  render();
}

const STAGE_ARTIFACTS = {
  research: ["research_brief"],
  proposal: ["proposal_packet"],
  idea: ["brief"],
  script: ["script"],
  scene_plan: ["scene_plan"],
  assets: ["asset_manifest"],
  edit: ["edit_decisions"],
  compose: ["render_report", "final_review"],
  publish: ["publish_log"],
};

function artifactNamesForStage(st) {
  const declared = Array.isArray(st.produces) ? st.produces : [];
  const fallback = STAGE_ARTIFACTS[st.name] || [];
  return [...new Set([...declared, ...fallback].filter(Boolean))];
}

function reviewMetrics(review) {
  const nested = review && review.summary && typeof review.summary === "object"
    ? review.summary : {};
  return {
    critical: Number((review && review.critical) ?? nested.critical ?? 0),
    suggestions: Number((review && review.suggestions) ?? nested.suggestions ?? 0),
    nitpicks: Number((review && review.nitpicks) ?? nested.nitpicks ?? 0),
  };
}

function reviewSummaryText(review) {
  if (!review) return "";
  if (typeof review.summary === "string") return review.summary;
  const nested = review.summary && typeof review.summary === "object" ? review.summary : {};
  const counts = reviewMetrics(review);
  return [
    review.decision,
    `${counts.critical} critical`,
    `${counts.suggestions} suggestion${counts.suggestions === 1 ? "" : "s"}`,
    nested.review_focus_met ? `review focus ${nested.review_focus_met}` : null,
    nested.schema_validation,
  ].filter(Boolean).join(" · ");
}

function renderDrawer(s) {
  if (!selectedStage) return null;
  const st = s.stages.find((x) => x.name === selectedStage);
  if (!st) return null;

  const body = el("div", { class: "drawer-body" });

  if (st.review) {
    const metrics = reviewMetrics(st.review);
    const summary = reviewSummaryText(st.review);
    body.append(el("div", { class: "findings", style: "margin-bottom:12px" },
      el("span", { class: `f ${metrics.critical ? "crit" : ""}` }, `${metrics.critical} critical`),
      el("span", { class: `f ${metrics.suggestions ? "sugg" : ""}` }, `${metrics.suggestions} suggestions`),
      el("span", { class: "f" }, `${metrics.nitpicks} nitpicks`),
      summary ? el("span", { style: "font-size:calc(11.5px * var(--fs-scale));color:var(--text-2);margin-left:8px" }, summary) : null,
    ));
  }

  const names = artifactNamesForStage(st);
  let shown = false;
  for (const name of names) {
    const artifact = s.artifacts[name];
    if (!artifact) continue;
    // decision_log is global (right-rail Decisions panel), not a per-stage doc.
    if (name === "decision_log") continue;
    const reading = renderStageReading(st, name, artifact, s);
    if (!reading) continue;
    shown = true;
    body.append(reading);
  }
  if (!shown) {
    body.append(el("div", { class: "hint" },
      st.status === "pending" ? "This stage hasn't run yet." : "No canonical artifact found on disk for this stage."));
  }

  return el("div", { class: `drawer${shown ? " has-reading" : ""}` },
    el("div", { class: "drawer-head" },
      el("h3", {}, `${st.name} — ${st.status}`),
      st.gate_skipped ? el("span", { class: "gate-chip" }, "⚑ GATE SKIPPED") : null,
      st.versions > 1 ? el("span", { class: "ver-chip" }, `v${st.versions}`) : null,
      st.timestamp ? el("span", { class: "meta", style: "font-family:var(--mono);font-size:calc(10.5px * var(--fs-scale));color:var(--text-3)" }, st.timestamp) : null,
      el("span", { class: "close", onclick: () => toggleDrawer(st.name) }, "CLOSE ✕"),
    ),
    body,
  );
}

// ---------------------------------------------------------------------------
// ---------------------------------------------------------------------------
// stage reading dispatcher — what the drawer shows when a stage is clicked.
// script & scene_plan have bespoke warm-paper renderers; every other stage's
// artifact is rendered readably by renderGenericReading (spec-driven), with
// the raw JSON kept as a collapsible <details> at the bottom.
// ---------------------------------------------------------------------------

function renderStageReading(st, name, artifact, s) {
  if (name === "script") return renderScriptCard(s);
  if (name === "scene_plan") return renderStoryboard(s);
  return renderGenericReading(st, name, artifact, s);
}

// Declarative per-artifact spec: how to surface each non-bespoke stage's
// artifact as a warm-paper doc. Adding a stage = one entry. Fields are
// [dottedKeyPath, label, fmt] where fmt ∈ text|money|duration|list|count.
// Scalars (text/money/duration/count) render as chips; lists render as
// warm asset-box stacks. Unknown artifacts (e.g. final_review) and any
// artifact without an entry fall through to a generic key-value dump.
const READING_SPEC = {
  research_brief: {
    title: (a) => a.topic,
    lead: (a) => a.research_summary,
    fields: [
      ["angles_discovered", "Angles discovered", "list"],
      ["data_points", "Data points", "list"],
      ["sources", "Sources", "list"],
    ],
  },
  proposal_packet: {
    title: (a) => {
      const sel = (a.selected_concept || {}).concept_id;
      const c = (a.concept_options || []).find((o) => o.id === sel || o.concept_id === sel);
      return (c && (c.title || c.name)) || "Production proposal";
    },
    lead: (a) => (a.selected_concept || {}).rationale,
    fields: [
      ["cost_estimate.total_estimated_usd", "Estimated cost", "money"],
      ["production_plan.render_runtime", "Runtime", "text"],
      ["production_plan.pipeline", "Pipeline", "text"],
      ["concept_options", "Concepts", "list"],
    ],
  },
  brief: {
    title: (a) => a.title || a.core_message,
    lead: (a) => a.hook,
    fields: [
      ["target_platform", "Platform", "text"],
      ["target_duration_seconds", "Duration", "duration"],
      ["tone", "Tone", "text"],
      ["key_points", "Key points", "list"],
    ],
  },
  asset_manifest: {
    title: () => "Generated assets",
    fields: [
      ["total_cost_usd", "Generation cost", "money"],
      ["assets", "Assets", "list"],
    ],
  },
  edit_decisions: {
    title: () => "Edit decisions",
    fields: [
      ["render_runtime", "Runtime", "text"],
      ["cuts", "Cuts", "list"],
      ["audio.music", "Music", "text"],
      ["slideshow_risk_score.verdict", "Slideshow risk", "text"],
    ],
  },
  render_report: {
    title: () => "Render report",
    fields: [
      ["render_time_seconds", "Render time", "duration"],
      ["render_grammar", "Grammar", "text"],
      ["outputs", "Outputs", "list"],
      ["warnings", "Warnings", "list"],
      ["verification_notes", "Verification", "list"],
    ],
  },
  publish_log: {
    title: () => "Publish log",
    fields: [["entries", "Destinations", "list"]],
  },
};

function resolvePath(obj, path) {
  if (obj == null) return undefined;
  if (!String(path).includes(".")) return obj[path];
  return String(path).split(".").reduce((acc, key) => (acc == null ? acc : acc[key]), obj);
}

function humanizeKey(k) {
  return String(k).replace(/[_-]+/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());
}

function readingItemLabel(it) {
  if (it == null) return "";
  if (typeof it !== "object") return String(it);
  return it.title || it.name || it.platform || it.destination || it.hook
    || it.id || it.status || it.path || it.tool_name || "";
}
function readingItemDesc(it) {
  if (it == null || typeof it !== "object") return "";
  return it.description || it.hook || it.url || it.reason || it.rationale
    || it.format || it.type || it.approach || "";
}

// A list field → stacked warm asset boxes (reuses .reading .asset.ok).
function readingListBlock(label, items) {
  const arr = Array.isArray(items) ? items : [];
  if (!arr.length) return null;
  const CAP = 20;
  const rows = arr.slice(0, CAP).map((it) => {
    const t = readingItemLabel(it);
    const d = readingItemDesc(it);
    return el("div", { class: "asset ok" },
      el("span", { class: "ico" }, "•"),
      el("div", {},
        t ? el("span", { class: "alabel" }, t) : null,
        d ? el("span", { class: "txt" }, d) : null));
  });
  const over = arr.length - CAP;
  if (over > 0) rows.push(el("div", { class: "asset" },
    el("span", { class: "ico" }, "…"),
    el("div", {}, el("span", { class: "txt" }, `${over} more`))));
  return el("div", { class: "gfield" },
    el("div", { class: "glabel" }, `${label} · ${arr.length}`),
    el("div", { class: "assets" }, ...rows));
}

// A scalar field → a chip for the meta row. Objects are not chip-shaped.
function readingScalarChip(label, value, fmt) {
  if (value == null || value === "") return null;
  let text;
  if (fmt === "money") text = fmtMoney(value);
  else if (fmt === "duration") text = fmtDuration(value);
  else if (typeof value === "object") return null;
  else text = String(value);
  if (text == null || text === "") return null;
  return el("span", { class: "rchip" }, `${label}: ${text}`);
}

function renderGenericReading(st, name, artifact, s) {
  const spec = READING_SPEC[name] || {};
  const title = (spec.title ? spec.title(artifact, s) : null)
    || artifact.title || artifact.topic || s.title;
  const lead = spec.lead ? spec.lead(artifact, s) : null;
  const lang = ((artifact.metadata && artifact.metadata.language) || "en");

  const root = el("section", { class: "reading reading-generic" });
  root.append(el("div", { class: "r-toolbar" },
    el("button", {
      class: "r-btn primary", type: "button", title: "이 문서를 HTML로 다운로드",
      onclick: () => downloadReading(root, `${slug(s.project_id)}-${name}.html`, title, lang),
    }, "↓ HTML 다운로드")));

  root.append(el("div", { class: "eyebrow" }, `${st.name} · ${name}.json`));
  root.append(el("h1", {}, title));
  if (lead) root.append(el("p", { class: "subtitle" }, lead));

  const chips = [];
  const blocks = [];
  for (const field of (spec.fields || [])) {
    const [path, label, fmt] = field;
    const value = resolvePath(artifact, path);
    if (fmt === "list") {
      const b = readingListBlock(label, value);
      if (b) blocks.push(b);
    } else {
      const c = readingScalarChip(label, value, fmt);
      if (c) chips.push(c);
    }
  }

  // Unknown artifact (no spec entry) → generic readable dump of every key.
  if (!spec.fields) {
    for (const [k, v] of Object.entries(artifact || {})) {
      if (v == null || k === "metadata") continue;
      if (Array.isArray(v)) {
        const b = readingListBlock(humanizeKey(k), v);
        if (b) blocks.push(b);
      } else if (typeof v === "object") {
        const b = readingListBlock(humanizeKey(k),
          Object.entries(v).map(([kk, vv]) => ({ name: kk, description: typeof vv === "object" ? "" : String(vv) })));
        if (b) blocks.push(b);
      } else {
        const c = readingScalarChip(humanizeKey(k), v, "text");
        if (c) chips.push(c);
      }
    }
  }

  if (chips.length) root.append(el("div", { class: "meta" }, ...chips));
  if (blocks.length) root.append(el("div", { class: "gfields" }, ...blocks));

  // Raw JSON safety net for power users / debugging.
  root.append(el("details", {},
    el("summary", {}, "Raw JSON"),
    el("pre", {}, JSON.stringify(artifact, null, 2))));

  root.append(buildReadingFooter(s, `projects/${s.project_id}/artifacts/${name}.json`,
    [`${st.name} stage · ${name} artifact`]));
  return root;
}

// reading views — warm paper documents for script & scene plan
// (design system in reading.css, namespaced under .reading). The standalone
// HTML download clones the live document so screen == file, always.
// ---------------------------------------------------------------------------

const TYPE_COLORS = {
  broll: "#C97B5E", text_card: "#2D4A3E", animation: "#8BA888",
  talking_head: "#6E8A6B", diagram: "#7B8FA8", character_scene: "#9B7BA8",
  transition: "#B8893E", generated: "#C98E5E", screen_recording: "#5E7A8A",
};
const TYPE_LABELS = {
  broll: "b-roll", text_card: "text card", animation: "animation",
  talking_head: "talking head", diagram: "diagram", character_scene: "character scene",
  transition: "transition", generated: "generated", screen_recording: "screen recording",
};
const CUE_LABELS = {
  overlay: "오버레이", broll: "B-roll", diagram: "다이어그램",
  stat_card: "통계 카드", code_snippet: "코드", animation: "애니메이션",
};

function escapeHTML(s) {
  return String(s == null ? "" : s).replace(/[&<>"']/g, (c) => (
    { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
}
function slug(id) {
  return String(id || "project").replace(/[^a-z0-9-]+/gi, "-").replace(/^-+|-+$/g, "").toLowerCase() || "project";
}
function axisTicks(total) {
  const t = Number(total);
  if (!Number.isFinite(t) || t <= 0) return [0];
  const out = [];
  for (let k = 0; k <= 4; k++) out.push(Math.round((t * k) / 4));
  return out;
}
function buildAxis(total) {
  return el("div", { class: "axis" }, ...axisTicks(total).map((t) => el("span", {}, `${t}s`)));
}
// Wrap emphasis words in <em> (peach highlighter). Terms sorted longest-first
// so a phrase wins over its substring. Text is split into nodes — no innerHTML.
function highlightEmphasis(text, words) {
  const frag = document.createDocumentFragment();
  const str = String(text || "");
  const terms = (words || []).map((w) => String(w)).filter(Boolean).sort((a, b) => b.length - a.length);
  let i = 0;
  while (i < str.length) {
    let hit = null;
    for (const t of terms) { if (t && str.startsWith(t, i)) { hit = t; break; } }
    if (hit) { frag.append(el("em", {}, hit)); i += hit.length; }
    else { frag.append(str[i]); i += 1; }
  }
  return frag;
}

// ---- standalone HTML export (clone the live doc → portable file) ----
let _readingCssText = null;
async function readingCssText() {
  if (_readingCssText !== null) return _readingCssText;
  try {
    const res = await fetch("/ui/reading.css", { cache: "no-cache" });
    _readingCssText = await res.text();
  } catch { _readingCssText = ""; }
  return _readingCssText;
}
function docHTML(title, bodyHTML, cssText, lang) {
  return `<!DOCTYPE html>\n<html lang="${escapeHTML(lang || "en")}">\n<head>\n`
    + `<meta charset="UTF-8">\n<meta name="viewport" content="width=device-width, initial-scale=1.0">\n`
    + `<title>${escapeHTML(title)}</title>\n<style>${cssText}</style>\n</head>\n<body>\n${bodyHTML}\n</body>\n</html>`;
}
function blobToDataURL(blob) {
  return new Promise((res, rej) => {
    const r = new FileReader();
    r.onload = () => res(String(r.result));
    r.onerror = rej;
    r.readAsDataURL(blob);
  });
}
// Inline every <img>/<video> as a data URL so the downloaded doc is portable
// (opens correctly with no server). Videos → their cached poster JPEG.
async function inlineMedia(root) {
  await Promise.all([...root.querySelectorAll("img")].map(async (img) => {
    try {
      const res = await fetch(img.src);
      if (!res.ok) return;
      img.src = await blobToDataURL(await res.blob());
    } catch { /* leave as-is */ }
  }));
  await Promise.all([...root.querySelectorAll("video")].map(async (v) => {
    try {
      const res = await fetch(v.dataset.posterSrc || v.src);
      if (!res.ok) return;
      const img = el("img", { alt: "" });
      img.src = await blobToDataURL(await res.blob());
      v.replaceWith(img);
    } catch { /* leave as-is */ }
  }));
}
function triggerDownload(blob, filename) {
  const url = URL.createObjectURL(blob);
  const a = el("a", { href: url, download: filename });
  document.body.appendChild(a);
  a.click();
  a.remove();
  setTimeout(() => URL.revokeObjectURL(url), 5000);
}
async function downloadReading(rootEl, filename, title, lang) {
  if (!rootEl) return;
  const clone = rootEl.cloneNode(true);
  clone.classList.add("reading-doc");
  clone.querySelectorAll(".r-toolbar").forEach((t) => t.remove());
  await inlineMedia(clone);
  const html = docHTML(title, clone.outerHTML, await readingCssText(), lang);
  triggerDownload(new Blob([html], { type: "text/html;charset=utf-8" }), filename);
}

function vpItem(k, v) { return el("div", { class: "vp-item" }, el("div", { class: "k" }, k), el("div", { class: "v" }, v)); }
function deliverySpan(k, v) { return el("span", {}, el("b", {}, `${k}: `), v); }
function collectPron(sections) {
  const map = new Map();
  for (const sec of sections || []) {
    for (const p of sec.pronunciation_guides || []) {
      if (p && p.word && !map.has(p.word)) map.set(p.word, p.phonetic || "");
    }
  }
  return [...map.entries()].map(([word, phonetic]) => ({ word, phonetic }));
}
function buildReadingFooter(s, artifactPath, extras) {
  const rows = [el("div", {}, el("b", {}, "원본 artifact: "), el("code", {}, artifactPath))];
  const ex = (extras || []).filter(Boolean);
  if (ex.length) rows.push(el("div", {}, ...ex.map((e, i) => [i ? " · " : "", e]).flat()));
  rows.push(el("div", { class: "foot-dim" }, `OpenMontage Backlot · ${s.title}`));
  return el("footer", {}, ...rows);
}

function buildScriptTimeline(sections) {
  const total = sections.reduce((m, sec) => Math.max(m, Number(sec.end_seconds) || 0), 0);
  const box = el("div", { class: "timeline-box" },
    el("div", { class: "tl-label" }, `Timeline · ${sections.length} sections · 0s → ${Math.round(total)}s`));
  const tl = el("div", { class: "timeline" });
  sections.forEach((sec, i) => {
    const dur = Math.max(0.001, (Number(sec.end_seconds) || 0) - (Number(sec.start_seconds) || 0));
    const seg = el("div", {
      class: `seg sc-s${(i % 6) + 1}`,
      title: `${sec.id || ""} · ${sec.start_seconds}–${sec.end_seconds}s`,
    });
    seg.style.flexGrow = String(dur);
    seg.textContent = (sec.id || `s${i + 1}`).toUpperCase();
    tl.append(seg);
  });
  box.append(tl, buildAxis(total));
  return box;
}

function renderScriptCard(s) {
  const script = s.artifacts.script;
  if (!script) return null;
  const vp = script.voice_performance || {};
  const sections = script.sections || [];
  const meta = script.metadata || {};
  const lang = meta.language || "en";
  const sampleId = vp.sample_section_id;

  const root = el("section", { class: "reading reading-script" });
  root.append(el("div", { class: "r-toolbar" },
    el("button", {
      class: "r-btn primary", type: "button", title: "이 대본을 HTML로 다운로드",
      onclick: () => downloadReading(root, `${slug(s.project_id)}-script.html`, script.title || s.title, lang),
    }, "↓ HTML 다운로드")));

  root.append(el("div", { class: "eyebrow" }, "Production Script · Narration"));
  root.append(el("h1", {}, script.title || s.title));
  if (vp.performance_intent) root.append(el("p", { class: "subtitle" }, vp.performance_intent));

  const chips = [
    script.total_duration_seconds ? el("span", { class: "rchip accent" }, `${script.total_duration_seconds}초`) : null,
    el("span", { class: "rchip" }, `${sections.length}섹션`),
    vp.pacing_profile ? el("span", { class: "rchip" }, vp.pacing_profile) : null,
    meta.pacing_wpm_estimate ? el("span", { class: "rchip" }, `~${meta.pacing_wpm_estimate}wpm`) : null,
    lang ? el("span", { class: "rchip" }, lang === "ko" ? "한국어" : lang) : null,
  ].filter(Boolean);
  if (chips.length) root.append(el("div", { class: "meta" }, ...chips));

  if (vp.performance_intent || vp.energy_curve || vp.pause_policy || vp.pacing_profile || vp.provider_notes) {
    const grid = el("div", { class: "vp-grid" });
    if (vp.pacing_profile) grid.append(vpItem("Pacing", vp.pacing_profile));
    if (vp.energy_curve) grid.append(vpItem("Energy Curve", vp.energy_curve));
    if (vp.pause_policy) grid.append(vpItem("Pause Policy", vp.pause_policy));
    const provKeys = Object.keys(vp.provider_notes || {});
    if (provKeys.length) grid.append(vpItem("Provider Notes",
      el("div", { class: "vp-providers" },
        provKeys.map((k) => el("div", { class: "vp-prov" }, el("b", {}, k), vp.provider_notes[k])))));
    const panel = el("div", { class: "vp" },
      el("h2", {}, "Voice Performance Plan"),
      vp.performance_intent ? el("p", { class: "intent" }, vp.performance_intent) : null,
      grid);
    if (sampleId) panel.append(el("span", { class: "sample-tag" }, `TTS 샘플 구간: ${sampleId}`));
    root.append(panel);
  }

  root.append(buildScriptTimeline(sections));

  const scenesEl = el("div", { class: "scenes" });
  sections.forEach((sec, i) => {
    const dc = sec.delivery_cues || {};
    const isSample = sampleId && sec.id === sampleId;
    const card = el("div", { class: `card${isSample ? " sample" : ""}` });
    card.append(el("div", { class: "card-head" },
      el("span", { class: "sc-id" }, (sec.id || `s${i + 1}`).toUpperCase()),
      sec.label ? el("span", { class: "label" }, sec.label) : null,
      dc.pace ? el("span", { class: `pace-chip${isSample ? " sample" : ""}` }, `${dc.pace}${isSample ? " · ⭐샘플" : ""}`) : null,
      el("span", { class: "time" }, `${sec.start_seconds}–${sec.end_seconds}s`)));
    card.append(el("div", { class: "narration" }, highlightEmphasis(sec.text, dc.emphasis_words)));

    const body = el("div", { class: "body" });
    const delivery = [];
    if (dc.energy) delivery.push(deliverySpan("energy", dc.energy));
    if (dc.emphasis_words && dc.emphasis_words.length) delivery.push(deliverySpan("emphasis", dc.emphasis_words.join(" · ")));
    if (dc.pause_before_seconds) delivery.push(deliverySpan("pause_before", `${dc.pause_before_seconds}s`));
    if (dc.pause_after_seconds) delivery.push(deliverySpan("pause_after", `${dc.pause_after_seconds}s`));
    if (delivery.length) body.append(el("div", { class: "delivery" }, ...delivery));
    if (dc.delivery_note) body.append(el("div", { class: "note" }, dc.delivery_note));

    const cues = sec.enhancement_cues || [];
    if (cues.length) {
      const vis = el("div", { class: "visual" }, el("div", { class: "vlabel" }, "Visual"));
      for (const c of cues) vis.append(el("span", { class: "vchip" }, `${CUE_LABELS[c.type] || c.type} · ${c.description || ""}`));
      body.append(vis);
    }
    if (sec.source_ref) body.append(el("div", { class: "grounding" }, el("b", {}, "근거: "), sec.source_ref));
    if (dc.provider_text) body.append(el("div", { class: "tts" },
      el("span", { class: "tlabel" }, "TTS-ready"), el("code", {}, dc.provider_text)));
    if (body.childNodes.length) card.append(body);
    scenesEl.append(card);
  });
  root.append(scenesEl);

  const pron = collectPron(sections);
  if (pron.length) root.append(el("div", { class: "pron" },
    el("h3", {}, "Pronunciation Guides"),
    el("div", { class: "pron-grid" },
      ...pron.map((p) => el("div", { class: "p" }, el("b", {}, p.word), el("span", {}, p.phonetic))))));

  const lastText = sections.length ? sections[sections.length - 1].text : "";
  if (lastText) root.append(el("div", { class: "closer" }, `"${shortText(lastText, 140)}"`));

  root.append(buildReadingFooter(s, `projects/${s.project_id}/artifacts/script.json`, [
    meta.pipeline ? `파이프라인: ${meta.pipeline}` : null,
    meta.selected_concept ? `콘셉트: ${meta.selected_concept}` : null,
  ]));
  return root;
}

function humanize(value) {
  return String(value || "artifact").replaceAll("_", " ");
}

function shortText(value, limit = 180) {
  const text = String(value || "").trim();
  return text.length > limit ? `${text.slice(0, limit - 1)}…` : text;
}

function reviewFact(label, value) {
  if (value == null || value === "") return null;
  return el("div", { class: "approval-fact" },
    el("span", {}, label),
    el("b", {}, value),
  );
}

function reviewFacts(items) {
  const facts = items.filter(Boolean);
  return facts.length ? el("div", { class: "approval-facts" }, facts) : null;
}

function titledItems(items, selectedId = null) {
  const rows = (items || []).slice(0, 4).map((item, index) => {
    if (item == null) return null;
    if (typeof item !== "object") {
      return el("li", {}, shortText(item));
    }
    const id = item.id || item.concept_id || item.option_id;
    const title = item.title || item.name || item.display_name || item.label || id || item.path || item.platform || item.description || `Item ${index + 1}`;
    const detail = item.hook || item.why_this_works || item.summary || item.description || item.silhouette_notes;
    return el("li", { class: id && id === selectedId ? "selected" : "" },
      el("div", { class: "approval-item-title" }, shortText(title, 100),
        id && id === selectedId ? el("span", { class: "approval-selected" }, "SELECTED") : null),
      detail && detail !== title ? el("p", {}, shortText(detail)) : null,
    );
  }).filter(Boolean);
  return rows.length ? el("ul", { class: "approval-items" }, rows) : null;
}

function genericArtifactSummary(artifact) {
  const facts = [];
  const items = [];
  for (const [key, value] of Object.entries(artifact || {})) {
    if (["version", "decision_log_ref"].includes(key)) continue;
    if (["string", "number", "boolean"].includes(typeof value)) {
      facts.push(reviewFact(humanize(key), shortText(value, 90)));
    } else if (Array.isArray(value)) {
      facts.push(reviewFact(humanize(key), `${value.length} item${value.length === 1 ? "" : "s"}`));
      if (!items.length && value.length) items.push(titledItems(value));
    }
    if (facts.length >= 6) break;
  }
  return [reviewFacts(facts), ...items].filter(Boolean);
}

function artifactReviewContent(name, artifact) {
  if (name === "brief") {
    return [
      artifact.hook ? el("p", { class: "approval-lead" }, artifact.hook) : null,
      reviewFacts([
        reviewFact("platform", artifact.target_platform),
        reviewFact("duration", artifact.target_duration_seconds != null ? fmtDuration(artifact.target_duration_seconds) : null),
        reviewFact("tone", artifact.tone),
        reviewFact("style", artifact.style),
      ]),
      titledItems(artifact.key_points),
    ].filter(Boolean);
  }
  if (name === "proposal_packet") {
    const selected = (artifact.selected_concept || {}).concept_id;
    const plan = artifact.production_plan || {};
    const cost = artifact.cost_estimate || {};
    return [
      reviewFacts([
        reviewFact("runtime", plan.render_runtime),
        reviewFact("pipeline", plan.pipeline),
        reviewFact("estimated cost", cost.total_estimated_usd != null ? fmtMoney(cost.total_estimated_usd) : null),
        reviewFact("concepts", Array.isArray(artifact.concept_options) ? artifact.concept_options.length : null),
      ]),
      titledItems(artifact.concept_options, selected),
      (artifact.selected_concept || {}).rationale
        ? el("p", { class: "approval-rationale" },
          el("b", {}, "WHY THIS CONCEPT  "), shortText(artifact.selected_concept.rationale))
        : null,
    ].filter(Boolean);
  }
  if (name === "research_brief") {
    return [
      artifact.topic ? el("p", { class: "approval-lead" }, artifact.topic) : null,
      reviewFacts([
        reviewFact("sources", Array.isArray(artifact.sources) ? artifact.sources.length : null),
        reviewFact("data points", Array.isArray(artifact.data_points) ? artifact.data_points.length : null),
        reviewFact("angles", Array.isArray(artifact.angles_discovered) ? artifact.angles_discovered.length : null),
      ]),
      titledItems(artifact.angles_discovered),
    ].filter(Boolean);
  }
  if (name === "script") {
    const first = (artifact.sections || [])[0];
    return [
      reviewFacts([
        reviewFact("duration", fmtDuration(artifact.total_duration_seconds)),
        reviewFact("sections", (artifact.sections || []).length),
      ]),
      first && first.text ? el("p", { class: "approval-lead" }, shortText(first.text, 220)) : null,
      el("p", { class: "approval-guidance" }, "Open the script stage in the rail to read the full document."),
    ].filter(Boolean);
  }
  if (name === "scene_plan") {
    const scenes = artifact.scenes || [];
    const end = scenes.reduce((max, scene) => Math.max(max, Number(scene.end_seconds) || 0), 0);
    return [
      reviewFacts([
        reviewFact("scenes", scenes.length),
        reviewFact("duration", end ? fmtDuration(end) : null),
      ]),
      titledItems(scenes),
      el("p", { class: "approval-guidance" }, "Open the scene_plan stage in the rail to review timing and coverage."),
    ].filter(Boolean);
  }
  if (name === "asset_manifest") {
    const assets = artifact.assets || [];
    const types = [...new Set(assets.map((asset) => asset.type).filter(Boolean))];
    return [
      reviewFacts([
        reviewFact("assets", assets.length),
        reviewFact("types", types.join(", ")),
        reviewFact("generation cost", artifact.total_cost_usd != null ? fmtMoney(artifact.total_cost_usd) : null),
      ]),
      titledItems(assets),
      el("p", { class: "approval-guidance" }, "Open the assets stage in the rail to inspect every generated take."),
    ].filter(Boolean);
  }
  if (name === "edit_decisions") {
    return [
      reviewFacts([
        reviewFact("cuts", Array.isArray(artifact.cuts) ? artifact.cuts.length : null),
        reviewFact("runtime", artifact.render_runtime || (artifact.metadata || {}).render_runtime),
      ]),
      titledItems(artifact.cuts),
    ].filter(Boolean);
  }
  if (name === "render_report") {
    return [
      reviewFacts([
        reviewFact("outputs", Array.isArray(artifact.outputs) ? artifact.outputs.length : null),
        reviewFact("duration", artifact.duration_seconds != null ? fmtDuration(artifact.duration_seconds) : null),
      ]),
      titledItems(artifact.outputs),
    ].filter(Boolean);
  }
  if (name === "publish_log") {
    return [
      reviewFacts([reviewFact("destinations", Array.isArray(artifact.entries) ? artifact.entries.length : null)]),
      titledItems((artifact.entries || []).map((entry) => ({
        title: entry.platform || entry.destination || "Publish destination",
        description: [entry.status, entry.url].filter(Boolean).join(" · "),
      }))),
    ].filter(Boolean);
  }
  return genericArtifactSummary(artifact);
}

function artifactReviewTitle(name, artifact, s) {
  if (name === "proposal_packet") {
    const selected = (artifact.selected_concept || {}).concept_id;
    const concept = (artifact.concept_options || []).find((item) => item.id === selected);
    return (concept && concept.title) || "Production proposal";
  }
  if (name === "research_brief") return artifact.topic || "Research brief";
  if (name === "scene_plan") return "Scene plan";
  if (name === "asset_manifest") return "Generated assets";
  if (name === "edit_decisions") return "Edit decisions";
  if (name === "render_report") return "Render report";
  if (name === "publish_log") return "Publish plan";
  return artifact.title || artifact.name || s.title;
}

function renderApprovalReview(s) {
  const awaiting = s.stages.find((item) => item.status === "awaiting_human");
  if (!awaiting) return null;

  const names = artifactNamesForStage(awaiting);
  const entries = names
    .filter((name) => name !== "decision_log")
    .map((name) => [name, s.artifacts[name]])
    .filter(([, artifact]) => artifact && typeof artifact === "object");
  const stageIndex = s.stages.findIndex((item) => item.name === awaiting.name);
  const nextStage = stageIndex >= 0 ? s.stages[stageIndex + 1] : null;
  const review = awaiting.review || {};
  const reviewSummary = reviewSummaryText(review);

  const artifacts = entries.map(([name, artifact]) => el("article", {
    class: "approval-artifact",
    "data-artifact": name,
  },
    el("div", { class: "approval-artifact-kicker" }, humanize(name)),
    el("h2", {}, artifactReviewTitle(name, artifact, s)),
    ...artifactReviewContent(name, artifact),
  ));

  if (!artifacts.length) {
    artifacts.push(el("div", { class: "approval-missing", role: "alert" },
      el("b", {}, "Nothing reviewable was found. "),
      names.length
        ? `The ${awaiting.name} checkpoint declares ${names.map(humanize).join(", ")}, but Backlot could not load it.`
        : `The ${awaiting.name} checkpoint does not declare an artifact.`,
    ));
  }

  return el("section", { class: "approval-review", "data-stage": awaiting.name },
    el("div", { class: "approval-review-head" },
      el("div", {},
        el("div", { class: "approval-eyebrow" }, "REVIEW GATE"),
        el("h2", {}, `${humanize(awaiting.name)} is ready for your review`),
        el("p", {}, "Review the artifact here, then reply in chat to approve it or request changes."),
      ),
      el("span", { class: "approval-status" }, "PENDING APPROVAL"),
    ),
    reviewSummary ? el("div", { class: "approval-review-note" },
      el("b", {}, "SELF-REVIEW  "), shortText(reviewSummary, 260)) : null,
    el("div", { class: "approval-artifacts" }, artifacts),
    el("div", { class: "approval-review-foot" },
      el("span", {}, nextStage
        ? `Approval unlocks ${humanize(nextStage.name)}.`
        : "This is the final approval gate."),
      el("button", { type: "button", onclick: () => toggleDrawer(awaiting.name) }, "OPEN FULL ARTIFACT"),
    ),
  );
}

// The script & scene-plan reading views render full and inline (reading.css),
// so the old expand/narration modal is retired. The <audio id="player"> element
// in board.html is still used for in-card narration playback.

// ---------------------------------------------------------------------------
// right rail: decisions, activity
// ---------------------------------------------------------------------------

function renderDecisions(s) {
  const log = s.artifacts.decision_log;
  const decisions = (log && log.decisions) || [];
  if (!decisions.length) return null;
  const body = el("div", { class: "panel-body" });
  // Collapse by category+subject: a decision that changed mid-run (e.g. voice
  // openai_onyx → chirp3) is superseded by the later entry — show the CURRENT
  // choice, not the first one recorded, and mark that it was revised.
  const current = new Map();
  decisions.forEach((d, i) => {
    const key = `${d.category || "decision"}::${d.subject || ""}`;
    const prev = current.get(key);
    current.set(key, { d, order: i, revised: prev ? prev.revised + 1 : 0 });
  });
  const shown = [...current.values()].sort((a, b) => b.order - a.order).slice(0, 8);
  for (const { d, revised } of shown) {
    const selLabel = (() => {
      // Prefer the human label of the selected option over its bare id.
      const opt = (d.options_considered || []).find((o) => (o.option_id ?? o.label) === d.selected);
      return (opt && opt.label) || d.selected || "";
    })();
    const alts = (d.options_considered || [])
      .filter((o) => (o.option_id ?? o.label) !== d.selected && (o.option_id || o.label));
    body.append(el("div", { class: "decision" },
      el("div", { class: "d-cat" }, `${d.category || "decision"}${d.confidence ? ` · ${d.confidence}` : ""}`,
        revised ? el("span", { class: "d-revised" }, " · revised") : null),
      el("div", { class: "d-pick" }, `${d.subject || ""} `, el("span", { class: "arrow" }, "→"), ` ${selLabel}`),
      d.reason ? el("div", { class: "d-why" }, d.reason) : null,
      alts.length ? el("div", { class: "d-alt" }, "also considered: ",
        alts.slice(0, 3).map((o, i) => [i ? " · " : "", el("s", {}, o.label || o.option_id)]).flat()) : null,
    ));
  }
  return el("div", { class: "panel" },
    el("div", { class: "panel-head" }, el("h2", {}, "Decisions"), el("span", { class: "meta" }, "decision_log.json")),
    body);
}

function renderActivity(s) {
  const events = s.events || [];
  if (!events.length) return null;
  const body = el("div", { class: "panel-body" });
  // A start is "running" only until a later finish/error for the same
  // tool+scene closes it — closed starts are dropped (the finish row tells
  // the story), unmatched starts render as live. Counted (not keyed-single)
  // so parallel runs of the same tool on the same scene stay visible.
  const open = new Map(); // key -> {count, ev}
  const rows = [];
  for (const ev of events) {
    const key = `${ev.tool}:${ev.scene_id || ""}`;
    if (ev.event === "start") {
      const slot = open.get(key) || { count: 0, ev };
      slot.count += 1;
      slot.ev = ev;
      open.set(key, slot);
    } else {
      const slot = open.get(key);
      if (slot) {
        slot.count -= 1;
        if (slot.count <= 0) open.delete(key);
      }
      rows.push(ev);
    }
  }
  for (const slot of open.values()) rows.push(slot.ev);
  rows.sort((a, b) => String(a.ts).localeCompare(String(b.ts)));
  for (const ev of rows.slice(-10).reverse()) {
    let statusEl;
    if (ev.event === "finish") {
      statusEl = el("span", { class: `status ${ev.success === false ? "err" : "ok"}` },
        `${ev.success === false ? "✕" : "✓"}${ev.duration_s != null ? ` ${ev.duration_s.toFixed ? ev.duration_s.toFixed(1) : ev.duration_s}s` : ""}${ev.cost_usd ? ` ${fmtMoney(ev.cost_usd)}` : ""}`);
    } else if (ev.event === "error") {
      statusEl = el("span", { class: "status err" }, "✕");
    } else {
      statusEl = el("span", { class: "status run" }, "● running");
    }
    body.append(el("div", { class: "act-row" },
      el("span", { class: "t" }, fmtClock(ev.ts)),
      el("span", { class: "tool" }, ev.tool || ""),
      el("span", { class: "target" }, ev.scene_id || ""),
      statusEl,
    ));
  }
  return el("div", { class: "panel" },
    el("div", { class: "panel-head" }, el("h2", {}, "Activity"), el("span", { class: "meta" }, "events.jsonl")),
    body);
}

// ---------------------------------------------------------------------------
// storyboard filmstrip
// ---------------------------------------------------------------------------

function sceneLabel(id) {
  // "sc4" → "SC 04", "scene-11" → "SC 11", anything else → uppercased id
  const m = String(id).match(/(\d+)\s*$/);
  if (m) return `SC ${m[1].padStart(2, "0")}`;
  return String(id).toUpperCase().slice(0, 10);
}

function sceneTypeLabel(t) { return TYPE_LABELS[t] || (t ? String(t).replaceAll("_", " ") : ""); }

function buildSceneTimeline(scenes) {
  const total = scenes.reduce((m, c) => Math.max(m, Number(c.end_seconds) || 0), 0);
  const box = el("div", { class: "timeline-box" },
    el("div", { class: "tl-label" }, `Timeline · 0s → ${Math.round(total)}s`));
  const tl = el("div", { class: "timeline" });
  scenes.forEach((c) => {
    const dur = Math.max(0.001, (Number(c.end_seconds) || 0) - (Number(c.start_seconds) || 0));
    const seg = el("div", {
      class: `seg t-${c.type}${c.hero_moment ? " hero" : ""}`,
      title: `${c.id || ""} · ${c.start_seconds}–${c.end_seconds}s · ${c.type || ""}${c.hero_moment ? " · HERO" : ""}`,
    });
    seg.style.flexGrow = String(dur);
    seg.textContent = String(c.id || "").toUpperCase().replace(/^SC/i, "");
    tl.append(seg);
  });
  box.append(tl, buildAxis(total));
  const types = [...new Set(scenes.map((c) => c.type).filter(Boolean))];
  const legend = el("div", { class: "legend" },
    ...types.map((t) => el("span", {},
      el("i", { class: "dot", style: `background:${TYPE_COLORS[t] || "#999"}` }), sceneTypeLabel(t))),
    el("span", {}, el("i", { class: "dot hero", style: "background:var(--r-gold)" }), "⭐ hero moment"));
  box.append(legend);
  return box;
}

// Live media slot (warm-styled): image / video / generating / missing.
// `media` is the storyboard-join card (carries visual/takes/audio/generating);
// `scene` is the raw scene_plan scene (carries required_assets for the fallback).
function sceneMedia(s, media, scene) {
  if (!media) return null;
  if (media.generating) {
    return el("div", { class: "r-media generating" },
      el("div", { class: "shimmer" }),
      el("div", { class: "gen-label" },
        el("span", {}, "◉ GENERATING"),
        el("small", {}, media.generating_tool || "")));
  }
  const v = media.visual;
  if (v && v.exists) {
    const badge = [v.model || v.source_tool, v.cost_usd != null ? fmtMoney(v.cost_usd) : null,
      v.quality_score != null ? `q ${v.quality_score}` : null].filter(Boolean).join(" · ");
    if (v.type === "video") {
      const m = el("div", { class: "r-media has-video" },
        el("video", {
          src: mediaURL(s.project_id, v.path), preload: "metadata", muted: "", playsinline: "",
          "data-poster-src": thumbURL(s.project_id, v.path, 640),
        }),
        el("span", { class: "play" }, "▶"),
        v.snapshot ? el("span", { class: "badge" }, "snapshot") : (badge ? el("span", { class: "badge" }, badge) : null));
      m.onclick = () => { const vid = m.querySelector("video"); if (vid.paused) vid.play(); else vid.pause(); };
      return m;
    }
    const img = el("img", { src: thumbURL(s.project_id, v.path, 640), loading: "lazy", alt: "" });
    img.onerror = () => { if (img.parentElement) img.parentElement.classList.add("missing"); };
    return el("div", { class: "r-media" }, img,
      v.snapshot ? el("span", { class: "badge" }, "snapshot") : (badge ? el("span", { class: "badge" }, badge) : null));
  }
  if (v && !v.exists) {
    return el("div", { class: "r-media missing" },
      el("div", { class: "miss-in" },
        el("span", { class: "miss-ic" }, "⚑"),
        el("span", {}, "asset in manifest, file missing"),
        el("span", { style: "font-size:11px;color:var(--r-muted)" }, v.path || "")));
  }
  const genReqs = (scene.required_assets || []).filter((a) => !a.source || a.source === "generate");
  if (genReqs.length) {
    return el("div", { class: "r-media missing" },
      el("div", { class: "miss-in" },
        el("span", { class: "miss-ic" }, "🔒"),
        el("span", {}, shortText(genReqs[0].description || "image generation needed", 90))));
  }
  return null;
}

function assetBox(kind, ico, label, txt) {
  return el("div", { class: `asset ${kind}` },
    el("span", { class: "ico" }, ico),
    el("div", {},
      el("span", { class: "alabel" }, label),
      txt ? el("span", { class: "txt" }, txt) : null));
}
// Map required_assets (+ metadata.blocked_assets) to the reference ok/blocked boxes.
function sceneAssetBoxes(scene, ctx) {
  const reqs = scene.required_assets || [];
  const genReqs = reqs.filter((a) => !a.source || a.source === "generate");
  const otherReqs = reqs.filter((a) => a.source && a.source !== "generate");
  const boxes = [];
  const blockedScene = ctx.blockedScenes && ctx.blockedScenes.has(String(scene.id));
  if (genReqs.length || blockedScene) {
    if (genReqs.length) {
      for (const r of genReqs) boxes.push(assetBox("blocked", "🔒", "이미지/자산 생성 필요", r.description || ""));
    } else {
      boxes.push(assetBox("blocked", "🔒", "자산 생성 필요", (ctx.blockedMeta && ctx.blockedMeta.reason) || ""));
    }
  } else {
    const zeroText = ["text_card", "animation", "transition"].includes(scene.type)
      ? "zero-key · 무생성 렌더 가능"
      : "자산 불필요";
    boxes.push(assetBox("ok", "✅", zeroText,
      scene.shot_intent ? shortText(scene.shot_intent, 90) : ""));
  }
  for (const r of otherReqs) boxes.push(assetBox("ok", "✅", `${r.source} 자산`, r.description || ""));
  return el("div", { class: "assets" }, ...boxes);
}

function sceneReadingCard(s, scene, media, ctx) {
  const type = scene.type || "";
  const isHero = !!scene.hero_moment;
  const isSample = !!(ctx.sampleId && scene.script_section_id === ctx.sampleId);
  const card = el("div", { class: `card t-${type}${isHero ? " hero" : ""}${isSample ? " sample" : ""}` });

  card.append(el("div", { class: "card-head" },
    el("span", { class: "sc-id" }, sceneLabel(scene.id)),
    el("span", { class: `type-chip ${type}` }, sceneTypeLabel(type)),
    scene.narrative_role ? el("span", { class: "role" }, String(scene.narrative_role).replaceAll("_", " ")) : null,
    isHero ? el("span", { class: "hero-badge" }, "⭐ Hero") : null,
    el("span", { class: "time" }, `${scene.start_seconds}–${scene.end_seconds}s`)));

  if (scene.description) card.append(el("p", { class: "desc" }, scene.description));
  if (scene.shot_intent) card.append(el("p", { class: "intent" }, el("b", {}, "의도: "), scene.shot_intent));

  const sl = scene.shot_language || {};
  const shotParts = [sl.shot_size, sl.camera_movement, sl.lens_mm ? `${sl.lens_mm}mm` : null,
    sl.lighting_key, sl.depth_of_field ? `${sl.depth_of_field} DoF` : null, sl.color_temperature]
    .filter(Boolean).map((t) => String(t).replaceAll("_", " "));
  if (shotParts.length) card.append(el("div", { class: "shot" }, ...shotParts.map((t) => el("span", {}, t))));

  const body = el("div", { class: "scene-body" });
  const mediaEl = sceneMedia(s, media, scene);
  if (mediaEl) body.append(mediaEl);
  body.append(sceneAssetBoxes(scene, ctx));

  if (media && media.takes && media.takes.length > 1) {
    const takes = el("div", { class: "rtakes" });
    media.takes.forEach((t, i) => {
      const isActive = media.visual && (t === media.visual
        || (t.path && t.path === media.visual.path) || (t.id && t.id === media.visual.id));
      const tk = el("span", { class: `tk${isActive ? " active" : ""}`, title: `take ${i + 1}` });
      if (t.exists && t.type === "image") tk.append(el("img", { src: thumbURL(s.project_id, t.path, 320), loading: "lazy", alt: "" }));
      takes.append(tk);
    });
    takes.append(el("span", { class: "tk-label" }, `${media.takes.length} TAKES`));
    body.append(takes);
  }

  if (media && media.narration) body.append(el("div", { class: "note", style: "margin-top:12px" }, media.narration));
  if (media) {
    const narrAudio = (media.audio || []).find((a) => a.exists && (a.type === "narration" || a.type === "audio"));
    if (narrAudio) {
      const wave = el("div", { class: "r-wave", title: "Play narration" });
      waveBars(wave, (media.id || "") + (narrAudio.path || ""));
      wave.append(el("span", { class: "wv-time" }, narrAudio.duration_seconds ? `${narrAudio.duration_seconds}s` : "♪"));
      wave.onclick = () => { player.src = mediaURL(s.project_id, narrAudio.path); player.play(); };
      body.append(wave);
    }
  }

  if (body.childNodes.length) card.append(body);
  return card;
}

function sceneAssetsSummary(scenes, blockedMeta) {
  if (blockedMeta && blockedMeta.scenes && blockedMeta.scenes.length) {
    const sum = el("div", { class: "summary" },
      el("h2", {}, `🔒 assets 단계 — ${blockedMeta.scenes.length}개 씬에 자산 생성 필요`));
    if (blockedMeta.zero_key_feasible) sum.append(el("p", {}, blockedMeta.zero_key_feasible));
    if (blockedMeta.reason) sum.append(el("p", {}, blockedMeta.reason));
    if (blockedMeta.unblock_options && blockedMeta.unblock_options.length) {
      sum.append(el("div", { class: "unlock" },
        ...blockedMeta.unblock_options.map((o) => el("span", {}, o))));
    }
    return sum;
  }
  const genScenes = scenes.filter((sc) => (sc.required_assets || []).some((a) => !a.source || a.source === "generate"));
  if (!genScenes.length) return null;
  return el("div", { class: "summary" },
    el("h2", {}, `🔒 assets 단계 — ${genScenes.length}개 씬에 자산 생성 필요`),
    el("p", {}, `${scenes.length}씬 중 ${scenes.length - genScenes.length}씬은 zero-key — 외부 자산 없이 렌더 가능합니다.`));
}

function renderStoryboard(s) {
  const board = s.storyboard;
  const planArtifact = s.artifacts.scene_plan || {};
  const planScenes = planArtifact.scenes || [];
  // Prefer the rich scene_plan scenes for layout; join live media from the
  // storyboard by id. If no scene_plan artifact, fall back to the board cards.
  const sourceScenes = planScenes.length ? planScenes : (board ? board.scenes : []);
  if (!sourceScenes || !sourceScenes.length) return null;

  const meta = planArtifact.metadata || {};
  const scriptMeta = (s.artifacts.script && s.artifacts.script.metadata) || {};
  const lang = scriptMeta.language || "en";
  const sampleId = (s.artifacts.script && s.artifacts.script.voice_performance || {}).sample_section_id;
  const mediaById = new Map((board && board.scenes ? board.scenes : []).map((c) => [String(c.id), c]));
  const total = board && board.total_duration_seconds
    || sourceScenes.reduce((m, c) => Math.max(m, Number(c.end_seconds) || 0), 0);

  const root = el("section", { class: "reading reading-scene" });
  root.append(el("div", { class: "r-toolbar" },
    el("button", {
      class: "r-btn primary", type: "button", title: "이 스토리보드를 HTML로 다운로드",
      onclick: () => downloadReading(root, `${slug(s.project_id)}-scene-plan.html`, s.title, lang),
    }, "↓ HTML 다운로드")));

  root.append(el("div", { class: "eyebrow" }, "Scene Plan · Storyboard"));
  root.append(el("h1", {}, s.title));
  const typesUsed = [...new Set(sourceScenes.map((c) => c.type).filter(Boolean))];
  const subParts = [planArtifact.style_playbook, `${sourceScenes.length}씬`,
    s.pipeline.pipeline_type && s.pipeline.pipeline_type !== "unknown" ? s.pipeline.pipeline_type : null].filter(Boolean);
  if (subParts.length) root.append(el("p", { class: "subtitle" }, subParts.join(" · ")));

  const chips = [
    total ? el("span", { class: "rchip accent" }, `${Math.round(total)}초`) : null,
    el("span", { class: "rchip" }, `${sourceScenes.length}씬`),
    planArtifact.style_playbook ? el("span", { class: "rchip" }, planArtifact.style_playbook) : null,
    s.pipeline.pipeline_type && s.pipeline.pipeline_type !== "unknown"
      ? el("span", { class: "rchip" }, `${s.pipeline.pipeline_type} pipeline`) : null,
    typesUsed.length ? el("span", { class: "rchip" }, typesUsed.map(sceneTypeLabel).join(" · ")) : null,
  ].filter(Boolean);
  if (chips.length) root.append(el("div", { class: "meta" }, ...chips));

  root.append(buildSceneTimeline(sourceScenes));

  const blockedMeta = meta.blocked_assets || {};
  const ctx = {
    blockedScenes: new Set((blockedMeta.scenes || []).map((x) => String(x))),
    blockedMeta,
    sampleId,
  };
  const scenesEl = el("div", { class: "scenes" });
  sourceScenes.forEach((scene) => {
    scenesEl.append(sceneReadingCard(s, scene, mediaById.get(String(scene.id)), ctx));
  });
  root.append(scenesEl);

  const summary = sceneAssetsSummary(sourceScenes, blockedMeta);
  if (summary) root.append(summary);

  const lastDesc = sourceScenes.length ? sourceScenes[sourceScenes.length - 1].description : "";
  if (lastDesc) root.append(el("div", { class: "closer" }, `"${shortText(lastDesc, 140)}"`));

  root.append(buildReadingFooter(s, `projects/${s.project_id}/artifacts/scene_plan.json`, [
    planArtifact.style_playbook ? `스타일: ${planArtifact.style_playbook}` : null,
    `${sourceScenes.length}씬`,
  ]));
  return root;
}

// ---------------------------------------------------------------------------
// renders + degraded media
// ---------------------------------------------------------------------------

function renderRenders(s) {
  const renders = s.media.renders;
  if (!renders.length) return null;
  if (activeRender >= renders.length) activeRender = 0;
  const current = renders[activeRender];
  // Full re-renders (every SSE refresh) must not reset an in-progress
  // watch: carry playback position/state over to the recreated element.
  const prev = document.querySelector(".render-hero video");
  const src = mediaURL(s.project_id, current.path);
  // preload="metadata" gives the element its intrinsic aspect ratio (and a
  // poster frame) before playback — without it a portrait 9:16 render sits
  // in a letterboxed 100%-wide black box that reads as landscape.
  const video = el("video", { src, controls: "", preload: "metadata" });
  // Click the frame to start playback (controls handle pause/scrub) — the
  // big player was inert to a click on the picture itself.
  video.addEventListener("click", () => { if (video.paused) video.play().catch(() => {}); });
  if (prev && prev.getAttribute("src") === src && (prev.currentTime > 0 || !prev.paused)) {
    const t = prev.currentTime;
    const wasPlaying = !prev.paused && !prev.ended;
    video.addEventListener("loadedmetadata", () => { video.currentTime = t; }, { once: true });
    video.setAttribute("preload", "metadata");
    if (wasPlaying) video.autoplay = true;
  }
  const versions = el("div", { class: "render-meta" },
    renders.map((r, i) => el("span", {
      class: `v${i === activeRender ? " active" : ""}`,
      onclick: () => { activeRender = i; render(); },
    }, `${r.path.split("/").pop()}${r.at_root ? " · root" : ""}`)),
    el("span", { style: "margin-left:auto" }, `${(current.size / 1048576).toFixed(1)} MB`),
  );
  return el("div", {},
    el("div", { class: "section-title" }, "Renders",
      el("span", { class: "meta" }, `${renders.length} version${renders.length === 1 ? "" : "s"}`)),
    el("div", { class: "render-hero" }, video),
    versions);
}

function renderFoundMedia(s) {
  // Degraded view: show discovered snapshots when there's no storyboard.
  if (s.storyboard || !s.media.snapshots.length) return null;
  const grid = el("div", { class: "found-grid" });
  for (const snap of s.media.snapshots.slice(0, 12)) {
    grid.append(el("div", { class: "thumb" },
      el("img", { src: thumbURL(s.project_id, snap.path, 640), loading: "lazy", alt: "" })));
  }
  return el("div", {},
    el("div", { class: "section-title" }, "What the watcher found",
      el("span", { class: "meta" }, "snapshots / verification frames")),
    grid);
}

function renderNoState(s) {
  if (s.has_pipeline_state) return null;
  return el("div", { class: "notice", style: "border-color:#2b2b33;background:var(--surface-2);color:var(--text-3)" },
    el("span", { style: "font-size:calc(15px * var(--fs-scale))" }, "◌"),
    el("span", {},
      el("b", { style: "color:var(--text-2)" }, "No pipeline state. "),
      "This project has no checkpoints — Backlot is showing what it found on disk. ",
      "Runs that follow the checkpoint protocol get the full board."));
}

function renderAwaitingNotice(s) {
  const awaiting = s.stages.find((x) => x.status === "awaiting_human");
  if (!awaiting) return null;
  return el("div", { class: "notice" },
    el("span", { style: "font-size:calc(16px * var(--fs-scale))" }, "◈"),
    el("span", {},
      el("b", {}, `The ${awaiting.name} stage is waiting for your review. `),
      "The agent is paused at this gate — reply ", el("b", {}, "in chat"), " to approve or request changes."));
}

// ---------------------------------------------------------------------------
// replay — scrub a completed run from its timestamps
// ---------------------------------------------------------------------------

// Python writers emit tz-aware UTC isoformat, but treat tz-naive strings as
// UTC too — mixing local-parsed and UTC-parsed timestamps would skew replay
// ordering by the user's UTC offset.
const ts = (iso) => {
  if (!iso) return null;
  let s = String(iso);
  if (!/(Z|[+-]\d{2}:?\d{2})$/.test(s)) s += "Z";
  const t = Date.parse(s);
  return Number.isFinite(t) ? t : null;
};

function replayBounds(s) {
  const moments = [];
  for (const st of s.stages) {
    for (const h of st.history_entries || []) {
      const t = ts(h.timestamp);
      if (t) moments.push(t);
    }
  }
  for (const ev of s.events || []) {
    const t = ts(ev.ts);
    if (t) moments.push(t);
  }
  if (moments.length < 2) return null;
  return { t0: Math.min(...moments), t1: Math.max(...moments) };
}

function stateAt(s, T) {
  const view = structuredClone(s);
  for (const st of view.stages) {
    const past = (st.history_entries || []).filter((h) => ts(h.timestamp) != null && ts(h.timestamp) <= T);
    if (!past.length) {
      st.status = "pending"; st.review = null; st.timestamp = null;
      st.gate_skipped = false; st.partial_progress = null;
    } else {
      const cur = past[past.length - 1];
      st.status = cur.status || "pending";
      st.timestamp = cur.timestamp;
    }
  }
  view.events = (view.events || []).filter((ev) => ts(ev.ts) != null && ts(ev.ts) <= T);

  // Storyboard: visuals appear as their scene finishes (events) or when the
  // assets stage has completed as of T (legacy runs without events).
  if (view.storyboard) {
    const assetsStage = view.stages.find((x) => x.name === "assets");
    const assetsDone = assetsStage && assetsStage.status === "completed";
    const finished = new Set();
    const startedNow = new Map();
    for (const ev of view.events) {
      if (!ev.scene_id) continue;
      if (ev.event === "finish") { finished.add(ev.scene_id); startedNow.delete(ev.scene_id); }
      else if (ev.event === "start") startedNow.set(ev.scene_id, ev);
      else if (ev.event === "error") startedNow.delete(ev.scene_id);
    }
    const scenePlanStage = view.stages.find((x) => x.name === "scene_plan");
    const scenePlanDone = scenePlanStage && ["completed", "awaiting_human"].includes(scenePlanStage.status);
    if (!scenePlanDone) {
      view.storyboard = null;
    } else {
      for (const card of view.storyboard.scenes) {
        const visible = assetsDone || finished.has(card.id);
        if (!visible) { card.visual = null; card.takes = []; card.audio = []; }
        card.generating = startedNow.has(card.id);
        card.generating_tool = (startedNow.get(card.id) || {}).tool;
      }
    }
  }
  // Final artifacts hide until their stage happened — for every project
  // shape, storyboard or not (a degraded run must not show the finished
  // movie before its stages ran).
  const scriptStage = view.stages.find((x) => x.name === "script");
  if (!(scriptStage && ["completed", "awaiting_human"].includes(scriptStage.status))) {
    delete view.artifacts.script;
  }
  const composeStage = view.stages.find((x) => x.name === "compose");
  if (!(composeStage && composeStage.status === "completed")) {
    view.media.renders = [];
  }
  return view;
}

function renderReplayBar(s) {
  const bounds = replayBounds(s);
  if (!bounds) return null;
  if (!replay) {
    // collapsed: just the entry button
    return el("div", { class: "replay-bar", style: "justify-content:flex-end" },
      el("span", { class: "rp-time" }, "scrub the whole run"),
      el("span", { class: "rp-btn", onclick: startReplay }, "▶ REPLAY RUN"));
  }
  const pos = (replay.t - replay.t0) / Math.max(1, replay.t1 - replay.t0);
  const timeLabel = el("span", { class: "rp-time" },
    new Date(replay.t).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit", second: "2-digit" }));
  const setT = (value) => {
    replay.t = replay.t0 + (Number(value) / 1000) * (replay.t1 - replay.t0);
    timeLabel.textContent = new Date(replay.t)
      .toLocaleTimeString([], { hour: "2-digit", minute: "2-digit", second: "2-digit" });
  };
  return el("div", { class: "replay-bar" },
    el("span", { class: "rp-btn", onclick: toggleReplayPlay }, replay.playing ? "❚❚" : "▶"),
    el("input", {
      type: "range", min: "0", max: "1000", value: String(Math.round(pos * 1000)),
      // A full render() would destroy this slider mid-drag: while dragging,
      // only pause + track the time label; re-render the board on release.
      onpointerdown: () => { replay.playing = false; },
      oninput: (e) => setT(e.target.value),
      onchange: (e) => { setT(e.target.value); render(); },
    }),
    timeLabel,
    el("span", { class: "rp-btn", onclick: stopReplay }, "✕ LIVE"),
  );
}

let replayTimer = null;

function startReplay() {
  const bounds = replayBounds(state);
  if (!bounds) return;
  replay = { ...bounds, t: bounds.t0, playing: true };
  document.body.classList.add("replaying");
  scheduleTick();
  render();
}

function stopReplay() {
  replay = null;
  clearTimeout(replayTimer);
  document.body.classList.remove("replaying");
  render();
}

function toggleReplayPlay() {
  if (!replay) return;
  replay.playing = !replay.playing;
  if (replay.playing) scheduleTick();
  render();
}

function scheduleTick() {
  // Single pending tick, ever — rapid pause/play must not stack chains.
  clearTimeout(replayTimer);
  replayTimer = setTimeout(tickReplay, 100);
}

function tickReplay() {
  if (!replay || !replay.playing) return;
  // A full run replays in ~20 seconds regardless of real duration
  // (10 renders/second — full re-render per tick, keep it modest).
  const step = (replay.t1 - replay.t0) / 200;
  replay.t = Math.min(replay.t1, replay.t + step);
  if (replay.t >= replay.t1) replay.playing = false;
  render();
  if (replay.playing) scheduleTick();
}

// ---------------------------------------------------------------------------
// page assembly
// ---------------------------------------------------------------------------

function render() {
  if (!state) return;
  const s = replay ? stateAt(state, replay.t) : state;
  document.title = `Backlot — ${s.title}`;
  document.body.classList.toggle("first", firstPaint);
  firstPaint = false;
  app.innerHTML = "";
  app.append(renderSlate(s));
  app.append(renderRail(s));
  const replayBar = renderReplayBar(state);
  if (replayBar) app.append(replayBar);
  const drawer = renderDrawer(s);
  if (drawer) app.append(drawer);
  const awaitingNotice = renderAwaitingNotice(s);
  if (awaitingNotice) app.append(awaitingNotice);
  const noState = renderNoState(s);
  if (noState) app.append(noState);

  const main = el("div", { class: "main-col" });
  const approvalReview = renderApprovalReview(s);
  if (approvalReview) main.append(approvalReview);
  const aside = el("aside", {});
  const decisions = renderDecisions(s);
  const activity = renderActivity(s);
  if (decisions) aside.append(decisions);
  if (activity) aside.append(activity);

  // Media sections live INSIDE the main column so a tall decisions rail
  // never pushes them below the fold — the column flows beside the rail.
  // The script & scene-plan reading docs are NOT rendered inline — click the
  // stage in the rail to open its warm-paper reading view in the drawer.
  const found = renderFoundMedia(s);
  const renders = renderRenders(s);

  if (approvalReview || decisions || activity) {
    for (const section of [found, renders]) {
      if (section) main.append(section);
    }
    const hasAside = Boolean(decisions || activity);
    app.append(el("div", { class: `board${hasAside ? "" : " solo"}` }, main, hasAside ? aside : null));
  } else {
    for (const section of [found, renders]) {
      if (section) app.append(section);
    }
  }
}

// Defensive normalization (F-02): the server contract guarantees these
// fields, but a sparse/legacy payload must degrade, never crash the board.
function normalize(s) {
  s.pipeline = s.pipeline || { pipeline_type: "unknown", stages: [], known: false };
  s.stages = Array.isArray(s.stages) ? s.stages : [];
  for (const stage of s.stages) {
    stage.produces = Array.isArray(stage.produces) ? stage.produces : [];
  }
  s.artifacts = s.artifacts || {};
  s.media = s.media || {};
  s.media.renders = Array.isArray(s.media.renders) ? s.media.renders : [];
  s.media.snapshots = Array.isArray(s.media.snapshots) ? s.media.snapshots : [];
  s.media.music = Array.isArray(s.media.music) ? s.media.music : [];
  s.events = Array.isArray(s.events) ? s.events : [];
  if (s.storyboard && Array.isArray(s.storyboard.scenes)) {
    for (const c of s.storyboard.scenes) {
      c.takes = Array.isArray(c.takes) ? c.takes : [];
      c.audio = Array.isArray(c.audio) ? c.audio : [];
      c.required_assets = Array.isArray(c.required_assets) ? c.required_assets : [];
    }
  } else {
    s.storyboard = null;
  }
  return s;
}

async function refresh() {
  state = normalize(await getJSON(`/api/project/${encodeURIComponent(projectId)}/state`));
  render();
}

refresh().catch((err) => {
  app.innerHTML = "";
  app.append(el("div", { class: "empty", style: "margin-top:80px" },
    el("div", { class: "big" }, "PROJECT NOT FOUND"),
    el("div", {}, String(err))));
});
// ?static=1 disables the live feed (screenshots, static exports).
if (!new URLSearchParams(location.search).has("static")) {
  subscribe(`/api/project/${encodeURIComponent(projectId)}/events`, () => refresh().catch(console.error));
}
