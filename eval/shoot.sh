#!/bin/bash
# 결과물마다 모바일(375px)·데스크톱(1440px) 스크린샷을 찍는다. 헤드리스 Chrome 필요.
# usage: eval/shoot.sh <결과 폴더>
set -u
OUT="$1"
CHROME="${CHROME:-}"
for c in "/c/Program Files/Google/Chrome/Application/chrome.exe" \
         "/c/Program Files (x86)/Microsoft/Edge/Application/msedge.exe" \
         "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
         "$(command -v google-chrome 2>/dev/null)" "$(command -v chromium 2>/dev/null)"; do
  [ -z "$CHROME" ] && [ -n "$c" ] && [ -x "$c" ] && CHROME="$c"
done
[ -z "$CHROME" ] && { echo "Chrome을 찾지 못했어요. CHROME=경로 로 지정하세요."; exit 1; }

# 헤드리스 Chrome은 창 최소 너비가 있어 375px 창을 그대로 쓰면 레이아웃이 더 넓게 잡힌다.
# 정확한 폭의 iframe 안에 페이지를 띄워서 찍는다.
for html in "$OUT"/*/*/index.html; do
  d="$(dirname "$html")"
  native="$(cd "$d" && pwd -W 2>/dev/null || pwd)"
  for spec in "mobile 375 1800" "desktop 1440 2200"; do
    set -- $spec
    [ -s "$d/$1.png" ] && continue
    cat > "$d/_frame_$1.html" <<EOF
<!doctype html><html><body style="margin:0;overflow:hidden">
<iframe src="index.html" style="width:$2px;height:$3px;border:0;display:block"></iframe></body></html>
EOF
    "$CHROME" --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor=1 \
      --allow-file-access-from-files --virtual-time-budget=5000 --window-size="$2,$3" \
      --screenshot="$native/$1.png" "file:///$native/_frame_$1.html" >/dev/null 2>&1
    rm -f "$d/_frame_$1.html"
  done
  echo "shot $d"
done
