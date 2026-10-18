# 국내 UI 패턴

## 1. 약관 동의 (회원가입·결제)

개인정보보호법상 필수/선택 동의는 구분해서 받아야 하고, 선택 동의를 하지 않아도 가입이 가능해야 한다. 마케팅 수신은 반드시 선택.

```html
<fieldset class="terms">
  <label class="terms-all">
    <input type="checkbox" id="agree-all"> <strong>전체 동의하기</strong>
  </label>
  <p class="terms-all-desc">선택 항목에 동의하지 않아도 서비스를 이용할 수 있어요.</p>
  <hr>
  <label><input type="checkbox" class="agree" required> [필수] 만 14세 이상이에요</label>
  <label><input type="checkbox" class="agree" required> [필수] 이용약관 동의 <a href="#">보기</a></label>
  <label><input type="checkbox" class="agree" required> [필수] 개인정보 수집·이용 동의 <a href="#">보기</a></label>
  <label><input type="checkbox" class="agree"> [선택] 마케팅 정보 수신 동의</label>
</fieldset>
<script>
  const all = document.getElementById('agree-all');
  const items = [...document.querySelectorAll('.agree')];
  all.addEventListener('change', () => items.forEach(i => i.checked = all.checked));
  items.forEach(i => i.addEventListener('change', () => all.checked = items.every(x => x.checked)));
</script>
```

- "보기"는 바텀시트/모달로 전문을 띄운다.
- 필수 미동의 상태에서는 "다음" 버튼 비활성화.

## 2. 사업자 정보 푸터 (쇼핑몰·유료 서비스)

전자상거래법상 통신판매업자는 사이트에 사업자 정보를 표시해야 한다. 작고 회색이어도 되지만 빠뜨리지 않는다. 값은 실제 정보로 바꾸도록 사용자에게 안내한다(임의 번호를 실제처럼 만들지 않는다).

```html
<footer class="biz-info">
  <p>
    상호명 (주)회사이름 · 대표 홍길동 · 사업자등록번호 000-00-00000
    <a href="https://www.ftc.go.kr/bizCommPop.do?wrkr_no=0000000000" target="_blank" rel="noopener">사업자정보확인</a><br>
    통신판매업신고 제0000-서울강남-0000호 · 주소 서울특별시 ○○구 ○○로 00<br>
    고객센터 1600-0000 (평일 10:00–18:00) · 이메일 help@example.com
  </p>
  <nav><a href="#">이용약관</a> · <a href="#"><strong>개인정보처리방침</strong></a></nav>
</footer>
```

개인정보처리방침 링크는 다른 링크보다 눈에 띄게(굵게) 표시하는 것이 관행이자 권고 사항이다.

## 3. 하단 고정 CTA (모바일)

```css
.bottom-cta {
  position: fixed; inset: auto 0 0 0;
  padding: 12px 16px calc(12px + env(safe-area-inset-bottom));
  background: linear-gradient(to top, #fff 80%, rgba(255,255,255,0));
}
.bottom-cta button {
  width: 100%; height: 56px; border-radius: 14px;
  font-size: 17px; font-weight: 700;
}
body { padding-bottom: 96px; } /* CTA에 내용이 가리지 않게 */
```

뷰포트 메타에 `viewport-fit=cover` 포함: `<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">`

## 4. 상품 카드 (커머스)

순서: 이미지 → 브랜드(회색, 작게) → 상품명(2줄 말줄임) → **할인율(빨강) + 판매가(굵게)** → 정가 취소선 → 별점·리뷰 수 → 배지(무료배송, 내일도착).

```html
<article class="product">
  <img src="..." alt="상품명">
  <p class="brand">브랜드명</p>
  <h3 class="name">상품명이 길면 두 줄까지만 보여주고 말줄임 처리해요</h3>
  <p class="price"><em class="rate">20%</em> <strong>12,900원</strong></p>
  <p class="origin"><del>16,000원</del></p>
  <p class="review">★ 4.8 <span>(1,234)</span></p>
  <span class="badge">무료배송</span>
</article>
```

```css
.product .name { display:-webkit-box; -webkit-line-clamp:2; -webkit-box-orient:vertical; overflow:hidden; }
.product .rate { color:#F04452; font-style:normal; font-weight:800; }
.product .price strong { font-weight:800; font-variant-numeric: tabular-nums; }
.product .origin { color:#9CA3AF; font-size:13px; }
```

## 5. 소셜 로그인 버튼

국내 사용률 순으로 카카오 → 네이버 → (애플/구글). 각 사 브랜드 가이드를 따른다.

- 카카오: 배경 `#FEE500`, 텍스트·심볼 검정(85% 불투명), 문구 "카카오 로그인" 또는 "카카오로 시작하기".
- 네이버: 배경 `#03C75A`, 흰색 N 로고, 문구 "네이버 로그인".
- 공식 로고 이미지는 각 개발자 센터에서 내려받아 쓴다(임의로 그리지 않는다).

## 6. 폼 입력

- 휴대폰 번호: `inputmode="numeric"`, 입력 중 자동 하이픈(010-1234-5678).
- 인증번호: `inputmode="numeric" autocomplete="one-time-code" maxlength="6"`, 남은 시간 타이머(03:00) 표시, "재전송" 버튼.
- 주소: [우편번호 찾기] 버튼 → 도로명 주소 자동 입력(읽기 전용) → 상세 주소 입력란으로 포커스 이동.
- 생년월일: 8자리 숫자 하나(19900101) 또는 년/월/일 셀렉트. 주민등록번호는 꼭 필요한 법적 근거가 없으면 받지 않는다.
- 라벨은 입력란 위에. placeholder만으로 라벨을 대신하지 않는다.

## 7. 토스트·스낵바·바텀시트

국내 앱은 확인 모달보다 **토스트**(하단 잠깐 표시)와 **바텀시트**(옵션 선택·약관 보기)를 많이 쓴다. 모바일에서 중앙 모달은 꼭 필요한 경고에만.

## 8. 빈 상태·로딩

- 빈 상태: 일러스트 + "아직 주문 내역이 없어요" + 행동 버튼("쇼핑하러 가기").
- 로딩: 스피너보다 스켈레톤 UI.

## 9. 공공·기관 페이지

- KRDS(대한민국 정부 디자인 시스템, 디지털 정부 서비스 UI/UX 가이드라인)를 우선 참고한다.
- 상단에 공식 누리집 표시, 글자 크기 조절, 고대비, 키보드 접근, 대체 텍스트 등 웹 접근성(KWCAG) 준수.
- 합니다체, 화려한 애니메이션·그라데이션 금지.
