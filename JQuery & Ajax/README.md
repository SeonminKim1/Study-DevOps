## JQuery
- Javascript로 HTML을 쉽게 제어 목적
- JavaScript Document 기반 접근은 복잡하므로 대신 사용.

## Client 요청 Type
- GET
    - 일반적으로 데이터 조회(Read)를 요청 
        - ex) 영화 목록 조회
    - 요청시 url뒤에 아래와 같이 정보를 붙여서 데이터를 가져감
        - ex) http://naver.com?param=value&param2=value2 
- POST
    - 일반적으로 데이터 생성(Create), 변경(Update), 삭제(Delete) 요청 
        - ex) 회원가입, 회원탈퇴, 비밀번호 수정
    - POST 요청은, data : {} 에 넣어서 데이터를 가져감. 
        - ex) data: { param: 'value', param2: 'value2' },
## GET 전달 방식 구조
- ? : 여기서부터 전달할 데이터가 작성된다는 의미.
- & : 전달할 데이터가 더 있다는 뜻
- 예시) google.com/search?q=아이폰&sourceid=chrome&ie=UTF-8
    - 위 주소는 google.com의 search 창구에 다음 정보를 전달.
    - q=아이폰 (검색어) 
    - sourceid=chrome (브라우저 정보)
    - ie=UTF-8 (인코딩 정보)


## Ajax
- 서버에 데이터를 요청하고 받아보기 

## Ajax 기본 골격
- success: 성공시, response 값에 서버의 결과 값을 담아서 함수를 실행
```
$.ajax({
  type: "GET", // GET 방식으로 요청
  url: "http://openapi.seoul.go.kr:8088/6d4d776b466c656533356a4b4b5872/json/RealtimeCityAir/1/99",
  data: {}, // 요청하면서 함께 줄 데이터 (GET 요청시엔 비워서감)
  success: function(response){ // 서버에서 준 결과를 response라는 변수에 담음
    console.log(response) // 서버에서 준 결과를 이용해서 나머지 코드를 작성
  }
})
```

