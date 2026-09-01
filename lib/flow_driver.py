"""Drive Google Flow through Playwright, attached to the user's own Chrome.

Google Flow has no public API for generation — Veo and Omni are reachable only
through the web UI, which is a React app that ignores synthesized input. So this
attaches over CDP to a real Chrome the user is signed into, and drives it with
genuinely trusted keyboard and mouse events.

Two things happen over Flow's own HTTP API instead of through the UI, because
the UI path for them is far more fragile: uploading a reference image (the
response hands back the exact media id, instead of hunting for a filename in a
picker) and downloading the finished clip. Both run *inside the page* via
`page.evaluate`, so they carry the browser's real session and TLS fingerprint —
a Python HTTP client hitting the same endpoints presents neither, which is a
fast route to a flagged account.

Starting a generation stays in the UI on purpose. That call is gated behind a
reCAPTCHA Enterprise token, and the only legitimate source of one is the app
itself reacting to real interaction.

Chrome must be started with `--remote-debugging-port` AND a non-default
`--user-data-dir`; since Chrome 136 the flag is ignored on the default profile.
"""

from __future__ import annotations

import base64
import json
import random
import re
import time
from pathlib import Path
from typing import Any, Optional

DEFAULT_CDP = "http://127.0.0.1:9222"
FLOW_HOME = "https://labs.google/fx/tools/flow"
FLOW_PATH = re.compile(r"^/fx/(?:[a-z]{2}(?:-[A-Za-z]{2})?/)?tools/flow")

# A 200 with a tiny body is Flow's "not rendered yet" answer, not a video.
MIN_VIDEO_BYTES = 100_000

ASPECT_ID = {
    "16:9": "LANDSCAPE", "9:16": "PORTRAIT", "1:1": "SQUARE",
    "3:4": "PORTRAIT_3_4", "4:3": "LANDSCAPE_4_3",
}

# Flow re-shows these on every navigation into a project — Google does not
# persist the acknowledgement — and they swallow pointer events while up.
MODAL_MARKERS = ["privacy policy", "your data and google flow", "shape ai tools",
                 "quyền cần thiết", "chính sách quyền riêng tư", "dữ liệu của bạn"]
MODAL_ACCEPT = ["Accept", "I accept", "I agree", "Agree", "Continue", "Next", "Got it",
                "Chấp nhận", "Tôi chấp nhận", "Đồng ý", "Tiếp tục", "Tiếp theo", "Đã hiểu"]
NEW_PROJECT = ["New project", "Dự án mới"]
DECLINE_AGENT = ["No thanks", "No, thanks", "Không, cảm ơn"]
START_SLOT = ["Bắt đầu", "Start"]
ADD_TO_PROMPT = ["Thêm vào câu lệnh", "Add to prompt"]
UPLOADS_TAB = ["Tệp tải lên", "Uploads", "Tải lên"]

MODEL_RE = re.compile(r"(veo|omni)[\s\d.]*[-–]?\s*(\w+)?", re.I)


class FlowError(RuntimeError):
    """A step failed. The message always names the step that failed."""


class FlowDriver:
    """One Flow session. Use as a context manager."""

    def __init__(self, cdp_url: str = DEFAULT_CDP, project_url: Optional[str] = None):
        self.cdp_url = cdp_url
        self.project_url = project_url
        self._pw = None
        self._browser = None
        self.page = None

    # ----------------------------------------------------------- lifecycle

    def __enter__(self) -> "FlowDriver":
        from playwright.sync_api import sync_playwright

        self._pw = sync_playwright().start()
        try:
            self._browser = self._pw.chromium.connect_over_cdp(self.cdp_url)
        except Exception as exc:
            self._pw.stop()
            raise FlowError(
                f"connect: no Chrome listening on {self.cdp_url}. Start it with\n"
                f'  chrome.exe --remote-debugging-port=9222 --user-data-dir="<a dedicated dir>"\n'
                f"(since Chrome 136 the port is ignored on the default profile.)\n"
                f"Underlying error: {exc}"
            ) from exc
        self.page = self._find_flow_page()
        return self

    def __exit__(self, *exc_info) -> None:
        # Only detach. The browser is the user's — never close their window.
        try:
            if self._browser:
                self._browser.close()
        finally:
            if self._pw:
                self._pw.stop()

    def _find_flow_page(self):
        pages = [p for ctx in self._browser.contexts for p in ctx.pages]
        if not pages:
            raise FlowError("connect: the browser has no open pages")

        for page in pages:
            if "accounts.google.com" in page.url:
                continue
            if FLOW_PATH.match(_path_of(page.url)):
                return page

        # Reuse a blank-ish tab rather than piling up windows.
        page = next((p for p in pages if p.url.startswith(("chrome://", "about:"))), None) \
            or self._browser.contexts[0].new_page()
        page.goto(self.project_url or FLOW_HOME, wait_until="domcontentloaded", timeout=60_000)
        page.wait_for_timeout(4000)
        if "accounts.google.com" in page.url:
            raise FlowError(
                "connect: this Chrome profile is not signed in to Google Flow. "
                "Sign in in that window, then retry — the profile keeps the session."
            )
        return page

    # -------------------------------------------------------------- basics

    def _body_text(self) -> str:
        try:
            return self.page.inner_text("body", timeout=3000) or ""
        except Exception:
            return ""

    def _smallest_exact(self, labels: list[str]):
        """The tightest element whose whole text is one of `labels`.

        A label like "Bắt đầu" is also in every ancestor's textContent, so the
        first match can be a wrapper spanning half the composer — clicking that
        lands nowhere near the control and looks exactly like a dead click.
        """
        return self.page.evaluate_handle(
            """(labels) => {
                const want = labels.map(s => s.toLowerCase());
                const vis = e => { const r = e.getBoundingClientRect();
                                   return r.width > 0 && r.height > 0; };
                const hits = [...document.querySelectorAll("button,[role='button'],div,span")]
                    .filter(vis)
                    .filter(e => want.includes((e.textContent || '').trim().toLowerCase()))
                    .map(e => { const r = e.getBoundingClientRect();
                                return { el: e, area: r.width * r.height }; })
                    .filter(c => c.area > 200)
                    .sort((a, b) => a.area - b.area);
                return hits.length ? hits[0].el : null;
            }""",
            labels,
        ).as_element()

    def _click(self, element, step: str) -> None:
        if element is None:
            raise FlowError(f"{step}: element not found")
        element.scroll_into_view_if_needed(timeout=5000)
        element.click(timeout=10_000)

    def dismiss_modals(self) -> None:
        for _ in range(10):
            text = self._body_text().lower()
            if not any(m in text for m in MODAL_MARKERS):
                return
            # The privacy notice keeps Continue disabled until its body is
            # scrolled to the end.
            self.page.evaluate(
                """() => { for (const el of document.querySelectorAll('*')) {
                    if (el.scrollHeight > el.clientHeight + 20) {
                        const oy = getComputedStyle(el).overflowY;
                        if (oy === 'auto' || oy === 'scroll') el.scrollTop = el.scrollHeight;
                    } } }"""
            )
            self.page.wait_for_timeout(300)
            for label in MODAL_ACCEPT:
                btn = self.page.locator(f'button:has-text("{label}")').first
                try:
                    if btn.count() and btn.is_visible() and btn.is_enabled():
                        btn.click(timeout=3000)
                        self.page.wait_for_timeout(600)
                        break
                except Exception:
                    continue
            else:
                return

    # ------------------------------------------------------------- project

    def ensure_project(self) -> None:
        if "/project/" in self.page.url:
            return
        self.dismiss_modals()
        for label in NEW_PROJECT:
            btn = self.page.locator(f'button:has-text("{label}")').first
            if btn.count() and btn.is_visible():
                btn.click(timeout=8000)
                self.page.wait_for_url("**/project/**", timeout=30_000)
                self.page.wait_for_timeout(2500)
                return
        raise FlowError("ensure_project: no project open and no 'New project' button found")

    # --------------------------------------------------------- prompt bar

    def _pill(self):
        # The settings pill carries the crop icon ligature; it appearing is the
        # signal that the classic (non-agent) composer finished rendering.
        loc = self.page.locator('button:has-text("crop_")').first
        return loc if loc.count() else None

    def wait_prompt_bar(self, timeout_s: int = 90) -> None:
        self.dismiss_modals()
        deadline = time.time() + timeout_s
        while time.time() < deadline:
            body = self._body_text()
            if "Application error" in body or "client-side exception" in body:
                # Flow crashes client-side often enough to be worth handling.
                self.page.reload(wait_until="domcontentloaded", timeout=45_000)
                self.page.wait_for_timeout(4000)
                self.dismiss_modals()
                continue

            pill = self._pill()
            if pill and pill.is_visible():
                return

            # A project may open in Agent mode, which has no inline pill.
            for label in DECLINE_AGENT:
                btn = self.page.locator(f'button:has-text("{label}")').first
                if btn.count() and btn.is_visible():
                    btn.click(timeout=3000)
                    self.page.wait_for_timeout(800)
            self.page.wait_for_timeout(1500)
        raise FlowError("wait_prompt_bar: the classic composer never appeared")

    # ------------------------------------------------------------ settings

    def _open_pill(self):
        """Open the settings popover and return it.

        The popover is identified by what it must contain — the VIDEO mode tab —
        not by being "some visible [role=menu]". Flow keeps other menus in the
        DOM, and matching one of those made this think the popover was already
        open, skip the click, and then fail looking for tabs that were never
        rendered.
        """
        pill = self._pill()
        if pill is None:
            raise FlowError("settings: pill not found")

        for attempt in range(3):
            if self._pill_menu():
                self.page.wait_for_timeout(400)
                return self._pill_menu()
            pill.click(timeout=8000)
            for _ in range(20):
                if self._pill_menu():
                    self.page.wait_for_timeout(400)
                    return self._pill_menu()
                self.page.wait_for_timeout(300)
        raise FlowError("settings: pill popover did not open")

    def _video_tab(self):
        return self.page.locator('[role="tab"][id$="-trigger-VIDEO"]').first

    def _pill_menu(self):
        """The settings popover, or None. Presence of the VIDEO tab is the test."""
        tab = self._video_tab()
        try:
            if tab.count() and tab.is_visible():
                return tab.locator("xpath=ancestor::*[@role='menu' or @role='dialog']").first
        except Exception:
            pass
        return None

    def _menu(self):
        return self._pill_menu()

    def _select_tab(self, suffix: str, label: str) -> None:
        """Radix trigger ids keep a stable suffix regardless of UI language."""
        tab = self.page.locator(f'[role="tab"][id$="-trigger-{suffix}"]').first
        if not tab.count():
            raise FlowError(f"settings: {label} option not found")
        if tab.get_attribute("aria-selected") == "true":
            return
        tab.click(timeout=8000)
        self.page.wait_for_timeout(400)
        # Verify rather than assume: a click onto an overlay changes nothing and
        # reports nothing.
        if tab.get_attribute("aria-selected") != "true":
            raise FlowError(f"settings: {label} would not select")

    def _tab_group(self, shape: str) -> list:
        """Locate a tab group by the shape of its labels.

        Duration and output-count share id suffixes — "4" is both "4s" and "x4"
        — so selecting by id alone silently sets the wrong control.
        """
        return self.page.evaluate(
            """(shape) => {
                const re = new RegExp(shape, 'i');
                const txt = e => (e.textContent || '').trim().replace(/\\s+/g, ' ');
                for (const list of document.querySelectorAll('[role="tablist"]')) {
                    const tabs = [...list.querySelectorAll('[role="tab"]')];
                    if (tabs.length && tabs.every(t => re.test(txt(t)))) {
                        return tabs.map(t => txt(t));
                    }
                }
                return null;
            }""",
            shape,
        )

    def _click_tab_by_text(self, text: str, label: str) -> None:
        tab = self.page.locator('[role="tab"]').filter(has_text=re.compile(rf"^{re.escape(text)}$")).first
        if not tab.count():
            raise FlowError(f"settings: {label} not offered")
        if tab.get_attribute("aria-selected") != "true":
            tab.click(timeout=8000)
            self.page.wait_for_timeout(400)
            if tab.get_attribute("aria-selected") != "true":
                raise FlowError(f"settings: {label} would not select")

    def apply_settings(self, *, aspect: str, model: str,
                       duration: Optional[str] = None,
                       resolution: Optional[str] = None,
                       count: int = 1) -> dict[str, Any]:
        menu = self._open_pill()

        self._select_tab("VIDEO", "video mode")
        self._select_tab("VIDEO_FRAMES", "frames sub-mode")

        # The model comes BEFORE duration and resolution because it decides
        # whether those controls exist at all: the Omni models render a duration
        # row and a 360p/720p row, the Veo ones render neither and run at their
        # own fixed length. Choosing the model last meant hunting for a duration
        # group the chosen model had already removed from the page.
        chosen_model = self._select_model(model)

        self._select_tab(ASPECT_ID.get(aspect, "LANDSCAPE"), f"aspect {aspect}")

        if resolution:
            tab = self.page.locator(
                f'[role="tab"][id$="-trigger-VIDEO_RESOLUTION_{resolution.upper()}"]').first
            if tab.count():
                self._select_tab(f"VIDEO_RESOLUTION_{resolution.upper()}", f"resolution {resolution}")
            else:
                raise FlowError(
                    f"settings: {chosen_model} does not offer a resolution choice in Flow, "
                    f"so {resolution} cannot be honoured")

        if duration:
            # Single backslashes: this string is handed to `new RegExp` in the
            # page, so doubling them would look for a literal backslash and the
            # group would never match.
            offered = self._tab_group(r"^\d+\s*s$")
            if not offered:
                raise FlowError(
                    f"settings: {chosen_model} does not offer a duration choice in Flow — "
                    f"the Omni models do, the Veo ones do not — so the requested {duration}s "
                    f'cannot be honoured. Omit "duration" to accept the model\'s own length.')
            if f"{duration}s" not in offered:
                raise FlowError(
                    f"settings: {duration}s is not offered (Flow lists: {', '.join(offered)})")
            self._click_tab_by_text(f"{duration}s", f"duration {duration}s")

        if self._tab_group(r"^x\s*\d+$"):
            # Flow defaults to more than one output per prompt, which multiplies
            # the credit cost for variants we throw away.
            self._click_tab_by_text(f"x{count}", f"output count x{count}")

        credits = None
        try:
            menu_text = menu.inner_text(timeout=3000)
            hit = re.search(r"(\d+)\s*(tín dụng|credits?)", menu_text, re.I)
            credits = int(hit.group(1)) if hit else None
        except Exception:
            pass

        self._close_pill()
        return {"model": chosen_model, "credits": credits}

    def _model_row(self):
        """The model dropdown inside the settings popover.

        Picked by content, never by position. `.first` has chosen the wrong
        element three times in this file — a wrapper instead of a chip, a text
        label instead of an asset row, and the "more options" kebab instead of
        this dropdown. The popover holds several aria-haspopup rows; the model
        one carries a caret ligature or a model name.
        """
        scope = self._pill_menu() or self.page
        candidates = scope.locator('[aria-haspopup="menu"]:not([role="tab"])')
        for i in range(candidates.count()):
            cand = candidates.nth(i)
            try:
                text = (cand.inner_text(timeout=1500) or "").strip()
            except Exception:
                continue
            if "more_vert" in text:
                continue
            if re.search(r"arrow_drop_down|expand_more|veo|omni", text, re.I):
                return cand
        return None

    def _select_model(self, model: str) -> str:
        row = self._model_row()
        if row is None:
            raise FlowError("settings: model dropdown not found in the settings popover")

        current = _clean_model_label(row.inner_text(timeout=3000) or "")
        if re.search(re.escape(model), current, re.I):
            return current

        row.click(timeout=8000)
        self.page.wait_for_timeout(900)

        options = self.page.locator('[role="menuitem"], [role="option"]')
        labels: list[str] = []
        target = None
        for i in range(options.count()):
            opt = options.nth(i)
            try:
                if not opt.is_visible():
                    continue
                text = (opt.inner_text(timeout=1500) or "").strip()
            except Exception:
                continue
            if not MODEL_RE.search(text):
                continue
            label = _clean_model_label(text)
            labels.append(label)
            if re.search(re.escape(model), label, re.I):
                target = opt
                chosen = label
        if target is None:
            # Never fall back to "any model": they differ in price, length and
            # which controls exist, so quietly using another is the same defect
            # as quietly ignoring the reference image.
            raise FlowError(
                f'settings: "{model}" is not one of Flow\'s models; the dropdown '
                f'reads "{current}" and offers: {" | ".join(labels) or "nothing"}')
        target.click(timeout=8000)
        self.page.wait_for_timeout(1000)  # the popover re-renders for the new model

        after_row = self._model_row()
        after = (after_row.inner_text(timeout=3000) or "") if after_row else ""
        if not re.search(re.escape(model), after, re.I):
            raise FlowError(
                f'settings: asked for "{model}" but Flow still shows '
                f'"{re.sub(chr(34), "", after).strip()}"')
        return chosen

    def _close_pill(self) -> None:
        for _ in range(4):
            if not self._menu():
                return
            self.page.keyboard.press("Escape")
            self.page.wait_for_timeout(500)
        if self._menu():
            raise FlowError("settings: popover would not close (it blocks the editor)")

    # -------------------------------------------------------- reference image

    def upload_image(self, path: Path, filename: str) -> str:
        """Put an image in the project library and return its media id.

        Uses Flow's own uploadImage endpoint from inside the page: the response
        carries the exact media id, where the click path had to poll the page
        text for a filename, sleep hoping Google had indexed it, then match a
        row in a picker. The access token is read from the page's own session
        and never leaves the browser.
        """
        project_id = _project_id(self.page.url)
        payload = base64.b64encode(path.read_bytes()).decode("ascii")
        mime = "image/png" if path.suffix.lower() == ".png" else "image/jpeg"

        result = self.page.evaluate(
            """async ({ projectId, imageBytes, mimeType, fileName }) => {
                const s = await (await fetch('/fx/api/auth/session',
                                             { credentials: 'same-origin' })).json();
                if (!s?.access_token) return { error: 'no access token in the Flow session' };
                const r = await fetch('https://aisandbox-pa.googleapis.com/v1/flow/uploadImage', {
                    method: 'POST',
                    headers: { Authorization: 'Bearer ' + s.access_token,
                               'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        clientContext: { projectId, tool: 'PINHOLE' },
                        imageBytes, isUserUploaded: true, isHidden: false, mimeType, fileName }),
                });
                if (!r.ok) return { error: 'uploadImage returned ' + r.status };
                const j = await r.json();
                return { mediaId: j?.media?.name || null };
            }""",
            {"projectId": project_id, "imageBytes": payload,
             "mimeType": mime, "fileName": filename},
        )
        if result.get("error"):
            raise FlowError(f"attach_frame: {result['error']}")
        if not result.get("mediaId"):
            raise FlowError("attach_frame: uploadImage returned no media id")
        return result["mediaId"]

    def upload_reference(self, path: Path) -> tuple[str, str]:
        """Upload the reference image and make Flow's picker aware of it.

        The picker renders a list the app fetched earlier, and nothing short of
        a page load refreshes it — reopening the picker is not enough. Verified
        against the live app: without the reload the asset exists server-side
        and the picker shows an empty library.
        """
        # A unique name per run: the library accumulates uploads, and two rows
        # with the same label make "pick the right one" a guess.
        unique = f"om-{random.randbytes(4).hex()}-{path.name}"[:60]
        media_id = self.upload_image(path, unique)

        self.page.reload(wait_until="domcontentloaded", timeout=60_000)
        self.page.wait_for_timeout(6000)
        self.dismiss_modals()
        self.wait_prompt_bar()
        return media_id, unique

    def attach_reference(self, unique: str) -> None:
        """Pick an already-uploaded image as the start frame."""
        self._click(self._smallest_exact(START_SLOT), "attach_frame: start slot")
        self.page.wait_for_timeout(2000)

        row = self._asset_row(unique)
        if row is None:
            listed = self.page.evaluate(
                """() => [...new Set([...document.querySelectorAll('*')]
                    .map(e => (e.textContent || '').trim())
                    .filter(t => /\.(png|jpe?g|webp)$/i.test(t) && t.length < 70))].slice(0, 8)"""
            )
            raise FlowError(
                f'attach_frame: "{unique}" is not in the picker; it lists: '
                f"{' | '.join(listed) or 'no image files at all'}")
        row.click(timeout=8000)
        self.page.wait_for_timeout(1200)

        # Clicking the row is usually enough: Flow attaches the asset and closes
        # the picker on the spot. The confirm button only appears in some
        # layouts, so it is used when present rather than required — demanding
        # it turned a successful attach into a reported failure.
        confirm = self.page.evaluate_handle(
            """(labels) => {
                const vis = e => { const r = e.getBoundingClientRect();
                                   return r.width > 0 && r.height > 0; };
                return [...document.querySelectorAll('button')].filter(vis)
                    .find(b => labels.some(l => (b.textContent || '').includes(l))) || null;
            }""",
            ADD_TO_PROMPT,
        ).as_element()
        if confirm is not None:
            confirm.click(timeout=8000)
            self.page.wait_for_timeout(2000)

        # Verify by Flow's own state. The slot label is replaced by a thumbnail
        # once something is attached, so its absence is the signal — checking for
        # a blob: image was wrong, since Flow serves thumbnails through its media
        # redirect, and that made a working attach look broken.
        deadline = time.time() + 15
        while time.time() < deadline:
            if self._smallest_exact(START_SLOT) is None:
                return
            self.page.wait_for_timeout(700)
        raise FlowError(
            "attach_frame: the start-frame slot is still empty after picking the image — "
            "Flow would have generated from the prompt only")

    def _picker_root(self):
        """The open asset picker, identified by the confirm button it contains."""
        return self.page.evaluate_handle(
            """(labels) => {
                const vis = e => { const r = e.getBoundingClientRect();
                                   return r.width > 0 && r.height > 0; };
                const dlgs = [...document.querySelectorAll(
                    '[role="dialog"], [data-radix-popper-content-wrapper]')].filter(vis);
                return dlgs.find(d => labels.some(l => (d.innerText || '').includes(l))) || null;
            }""",
            ADD_TO_PROMPT + UPLOADS_TAB,
        ).as_element()

    def _asset_row(self, filename: str, timeout_s: float = 20.0):
        """The picker row for this file.

        Matched by *containment*, not equality: rows read "imageom-probe.png" —
        a Material Symbols ligature glued to the filename — so an exact-text
        match never fires. The size filter picks the clickable row rather than
        the bare label inside it or the list that wraps it.
        """
        deadline = time.time() + timeout_s
        while time.time() < deadline:
            picker = self._picker_root()
            if picker is None:
                self.page.wait_for_timeout(1000)
                continue
            handle = picker.evaluate_handle(
                """(root, name) => {
                    const vis = e => { const r = e.getBoundingClientRect();
                                       return r.width > 0 && r.height > 0; };
                    // Scoped to the picker: the project grid behind the dialog
                    // shows the same filenames, and clicking one of those closes
                    // the picker without attaching anything.
                    const hits = [...root.querySelectorAll('*')]
                        .filter(vis)
                        .filter(e => (e.textContent || '').includes(name))
                        .map(e => { const r = e.getBoundingClientRect();
                                    return { el: e, w: r.width, h: r.height, top: r.top }; })
                        .filter(c => c.w >= 150 && c.w <= 600 && c.h >= 30 && c.h <= 120)
                        .sort((a, b) => a.top - b.top);
                    return hits.length ? hits[0].el : null;
                }""",
                filename,
            ).as_element()
            if handle is not None:
                return handle
            self.page.wait_for_timeout(1000)
        return None

    # -------------------------------------------------------------- prompt

    def _editor(self):
        return self.page.locator('[role="textbox"][contenteditable="true"]').first

    def _send_button(self):
        return self.page.locator('button:has-text("arrow_forward")').last

    def _prompt_accepted(self) -> bool:
        """Flow enables the send button only once its editor model holds a
        prompt, which makes it the one trustworthy signal the text landed."""
        btn = self._send_button()
        if not btn.count():
            return False
        return btn.get_attribute("aria-disabled") != "true" and btn.is_enabled()

    def type_prompt(self, text: str) -> None:
        editor = self._editor()
        editor.wait_for(state="visible", timeout=20_000)
        clean = re.sub(r"\s*\n\s*", " ", text).strip()

        editor.click(timeout=8000)
        self.page.keyboard.press("Control+a")
        self.page.keyboard.press("Delete")
        self.page.wait_for_timeout(200)

        # The composer is a Slate.js contenteditable. Setting .value or
        # dispatching a synthetic InputEvent puts characters in the DOM while
        # Slate's own model stays empty — the placeholder keeps showing and the
        # send button stays disabled. Real key events are what it listens to,
        # and Playwright's are real.
        editor.press_sequentially(clean, delay=8, timeout=120_000)
        self.page.wait_for_timeout(800)

        if not self._prompt_accepted():
            # Verify against Flow's own state, never against our DOM read: the
            # text being visible proves nothing about whether Flow accepted it.
            raise FlowError(
                "type_prompt: Flow still reports an empty prompt (the send button stays "
                "disabled) — the text reached the DOM but not the editor's model")

    # -------------------------------------------------------------- submit

    def media_names(self) -> set[str]:
        return set(self.page.evaluate(
            """() => {
                const out = [];
                for (const v of document.querySelectorAll('video')) {
                    const s = v.currentSrc || v.src || '';
                    if (!s.includes('media.getMediaUrlRedirect')) continue;
                    const n = new URL(s, location.origin).searchParams.get('name');
                    if (n) out.push(n.replace('_upsampled', ''));
                }
                return out;
            }"""
        ))

    def _reveal_players(self) -> None:
        """Nudge Flow into rendering clip <video> elements.

        The grid is react-virtuoso and the player is lazy: after a load the
        elements can take minutes to appear on their own, which reads as "the
        clip vanished".
        """
        self.page.evaluate(
            """() => {
                window.scrollTo(0, 0);
                const grid = document.querySelector('[data-test-id="virtuoso-item-list"]')
                          || document.querySelector('[data-test-id="virtuoso-scroller"]');
                const t = grid?.firstElementChild || grid;
                if (!t) return;
                const r = t.getBoundingClientRect();
                const o = { bubbles: true, clientX: r.left + r.width / 2,
                            clientY: r.top + r.height / 2 };
                t.dispatchEvent(new MouseEvent('mouseover', o));
                t.dispatchEvent(new MouseEvent('mousemove', o));
            }"""
        )
        self.page.wait_for_timeout(800)

    def stable_media_names(self, settle_s: float = 6.0, timeout_s: float = 45.0) -> set[str]:
        """Wait until the grid stops producing clips, then snapshot.

        A snapshot taken right after load sees a fraction of what is there, and
        anything appearing later looks brand new — which is how a run once
        returned an 8s clip from an earlier session while reporting the one it
        had just generated.
        """
        deadline = time.time() + timeout_s
        seen: set[str] = set()
        last_change = time.time()
        while True:
            self._reveal_players()
            now = self.media_names()
            if now != seen:
                seen = now
                last_change = time.time()
            if time.time() - last_change >= settle_s or time.time() > deadline:
                return seen
            self.page.wait_for_timeout(1500)

    def submit(self) -> None:
        # Check readiness BEFORE acting. Checking afterwards reads the
        # post-submit state — Flow clears the prompt on send, which disables the
        # button again — and reports a successful submit as a failure, throwing
        # away a clip that was already paid for.
        btn = self._send_button()
        if not btn.count():
            raise FlowError("submit: no send button found")
        if btn.get_attribute("aria-disabled") == "true" or not btn.is_enabled():
            raise FlowError("submit: the send button is disabled — Flow has not accepted the prompt")

        before = self.media_names()
        self._editor().click(timeout=5000)
        self.page.keyboard.press("Control+Enter")
        self.page.wait_for_timeout(1500)

        if self._submitted(before):
            return
        btn = self._send_button()
        if btn.count() and btn.get_attribute("aria-disabled") != "true":
            btn.click(timeout=8000)
            self.page.wait_for_timeout(1500)
        if not self._submitted(before):
            raise FlowError("submit: neither Ctrl+Enter nor the send button started a generation")

    def _submitted(self, before: set[str]) -> bool:
        # Flow empties the composer on send, so the button going back to
        # disabled is the earliest signal; a new clip or a progress figure
        # confirms it.
        if not self._prompt_accepted():
            return True
        if self.media_names() - before:
            return True
        return bool(re.search(r"\b\d{1,3}%\b", self._body_text()))

    # ---------------------------------------------------------- generation

    def wait_generation(self, before: set[str], timeout_s: float) -> str:
        deadline = time.time() + timeout_s
        while time.time() < deadline:
            self.page.wait_for_timeout(5000)
            body = self._body_text()
            if re.search(r"Sinh lại|Tạo lại|Generate again|lâu hơn bình thường", body, re.I):
                raise FlowError("generation failed: Flow reported an error on the clip")
            self._reveal_players()
            fresh = self.media_names() - before
            if fresh:
                return sorted(fresh)[0]
        raise FlowError(f"generation timeout after {timeout_s:.0f}s")

    def download(self, media_id: str, out_path: Path) -> int:
        """Fetch the finished clip through Flow's own media redirect."""
        for name in (f"{media_id}_upsampled", media_id):
            for _ in range(6):
                data = self.page.evaluate(
                    """async (name) => {
                        const r = await fetch(
                            '/fx/api/trpc/media.getMediaUrlRedirect?name=' + encodeURIComponent(name),
                            { credentials: 'same-origin' });
                        if (!r.ok) return null;
                        const buf = new Uint8Array(await r.arrayBuffer());
                        if (buf.length < 100000) return null;   // still rendering
                        let s = '';
                        for (let i = 0; i < buf.length; i += 8192) {
                            s += String.fromCharCode(...buf.subarray(i, i + 8192));
                        }
                        return btoa(s);
                    }""",
                    name,
                )
                if data:
                    blob = base64.b64decode(data)
                    if len(blob) >= MIN_VIDEO_BYTES:
                        out_path.parent.mkdir(parents=True, exist_ok=True)
                        out_path.write_bytes(blob)
                        return len(blob)
                self.page.wait_for_timeout(5000)   # upscale may still be running
        raise FlowError("download: the media never became available at a usable size")

    # ----------------------------------------------------------------- run

    def generate(self, job: dict[str, Any]) -> dict[str, Any]:
        """Drive one generation end to end. Returns what Flow actually did."""
        self.ensure_project()
        self.wait_prompt_bar()

        # Upload first. It reloads the page — the only thing that makes the
        # asset picker aware of a new upload — and doing that after configuring
        # the composer would throw the settings away.
        media_ref = unique = None
        if job.get("operation") == "image_to_video" and job.get("asset_path"):
            media_ref, unique = self.upload_reference(Path(job["asset_path"]))

        applied = self.apply_settings(
            aspect=job.get("aspect_ratio", "16:9"),
            model=job.get("model_variant", "Quality"),
            duration=job.get("duration"),
            resolution=job.get("resolution"),
        )

        if unique:
            self.attach_reference(unique)

        self.dismiss_modals()
        self.type_prompt(job["prompt"])

        before = self.stable_media_names()
        self.submit()
        media_id = self.wait_generation(before, float(job.get("timeout_seconds", 900)) - 90)
        size = self.download(media_id, Path(job["output_path"]))

        return {
            "output": job["output_path"],
            "bytes": size,
            "media_id": media_id,
            "reference_media_id": media_ref,
            "model": applied["model"],
            "credits": applied["credits"],
        }


def _clean_model_label(text: str) -> str:
    """Strip Flow's Material Symbols ligatures off a model label.

    Options read "volume_up
Veo 3.1 - Fast" and the closed row reads
    "Veo 3.1 - Fastarrow_drop_down". The icon name is a lowercase token glued to
    the label with arbitrary whitespace — an earlier version required the label
    to follow immediately, so a newline left the ligature in and the tool
    reported the model as "volume_up Veo 3.1 - Fast".
    """
    cleaned = re.sub(r"^[a-z_]+\s*(?=[A-Z0-9])", "", (text or "").strip())
    cleaned = re.sub(r"\s*(arrow_drop_down|expand_more|unfold_more)\s*$", "", cleaned)
    return " ".join(cleaned.split())


def _path_of(url: str) -> str:
    from urllib.parse import urlparse
    return urlparse(url).path


def _project_id(url: str) -> str:
    hit = re.search(r"/project/([0-9a-f-]{36})", url)
    if not hit:
        raise FlowError("no project id in the URL — open a Flow project first")
    return hit.group(1)
