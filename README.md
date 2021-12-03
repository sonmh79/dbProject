# 21-2 소프트웨어 실습 기말 프로젝트

### 주제 

PyQt5, MySQL을 사용해 학생 관리 프로그램 만들기

### 내용

교수의 입장에서 강의를 수강하고 있는 학생들의 출결, 성적, 학점 등을 조작, 관리할 수 있는 프로그램 만들기

### 의도

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


