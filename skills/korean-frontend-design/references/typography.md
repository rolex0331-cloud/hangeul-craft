# 한글 타이포그래피

## 폰트 선택

모두 무료 상업 사용 가능(SIL OFL 등). 배포 전 각 폰트의 최신 라이선스를 확인한다.

| 용도 | 폰트 | 특징 |
|---|---|---|
| 기본 고딕 (1순위) | **Pretendard** | 국내 웹 사실상 표준. 영문·숫자가 Inter 기반이라 섞어 써도 자연스러움. 가변 폰트 지원 |
| 기본 고딕 대안 | Noto Sans KR | Google Fonts로 간편 로드. 다소 넓고 무난 |
| 기본 고딕 대안 | SUIT, Spoqa Han Sans Neo | 깔끔한 UI용. SUIT는 자간이 좁아 정보 밀도 높은 화면에 적합 |
| 명조 (에디토리얼) | Noto Serif KR, 마루부리(MaruBuri) | 브랜드·매거진·포트폴리오 제목 |
| 디스플레이 | Gmarket Sans, 여기어때 잘난체, 나눔스퀘어 네오 | 랜딩 헤드라인·배너 한정. 본문 금지 |
| 코드 | D2Coding, JetBrains Mono + Pretendard | 코드 블록 |

### 로드 방법

Pretendard (CDN, 동적 서브셋 — 필요한 글자만 내려받아 빠름):

```html
<link rel="stylesheet" as="style" crossorigin
  href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css" />
```

npm: `npm i pretendard` 후 `import 'pretendard/dist/web/variable/pretendardvariable-dynamic-subset.css'`.

Next.js `next/font/local`로 `PretendardVariable.woff2`를 self-host하는 것도 좋다(외부 요청 제거).

Noto Sans KR (Google Fonts):

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700;800&display=swap" rel="stylesheet">
```

한글 폰트 파일은 영문보다 수십~수백 배 크다(글자 수 11,172자). 전체 웹폰트를 통째로 넣지 말고 **서브셋/동적 서브셋**을 쓴다. 디스플레이 폰트는 제목에 쓸 글자만 서브셋하거나 이미지로 처리한다.

### font-family 순서

```css
font-family: "Pretendard Variable", Pretendard,
  -apple-system, BlinkMacSystemFont, system-ui,
  "Apple SD Gothic Neo",   /* macOS·iOS 한글 */
  "Noto Sans KR",
  "Malgun Gothic",         /* Windows 한글 (맑은 고딕) */
  sans-serif;
```

영문 브랜드 폰트를 쓸 때: `font-family: "Inter", "Pretendard Variable", ...` — 영문 글자는 Inter, 한글은 Pretendard로 떨어진다. 한글 폰트를 빼먹지 않는 것이 핵심.

## 줄바꿈

| 속성 | 값 | 이유 |
|---|---|---|
| `word-break` | `keep-all` | 한글은 기본적으로 **글자 단위**로 줄이 바뀐다. 어절(띄어쓰기) 단위로 바꾸려면 필수 |
| `overflow-wrap` | `break-word` (또는 `anywhere`) | keep-all 상태에서 긴 영문·URL·띄어쓰기 없는 문자열이 박스를 넘지 않게 |
| `text-wrap` | 제목 `balance`, 본문 `pretty` | 마지막 줄에 한 단어만 남는 것 방지(지원 브라우저에서) |

`word-break: break-all`은 한글을 아무 곳에서나 자르므로 쓰지 않는다.

좁은 카드·버튼·탭·뱃지는 `white-space: nowrap; overflow: hidden; text-overflow: ellipsis;`. 여러 줄 말줄임은 `-webkit-line-clamp`.

제목 줄바꿈 위치를 직접 지정하려면 `<br>` 대신 반응형을 고려해 어절 단위 `<span style="display:inline-block">`로 묶는 방법도 있다.

## 크기·행간·자간 기준

| 요소 | 크기 (모바일 / 데스크톱) | 굵기 | 행간 | 자간 |
|---|---|---|---|---|
| Display / 히어로 | 32–40 / 48–64px | 700–800 | 1.25 | -0.03em |
| H1 | 26–28 / 36–40px | 700 | 1.3 | -0.02em |
| H2 | 22 / 28px | 700 | 1.35 | -0.02em |
| H3 | 18 / 20px | 600 | 1.4 | -0.01em |
| 본문 | 15–16 / 16–17px | 400 | 1.6–1.7 | -0.01em ~ 0 |
| 캡션·보조 | 13 / 13–14px | 400–500 | 1.5 | 0 |

- 한글은 글자 높이가 꽉 차서 영문과 같은 행간이면 답답하다. 본문은 최소 1.6.
- 한글은 굵기 차이가 영문보다 덜 드러난다. 위계는 굵기보다 **크기와 색 대비**로 확실히 준다.
- 회색 텍스트는 대비 4.5:1 이상 유지(예: 흰 배경에 #6B7280 이상 진하게).

## 숫자·영문 혼용

- Pretendard는 숫자 폭이 일정하지 않을 수 있으므로 가격표·표·카운터에는 `font-variant-numeric: tabular-nums;`.
- 한글과 영문/숫자 사이 자동 간격 조정 CSS(`text-autospace`)는 지원이 제한적이므로 의존하지 않는다.
