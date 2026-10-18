#!/usr/bin/env python3
"""한국어 웹 UI 검사기.

사용법: python check_korean.py <파일 또는 폴더> [...]

HTML/CSS/JS/JSX/TSX/Vue/Svelte 파일에서 한글 UI의 흔한 실수를 찾는다.
오류(ERROR)가 하나라도 있으면 종료 코드 1.
"""
import re
import sys
from pathlib import Path

EXTS = {".html", ".htm", ".css", ".scss", ".js", ".jsx", ".ts", ".tsx", ".vue", ".svelte", ".astro"}
SKIP_DIRS = {"node_modules", ".git", "dist", "build", ".next", "out", "coverage"}

HANGUL = re.compile(r"[가-힣]")
KOREAN_FONTS = re.compile(
    r"Pretendard|Noto\s*Sans\s*KR|Noto\s*Serif\s*KR|Apple\s*SD\s*Gothic|Malgun|맑은\s*고딕|"
    r"SUIT|Spoqa|Nanum|나눔|MaruBuri|마루부리|Gmarket|IBM\s*Plex\s*Sans\s*KR|Wanted\s*Sans|"
    r"Gowun|Black\s*Han\s*Sans|Do\s*Hyeon|Jua|Sunflower|Gothic\s*A1",
    re.I,
)
FONT_DECL = re.compile(r"font-family\s*:|fontFamily\s*[:=]", re.I)
KEEP_ALL = re.compile(r"word-break\s*:\s*keep-all|wordBreak\s*:\s*['\"]keep-all|\bbreak-keep\b", re.I)
BREAK_ALL = re.compile(r"word-break\s*:\s*break-all|wordBreak\s*:\s*['\"]break-all|\bbreak-all\b", re.I)
HTML_TAG = re.compile(r"<html\b[^>]*>", re.I)
LANG_KO = re.compile(r"lang\s*=\s*['\"]ko", re.I)

# (패턴, 메시지) — 줄 단위 경고
LINE_RULES = [
    (re.compile(r"lorem\s+ipsum", re.I), "영어 더미 텍스트(Lorem ipsum) — 자연스러운 한국어 예시 문구로 바꾸세요"),
    (re.compile(r"first\s*name|last\s*name|\b이름\s*\(성\)|성\s*/\s*이름", re.I), "성/이름 분리 입력은 해외 패턴 — '이름' 한 칸으로"),
    (re.compile(r"(?<![\d/])(0?[1-9]|1[0-2])/(0?[1-9]|[12]\d|3[01])/(19|20)\d{2}(?![\d/])"), "MM/DD/YYYY 날짜 — 2026년 10월 18일 또는 2026.10.18 형식으로"),
    (re.compile(r"것이\s*가능합니다|당신의|성공적으로\s*(완료|처리)|하는\s*것을\s*원하|에\s*의해\s*제공"), "번역체 문구 — 자연스러운 한국어로 다듬으세요"),
    (re.compile(r"\$\s?\d[\d,]*(\.\d{2})?"), "달러 가격 표기 — 국내 서비스라면 12,900원 형식으로 (의도한 경우 무시)"),
    (re.compile(r"text-transform\s*:\s*uppercase|\buppercase\b"), "uppercase는 한글에 효과 없음 — 한글 텍스트라면 굵기·크기로 강조하세요"),
]


def iter_files(paths):
    for p in paths:
        p = Path(p)
        if p.is_file():
            if p.suffix.lower() in EXTS:
                yield p
        elif p.is_dir():
            for f in p.rglob("*"):
                if f.is_file() and f.suffix.lower() in EXTS and not (SKIP_DIRS & set(f.parts)):
                    yield f


def main(argv):
    if not argv:
        print(__doc__)
        return 2
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    files = list(iter_files(argv))
    if not files:
        print("검사할 파일이 없어요.")
        return 2

    errors, warnings = [], []
    has_hangul = has_keep_all = has_kfont = has_font_decl = False

    for f in files:
        try:
            text = f.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        has_hangul |= bool(HANGUL.search(text))
        has_keep_all |= bool(KEEP_ALL.search(text))
        has_kfont |= bool(KOREAN_FONTS.search(text))
        has_font_decl |= bool(FONT_DECL.search(text))

        m = HTML_TAG.search(text)
        if m and not LANG_KO.search(m.group(0)) and HANGUL.search(text):
            line = text[: m.start()].count("\n") + 1
            errors.append(f"{f}:{line}: <html>에 lang=\"ko\"가 없어요")

        for i, line in enumerate(text.splitlines(), 1):
            if BREAK_ALL.search(line):
                errors.append(f"{f}:{i}: word-break: break-all은 한글을 글자 단위로 자릅니다 — keep-all을 쓰세요")
            for pat, msg in LINE_RULES:
                if pat.search(line):
                    warnings.append(f"{f}:{i}: {msg}")

    if has_hangul and not has_keep_all:
        errors.append("전체: 한글 텍스트가 있는데 word-break: keep-all(또는 Tailwind break-keep)이 없어요 — 단어 중간에서 줄이 바뀝니다")
    if has_hangul and not has_kfont:
        level = errors if has_font_decl else warnings
        level.append("전체: 한글 폰트(Pretendard, Noto Sans KR 등)가 지정되지 않았어요 — OS마다 한글이 다르게 보입니다")

    for e in errors:
        print(f"ERROR  {e}")
    for w in warnings:
        print(f"WARN   {w}")
    print(f"\n파일 {len(files)}개 검사 · 오류 {len(errors)} · 경고 {len(warnings)}")
    if not errors and not warnings:
        print("한글 UI 기본기 통과 ✓")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
