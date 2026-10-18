# 한글 서체 고르기

Pretendard는 안전한 기본값이지 디자인 선택이 아니다. 주제의 성격이 서체에서 드러나야 한다. 아래는 웹에서 바로 불러올 수 있는 무료 한글 서체다(2026-10 기준 로드 확인). 배포 전 각 서체의 라이선스(대부분 SIL OFL)를 확인한다.

## 성격별 서체

| 성격 | 서체 | 어울리는 주제 | 로드 |
|---|---|---|---|
| 중립 고딕 (본문 기본) | Pretendard | 거의 모든 UI 본문 | jsDelivr |
| 기하학·현대적 고딕 | SUIT, Wanted Sans | 테크, 스타트업, 대시보드 | jsDelivr |
| 둥근·친근한 고딕 | Gowun Dodum, Spoqa Han Sans Neo | 생활, 육아, 반려동물, 동네 가게 | Google / jsDelivr |
| 인문적 고딕 | IBM Plex Sans KR, Gothic A1 | 리포트, 연구, 기업, 미디어 | Google |
| 전통 명조 (본문 가능) | Noto Serif KR, Nanum Myeongjo | 출판, 에세이, 법률, 공예 | Google |
| 부드러운 명조 | Gowun Batang | 차, 한식, 웰니스, 웨딩, 갤러리 | Google |
| 대비 큰 현대 명조 | Hahmlet (가변 굵기) | 패션, 매거진, 브랜드 제목 | Google |
| 붓·서예 | Song Myung, Nanum Brush Script | 전통주, 한옥, 축제, 문화재 | Google |
| 묵직한 디스플레이 | Black Han Sans, Gasoek One | 스포츠, 공연, 강한 헤드라인 | Google |
| 레트로·간판 | Do Hyeon, Jua, Gugi, Yeon Sung | 분식, 레트로, 동네 축제, 게임 | Google |
| 장난스러운·둥근 | Bagel Fat One, Dongle | 키즈, 디저트, 캐릭터 | Google |
| 손글씨 | Nanum Pen Script, Gamja Flower | 메모, 다이어리, 손편지 느낌 포인트 | Google |
| 실험적·장식 | Orbit, Diphylleia, Moirai One, Grandiflora One | 전시, 음악, 아트 프로젝트 | Google |
| 코드 | Nanum Gothic Coding, D2Coding | 개발 문서 | Google / 별도 |

디스플레이·손글씨·장식 서체는 **제목과 포인트에만** 쓴다. 본문은 고딕이나 본문용 명조로.

## 페어링 원칙

- 1종이면 굵기 대비로 위계를 만든다(Pretendard 300 / 800, Hahmlet 200 / 900).
- 2종이면 분명히 다르게. 명조 제목 + 고딕 본문, 디스플레이 제목 + 중립 고딕 본문. 고딕 + 고딕(Pretendard + SUIT)처럼 비슷한 조합은 의미 없다.
- 한글 서체에는 라틴 글자가 들어 있다. 영문 서체를 따로 더할 때는 한글 서체의 라틴과 x-height, 굵기가 맞는지 본다.
- 명조 본문은 고딕보다 크게(+1px)·넉넉하게(line-height 1.75) 쓴다.

## 페어링 예시 (그대로 쓰지 말고 출발점으로만)

| 주제 | 제목 | 본문 |
|---|---|---|
| 동네 수제 막걸리 양조장 | Song Myung | Gowun Dodum |
| 독립서점 | Hahmlet 700 | Noto Serif KR 400 |
| 아동 코딩 교실 | Bagel Fat One | Pretendard |
| 법무법인 | Noto Serif KR 600 | IBM Plex Sans KR |
| 인디 음악 페스티벌 | Gasoek One | SUIT |
| 웰니스·요가 | Gowun Batang | Pretendard 300/400 |
| 데이터 대시보드 | Wanted Sans (1종, 굵기 대비) | Wanted Sans |

## 로드 코드

Google Fonts (필요한 굵기만):

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Hahmlet:wght@300;700;900&family=Gowun+Dodum&display=swap" rel="stylesheet">
```

Google Fonts는 한글 서체를 유니코드 범위별로 자동 분할 제공하므로, 페이지에 쓰인 글자 묶음만 내려받는다.

jsDelivr:

```html
<!-- Pretendard (동적 서브셋) -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css">
<!-- SUIT (가변) -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/sun-typeface/SUIT@2.0.5/fonts/variable/woff2/SUIT-Variable.css">
<!-- Wanted Sans (가변) -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/wanteddev/wanted-sans@v1.0.3/packages/wanted-sans/fonts/webfonts/variable/split/WantedSansVariable.min.css">
```

font-family 이름: `"Pretendard Variable"`, `"SUIT Variable"`, `"Wanted Sans Variable"`.

## 피할 것

- 눈누(noonnu) 등에서 받은 상업용 무료 서체를 라이선스 확인 없이 웹폰트로 임베드
- 디스플레이 서체 전체 파일(수 MB)을 본문까지 로드
- 서체 4종 이상 혼용
