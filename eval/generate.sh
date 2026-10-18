#!/bin/bash
# 같은 요청으로 두 플러그인의 결과물을 만든다.
# usage: eval/generate.sh <결과 폴더> [동시 실행 수=5]
# 비교가 공정하도록, 실행 전 사용자 범위에 설치된 korean-frontend-design은 꺼 둔다:
#   claude plugin disable korean-frontend-design@korean-frontend-design
set -u
OUT="$(cd "$1" 2>/dev/null || mkdir -p "$1" && cd "$1" && pwd)"
JOBS="${2:-5}"
HERE="$(cd "$(dirname "$0")" && pwd)"
export KO_DIR="$(dirname "$HERE")"
export FD_DIR="${FD_DIR:-$HOME/.claude/plugins/marketplaces/claude-plugins-official/plugins/frontend-design}"
export OUT

gen() { # "<plugin>|<id>|<prompt>"
  IFS='|' read -r who id prompt <<< "$1"
  dir="$OUT/$id/$who"; mkdir -p "$dir"
  [ -s "$dir/index.html" ] && { echo "skip $id/$who"; return; }
  if [ "$who" = ko ]; then pd="$KO_DIR"; else pd="$FD_DIR"; fi
  (cd "$dir" && claude -p "$prompt" --plugin-dir "$pd" --permission-mode acceptEdits \
     --allowedTools "Write Edit Read Skill Glob Bash(python:*) Bash(python3:*)" > log.txt 2>&1)
  echo "done $id/$who ($([ -s "$dir/index.html" ] && echo ok || echo MISSING))"
}
export -f gen

while IFS='|' read -r id prompt; do
  [ -z "$id" ] && continue
  echo "fd|$id|$prompt"; echo "ko|$id|$prompt"
done < "$HERE/prompts.txt" | tr '\n' '\0' | xargs -0 -P "$JOBS" -I{} bash -c 'gen "$1"' _ {}
