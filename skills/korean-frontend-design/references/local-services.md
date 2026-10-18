# 국내 서비스 연동 패턴

SDK 버전·URL·파라미터는 자주 바뀐다. 코드를 쓰기 전에 각 공식 문서에서 최신 내용을 확인하고, 확인하지 못했다면 사용자에게 "공식 문서에서 최신 버전 확인 필요"라고 알린다. 키·시크릿은 코드에 하드코딩하지 말고 환경 변수로 둔다.

## 주소 검색 — 다음(카카오) 우편번호 서비스

키 발급 없이 무료로 쓸 수 있다. 공식 안내: https://postcode.map.daum.net/guide

```html
<input id="zonecode" placeholder="우편번호" readonly>
<button type="button" onclick="openPostcode()">우편번호 찾기</button>
<input id="address" placeholder="도로명 주소" readonly>
<input id="detail" placeholder="상세 주소를 입력해 주세요">

<script src="//t1.daumcdn.net/mapjsapi/bundle/postcode/prod/postcode.v2.js"></script>
<script>
function openPostcode() {
  new daum.Postcode({
    oncomplete(data) {
      document.getElementById('zonecode').value = data.zonecode;
      document.getElementById('address').value = data.roadAddress || data.jibunAddress;
      document.getElementById('detail').focus();
    }
  }).open();
}
</script>
```

모바일에서는 `.open()` 팝업 대신 `.embed(element)`로 레이어 안에 띄우는 편이 낫다.

## 카카오 로그인

- 문서: https://developers.kakao.com/docs/latest/ko/kakaologin/common
- Kakao Developers에서 앱 생성 → JavaScript 키 / REST API 키 발급 → 플랫폼(도메인)·Redirect URI 등록.
- 웹은 JavaScript SDK의 `Kakao.Auth.authorize({ redirectUri })`로 인가 코드를 받고, **토큰 교환은 서버에서** REST API로 한다(클라이언트 시크릿 노출 금지).
- 버튼 디자인은 카카오 디자인 가이드 준수(`#FEE500`).

## 네이버 로그인

- 문서: https://developers.naver.com/docs/login/overview/
- 네이버 개발자센터 애플리케이션 등록 → Client ID/Secret → Callback URL 등록.
- 인가 코드 → 서버에서 토큰 교환 → 프로필 조회. 검수 전에는 등록된 테스트 아이디만 로그인 가능.

## 결제 — 토스페이먼츠 / 포트원

- 토스페이먼츠: https://docs.tosspayments.com — 결제위젯(카드·간편결제·계좌이체 UI를 한 번에 제공) 사용 권장. 흐름: 클라이언트에서 결제 요청 → successUrl로 `paymentKey, orderId, amount` 수신 → **서버에서 금액 검증 후 결제 승인 API 호출**.
- 포트원(PortOne): https://developers.portone.io — 여러 PG사(KG이니시스, NHN KCP, 토스페이먼츠 등)를 하나의 SDK로 연동할 때.
- 공통 원칙: 결제 금액은 반드시 서버에서 주문 정보와 대조해 검증한다. 개발 중에는 테스트 키만 쓴다.
- 결제 화면에는 결제 금액 합계, 할인, 배송비를 명확히 분리해 보여주고 "총 12,900원 결제하기"처럼 버튼에 금액을 넣는다.

## 지도

- 카카오맵 JavaScript API: https://apis.map.kakao.com/web/guide/ — JavaScript 키 + 도메인 등록.
- 네이버 지도(NAVER Maps API, 네이버 클라우드 플랫폼): https://navermaps.github.io/maps.js.ncp/ — Client ID 발급.
- 국내 주소·장소 검색 정확도 때문에 국내 서비스는 구글 지도보다 카카오·네이버 지도를 주로 쓴다.

## 본인인증

- 휴대폰 본인인증은 PASS·통신사 인증을 PG사/포트원 본인인증 기능으로 연동한다. 직접 구현하지 않는다.
- 단순 연락처 확인이면 SMS 인증번호(문자 발송 서비스: NHN Cloud, 솔라피 등)로 충분하다.

## 공유

- 카카오톡 공유: Kakao JavaScript SDK `Kakao.Share.sendDefault` (피드 템플릿). 국내 서비스의 공유 버튼 1순위.
- 링크 미리보기(오픈그래프): `og:title`, `og:description`, `og:image`(1200×630)를 한국어로 채운다. 카카오톡 미리보기 캐시는 카카오 개발자 도구에서 초기화할 수 있다.
