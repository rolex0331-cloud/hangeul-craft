#!/usr/bin/env python3
"""렌더링 검사기: 헤드리스 Chrome으로 페이지를 실제로 띄워서 모바일 폭 문제를 잰다.

사용법: python check_render.py <index.html> [폭=375]

찾는 것
- 가로 넘침: 문서가 화면 폭보다 넓거나, 화면 밖으로 삐져나간 요소
- 빈 첫 화면: 첫 화면(높이 812px) 안에 보이는 글자가 거의 없음
- 숨은 콘텐츠: opacity 0·visibility hidden 상태로 남은 글자(등장 애니메이션 의존)

Chrome/Edge가 필요하다. CHROME 환경 변수로 경로를 지정할 수 있다.
오류가 있으면 종료 코드 1.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

CANDIDATES = [
    os.environ.get("CHROME", ""),
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    shutil.which("google-chrome") or "",
    shutil.which("chromium") or "",
    shutil.which("chromium-browser") or "",
]

PROBE = r"""
<!doctype html><html><body style="margin:0">
<iframe id="f" src="%(src)s" style="width:%(w)dpx;height:812px;border:0"></iframe>
<pre id="out">pending</pre>
<script>
const f = document.getElementById('f');
f.addEventListener('load', () => setTimeout(() => {
  const r = { error: null };
  try {
    const d = f.contentDocument, W = %(w)d, H = 812;
    r.scrollWidth = d.documentElement.scrollWidth;
    const effOpacity = el => { let o = 1; for (let e = el; e && e.nodeType === 1; e = e.parentElement) {
      const cs = d.defaultView.getComputedStyle(e);
      if (cs.visibility === 'hidden' || cs.display === 'none') return 0;
      o *= parseFloat(cs.opacity); } return o; };
    // 가로 스크롤 영역이나 overflow:hidden 부모 안에서 잘리는 건 의도된 것이라 제외
    const clipped = el => { for (let e = el.parentElement; e && e !== d.body; e = e.parentElement) {
      const ox = d.defaultView.getComputedStyle(e).overflowX;
      if (ox !== 'visible' && e.getBoundingClientRect().right <= W + 1) return true; } return false; };
    const over = [], hidden = []; let firstScreen = 0;
    const walker = d.createTreeWalker(d.body, NodeFilter.SHOW_TEXT);
    for (let n; (n = walker.nextNode());) {
      const t = n.textContent.trim(); if (!t) continue;
      const el = n.parentElement; const tag = el.tagName;
      if (tag === 'SCRIPT' || tag === 'STYLE' || tag === 'NOSCRIPT') continue;
      const rg = d.createRange(); rg.selectNodeContents(n); const b = rg.getBoundingClientRect();
      if (!b.width) continue;
      const op = effOpacity(el);
      if (op < 0.1) { hidden.push(t.slice(0, 20)); continue; }
      if (b.top < H && b.bottom > 0) firstScreen += t.length;
      // 완전히 화면 밖(건너뛰기 링크·스크린리더 전용)은 의도된 숨김이라 제외, 걸쳐서 잘리는 것만
      if (b.width > 2 && ((b.right > W + 1 && b.left < W) || (b.left < -1 && b.right > 0)) && !clipped(el)) over.push(t.slice(0, 20));
    }
    for (const el of d.body.querySelectorAll('*')) {
      const b = el.getBoundingClientRect();
      if (b.width > 2 && b.right > W + 1 && b.left < W && !over.length && !clipped(el)) over.push('<' + el.tagName.toLowerCase() + ' class="' + (el.className || '') + '">');
    }
    r.overflowing = [...new Set(over)].slice(0, 8);
    r.hidden = hidden.length; r.hiddenSample = hidden.slice(0, 5);
    r.firstScreenChars = firstScreen;
  } catch (e) { r.error = String(e); }
  document.getElementById('out').textContent = 'RESULT' + JSON.stringify(r) + 'END';
}, 1500));
</script></body></html>
"""


def find_chrome():
    for c in CANDIDATES:
        if c and Path(c).exists():
            return c
    return None


def main(argv):
    if not argv:
        print(__doc__)
        return 2
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    page = Path(argv[0]).resolve()
    width = int(argv[1]) if len(argv) > 1 else 375
    chrome = find_chrome()
    if not chrome:
        print("Chrome/Edge를 찾지 못해 렌더링 검사를 건너뜁니다. CHROME=경로 로 지정하세요.")
        return 0

    probe = page.parent / f"_render_probe_{os.getpid()}.html"
    probe.write_text(PROBE % {"src": page.name, "w": width}, encoding="utf-8")
    try:
        with tempfile.TemporaryDirectory() as prof:
            out = subprocess.run(
                [chrome, "--headless=new", "--disable-gpu", "--allow-file-access-from-files",
                 f"--user-data-dir={prof}", "--virtual-time-budget=6000", "--window-size=1200,900",
                 "--dump-dom", probe.as_uri()],
                capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=90,
            ).stdout
    finally:
        probe.unlink(missing_ok=True)

    start, end = out.find("RESULT"), out.find("END", out.find("RESULT"))
    if start < 0 or end < 0:
        print("렌더링 결과를 읽지 못했어요.")
        return 0
    r = json.loads(out[start + 6:end].replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&").replace("&quot;", '"'))
    if r.get("error"):
        print(f"렌더링 검사 실패: {r['error']}")
        return 0

    errors, warnings = [], []
    if r["scrollWidth"] > width + 1:
        errors.append(f"{width}px 화면에서 가로 스크롤이 생겨요 (문서 폭 {r['scrollWidth']}px)")
    if r["overflowing"]:
        errors.append("화면 밖으로 잘리는 요소: " + ", ".join(r["overflowing"]))
    if r["firstScreenChars"] < 20:
        errors.append(f"첫 화면에 보이는 글자가 {r['firstScreenChars']}자뿐이에요 — 등장 애니메이션이나 거대한 빈 히어로 때문에 비어 보입니다")
    if r["hidden"] >= 5:
        warnings.append(f"opacity 0·숨김 상태로 남은 글자 {r['hidden']}곳 (예: {', '.join(r['hiddenSample'])}) — "
                        "스크롤 등장 효과에 기대지 말고 기본 상태에서 보이게 하세요")

    for e in errors:
        print(f"ERROR  {e}")
    for w in warnings:
        print(f"WARN   {w}")
    print(f"\n렌더링 검사 ({width}px) · 오류 {len(errors)} · 경고 {len(warnings)} · 첫 화면 글자 {r['firstScreenChars']}자")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
