#!/bin/bash
# 블라인드 판정: 두 결과물의 스크린샷을 A/B로 이름만 바꿔 별도 Claude에게 보여준다.
# 위치 편향을 없애려고 순서를 바꿔 두 번 판정한다(round 1: A=fd, round 2: A=ko).
# usage: eval/judge.sh <결과 폴더> [동시 실행 수=5]
set -u
OUT="$(cd "$1" && pwd)"
JOBS="${2:-5}"
HERE="$(cd "$(dirname "$0")" && pwd)"
export OUT HERE

judge() { # "<id>|<round>"
  IFS='|' read -r id round <<< "$1"
  prompt="$(grep "^$id|" "$HERE/prompts.txt" | cut -d'|' -f2-)"
  if [ "$round" = 1 ]; then a=fd; b=ko; else a=ko; b=fd; fi
  j="$OUT/$id/judge$round"; mkdir -p "$j"
  [ -s "$j/verdict.json" ] && return
  for v in mobile desktop; do
    cp "$OUT/$id/$a/$v.png" "$j/A_$v.png"; cp "$OUT/$id/$b/$v.png" "$j/B_$v.png"
  done
  echo "$a" > "$OUT/$id/.judge${round}_A_is"
  (cd "$j" && claude -p "$(cat <<EOF
당신은 한국 웹 서비스 디자인 심사위원이다. 두 디자이너가 같은 의뢰로 만든 웹 페이지를 블라인드로 비교한다.

의뢰: "$prompt"

현재 폴더의 스크린샷 4장을 Read 도구로 모두 열어 본다:
- A_mobile.png, A_desktop.png (A안)
- B_mobile.png, B_desktop.png (B안)

아래 5개 기준으로 각 안을 1~10점 채점한다. 한국 사용자가 실제로 이 페이지를 쓴다고 생각하고 엄격하게 본다.
1. distinct: 주제에 맞는 개성. 흔한 AI 템플릿 느낌(보라 그라데이션, 똑같은 카드 반복, 토스 클론, 이모지 장식)이면 감점
2. typography: 한글 타이포그래피. 단어 중간 줄바꿈, 어색한 행간·자간, 한글 서체 선택, 위계
3. copy: 한국어 문구의 자연스러움. 번역체·상투어·영어 혼용이면 감점
4. local: 국내 관행 (원화·날짜 표기, 약관 동의, 사업자 정보, 모바일 우선, 국내 결제·지도 등 의뢰에 필요한 것)
5. polish: 완성도. 잘림, 겹침, 빈 영역, 가로 넘침, 깨진 레이아웃

마지막 줄에 아래 형식의 JSON 한 줄만 출력한다(앞뒤 설명은 그 위에):
{"A":{"distinct":0,"typography":0,"copy":0,"local":0,"polish":0},"B":{"distinct":0,"typography":0,"copy":0,"local":0,"polish":0},"winner":"A|B|tie","reason":"한 문장"}
EOF
)" --allowedTools "Read" > judge_log.txt 2>&1)
  tail -n 5 "$j/judge_log.txt" | grep -o '{"A".*}' | tail -n 1 > "$j/verdict.json"
  echo "judged $id r$round $(cat "$j/verdict.json" | grep -o '"winner":"[^"]*"')"
}
export -f judge

for d in "$OUT"/*/; do
  id="$(basename "$d")"
  [ -s "$d/fd/mobile.png" ] && [ -s "$d/ko/mobile.png" ] || { echo "skip $id (스크린샷 없음)"; continue; }
  printf '%s|1\0%s|2\0' "$id" "$id"
done | xargs -0 -P "$JOBS" -I{} bash -c 'judge "$1"' _ {}
