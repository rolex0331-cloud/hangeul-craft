# korean-frontend-design

**개성 있는 디자인 + 한국어 완성도. 한국어 웹 화면을 위한 Claude Code 프론트엔드 디자인 플러그인.**

Anthropic 공식 `frontend-design`의 디자인 방법론(기획 → 검토 → 제작 → 비평, 템플릿 같은 AI 기본값 피하기)을 한국어로 옮기고, 그 플러그인에 없는 한국어 전문성을 더했습니다.

AI가 만든 UI에 한글을 넣으면 생기는 문제들:

- 단어 중간에서 줄이 바뀜 (`안녕하세\n요`)
- 영문 폰트만 지정돼서 한글이 OS 기본 글꼴로 뭉개짐
- 영문 기준 좁은 행간 때문에 답답한 본문
- "당신의 계정이 성공적으로 생성되었습니다" 같은 번역체
- First/Last name, 10/18/2026, $12.99 같은 해외식 입력·표기

- 토스 클론, 보라색 그라데이션, 이모지 3단 카드 같은 "AI가 만든 티"

이 플러그인은 이걸 자동으로 잡아줍니다.

## 들어 있는 것

| 구성 | 내용 |
|---|---|
| `SKILL.md` | 주제에서 출발하는 디자인 과정, 한국형 AI 기본값 목록, 한글 기본기(줄바꿈·폰트·행간·자간), 한국어 카피 원칙, 국내 표기·관행 |
| `references/korean-fonts.md` | 성격별 한글 서체 30여 종(로드 확인 완료), 페어링 원칙과 예시 |
| `references/typography.md` | 한글 폰트 선택표와 로드 방법(Pretendard 등), 크기·행간·자간 기준표 |
| `references/ui-patterns.md` | 약관 전체 동의, 사업자 정보 푸터, 하단 고정 CTA, 상품 카드, 소셜 로그인 버튼, 국내식 폼 |
| `references/local-services.md` | 다음 우편번호, 카카오·네이버 로그인, 토스페이먼츠·포트원 결제, 카카오맵·네이버 지도, 카카오톡 공유 |
| `scripts/check_korean.py` | 결과물 자동 검사기 (lang="ko", keep-all, 한글 폰트, break-all, 번역체, 해외식 표기, 여백 덮어쓰기, AI 기본값 신호) |

## 설치

```bash
/plugin marketplace add rolex0331-cloud/korean-frontend-design
/plugin install korean-frontend-design@korean-frontend-design
```

설치 후 한국어로 화면을 요청하면 자동으로 적용됩니다.

> "카페 원두 쇼핑몰 랜딩 페이지 만들어줘"
> "토스 스타일로 회원가입 화면 만들어줘"

## 검사기만 따로 쓰기

```bash
python skills/korean-frontend-design/scripts/check_korean.py ./src
```

```
ERROR  index.html:1: <html>에 lang="ko"가 없어요
ERROR  전체: 한글 텍스트가 있는데 word-break: keep-all이 없어요 — 단어 중간에서 줄이 바뀝니다
WARN   index.html:2: 번역체 문구 — 자연스러운 한국어로 다듬으세요
```

오류가 있으면 종료 코드 1이라 CI에도 넣을 수 있습니다.

## 라이선스

MIT. 일부 디자인 방법론은 Apache 2.0 라이선스의 anthropics/claude-plugins-official `frontend-design`에서 옮겨 왔습니다. `NOTICE` 참고.
