#!/usr/bin/env python3
"""판정 결과를 플러그인 기준으로 되돌려 승률·기준별 평균을 낸다.

usage: python eval/summarize.py <결과 폴더>
"""
import json
import subprocess
import sys
from pathlib import Path

CRITERIA = ["distinct", "typography", "copy", "local", "polish"]
CHECKER = Path(__file__).resolve().parent.parent / "skills/hangeul-craft/scripts/check_korean.py"


def checker_counts(html):
    out = subprocess.run([sys.executable, "-I", str(CHECKER), str(html)],
                         capture_output=True, text=True, encoding="utf-8").stdout
    return out.count("ERROR"), out.count("WARN")


def main(root):
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    root = Path(root)
    wins = {"ko": 0, "fd": 0, "tie": 0}
    totals = {w: {c: 0 for c in CRITERIA} for w in ("ko", "fd")}
    n = 0
    rows = []
    for d in sorted(p for p in root.iterdir() if p.is_dir()):
        per = []
        for j in sorted(d.glob("judge*")):
            try:
                v = json.loads((j / "verdict.json").read_text(encoding="utf-8"))
                a_is = (d / f".{j.name}_A_is").read_text().strip()
            except (OSError, ValueError):
                continue
            b_is = "fd" if a_is == "ko" else "ko"
            who = {"A": a_is, "B": b_is}
            winner = who.get(v.get("winner"), "tie")
            wins[winner] += 1
            for side in ("A", "B"):
                for c in CRITERIA:
                    totals[who[side]][c] += v[side].get(c, 0)
            n += 1
            per.append(winner)
        ce = {w: checker_counts(d / w / "index.html") for w in ("fd", "ko") if (d / w / "index.html").exists()}
        rows.append((d.name, per, ce))

    print(f"{'주제':<10} {'판정(r1,r2)':<14} {'원본 검사기(오류/경고)':<22} 우리 검사기(오류/경고)")
    for name, per, ce in rows:
        fd = "{}/{}".format(*ce["fd"]) if "fd" in ce else "-"
        ko = "{}/{}".format(*ce["ko"]) if "ko" in ce else "-"
        print(f"{name:<10} {','.join(per):<14} {fd:<22} {ko}")
    if not n:
        print("판정 결과가 없어요.")
        return
    print(f"\n판정 {n}회: 우리 {wins['ko']}승 · 원본 {wins['fd']}승 · 무승부 {wins['tie']}")
    print(f"우리 승률(무승부 제외): {wins['ko'] / max(1, wins['ko'] + wins['fd']):.0%}")
    print("\n기준별 평균 (우리 / 원본)")
    for c in CRITERIA:
        print(f"  {c:<11} {totals['ko'][c] / n:.1f} / {totals['fd'][c] / n:.1f}")


if __name__ == "__main__":
    main(sys.argv[1])
