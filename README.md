# ComMoni

서버에서 수집한 실시간 데이터를 이용하여 모니터링을 할 수 있는 기능을 제공합니다.

## 모니터링으로 수집할 데이터

* CPU 사용률
* 메모리 사용률
* 디스크 사용률

## DB 설계

### User (사용자)

- user_id : 사용자 아이디
- user_pw : 사용자 비밀번호
- user_name : 사용자 이름
- deleted : 삭제 여부

### ComManage (원격 호스트 관리)

- host_id : 호스트 아이디
- user_id : 사용자 아이디
- host_name : 호스트 이름
- host_ip : 호스트 아이피
- memory : 메모리 용량
- disk : 디스크 용량
-
    - deleted : 삭제 여부

### ComInfo (모니터링 데이터)

- sequence : 시퀀스번호
- host_id : 호스트 아이디
- cpu_utilization : cpu 사용률
- memory_utilization : 메모리 사용률
- disk__utilization : 디스크 사용률
- make_datetime : 데이터 생성 날짜/시간

### ComInfoRT (실시간 모니터링 데이터)

- host_id : 호스트 아이디
- cpu_utilization : cpu 사용률
- memory_utilization : 메모리 사용률
- disk__utilization : 디스크 사용률
- make_time : 데이터 생성 시간
- update_datetime : 데이터 수정 시간

> site url : https://www.erdcloud.com/d/YaWGWhvWW8xpwqPxE

## 프로젝트 구조

### Server

* app
    * api
        * auth : 로그인 관련
        * cominfo : 모니터링 관련
        * commanage : 모니터링 대상 관리
        * exception : api 예외
        * user : 사용자 관련
    * common : 공통 코드
    * configs : 설정 관련
    * db_init : orm 디비 초기화 관련
    * tests : 테스트
    * database.py : 뎅터베이스 설정
    * main.py : 파이썬 메인


