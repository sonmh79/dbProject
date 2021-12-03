# 21-2 소프트웨어 실습 기말 프로젝트

### 주제 

PyQt5, MySQL을 사용해 학생 관리 프로그램 만들기

### 내용

교수의 입장에서 강의를 수강하고 있는 학생들의 출결, 성적, 학점 등을 조작, 관리할 수 있는 프로그램 만들기

### 목적

데이터베이스 공부

### 구현한 기능

로그인, DB에서 데이터 불러오기, 화면에서 직접 수정, 수강생 검색, 강제 입력 / 삭제, 학점 관리 등

## ER 다이어그램

<img width="500" alt="다이어그램" src="https://user-images.githubusercontent.com/78152114/144629698-5afa2ea2-c5fb-4540-a44f-3f59b564c63e.png">

STUDENT(id, name, department)  
PROFESSOR(id, pw, name)  
CLASS(classid, semester, subject, pid)  
ATTEND(classid, semester, studentid, aid, hid, tid, grade)  
ATTENDANCE(id, score)  
HOMEWORK(id, score)  
TEST(id, midterm, finals)  

* 총 7개의 테이블
* 메인 테이블은 attend테이블로 강의를 수강하는 학생에 대한 정보를 포함한다.
* 학생이 강의를 수강하게 되면 출석, 과제, 시험에 대한 테이블인 attendance, homework, test에서 각각 새로운 레코드를 생성하고 attend에서 참조한다.

## 실행화면

<img width="500" alt="실행화면" src="https://user-images.githubusercontent.com/78152114/144632363-d5942d71-38b2-4890-812f-a3c96e3819a5.png">

## 1. 로그인

<img width="500" alt="로그인화면" src="https://user-images.githubusercontent.com/78152114/144629493-2f3989e9-8c29-446d-8990-c7457021a0ea.png">

화면에서 id와 pw를 입력받아 교수 테이블에서 일치하는 레코드가 있는지 확인한다.

로그인 성공 시, 로그인 윈도우를 종료하면서 교수 id를 반환하고 이 값을 메인 윈도우에서 넘겨받아 host를 식별한다.

## 2. 메인 테이블

<img width="500" alt="메인 테이블" src="https://user-images.githubusercontent.com/78152114/144629513-2ef39b32-e972-4afe-adbd-16f59d317083.png">

DB -> Dataframe(pandas) -> QTablewidget 순으로 데이터를 처리해서 보여준다.

직접 수정하길 원하는 행을 클릭하면, 테이블 아래에 해당하는 정보들이 나오고 편집 후 update를 클릭하여 수정한다.

테이블의 헤더를 클릭 시, 오름차순 내림차순으로 정렬할 수 있다.

## 3. 검색

<img width="500" alt="검색" src="https://user-images.githubusercontent.com/78152114/144629560-9f1634e2-7888-422e-925e-f1f1241eb56e.png">

강의를 수강하고 있는 학생들을 직접 검색할 수 있다.

## 4. 강제 입력 / 삭제

<img width="500" alt="강제 입력 삭제" src="https://user-images.githubusercontent.com/78152114/144629583-567872d1-86c1-45be-99cd-c8e84c50ac51.png">

강제 입력 또는 삭제하고자 하는 학생의 학번, 이름, 학과를 입력해 입력 또는 삭제할 수 있다.

단, 해당하는 학생이 student 테이블에 존재하여야 한다.

강제 입력 시, attendance, homework, test 테이블에서 각각 레코드가 생성되며 새로운 학생의 정보와 함께 attend테이블에 포함된다.

## 5. 학점 관리

<img width="500" alt="학점 관리" src="https://user-images.githubusercontent.com/78152114/144629592-abdb61cc-c0dd-42e7-bf47-529d18a2430c.png">

성적 산출을 위한 비율을 직접 지정할 수 있다.

절대평가 방식으로 각 학점 별 커트라인을 지정할 수 있으며, 산출 버튼을 클릭 시 이에 대한 비율이 계산된다.

산출된 비율을 보고 커트라인을 조정할 수 있다.

최종 성적이 확정되면, 엑셀로 저장 버튼을 통해 테이블의 내용을 엑셀로 저장할 수 있다.






