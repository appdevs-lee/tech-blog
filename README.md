# tech-blog
django로 개발한 기술 블로그

## ERD 설계
<img width="797" alt="스크린샷 2025-02-12 오전 12 29 04" src="https://github.com/user-attachments/assets/0d6960f3-e719-44c3-acdf-ecf162ded679" />

> **개발 기간** : 2024년 2월 5일 ~ 2024년 2월 11일 <br>

블로그를 쓰려고 할 때, 어떻게 써야 할 지 막막한 사람들을 위한 기술 블로그입니다.

## 시작 가이드
#### 가상환경 설정 및 라이브러리 설치
```
$ python -m venv venv
$ Mac: . ./venv/bin/activate
$ Window: .\venv\Scripts\activate
$ pip install -r requirements.txt
$ python manage.py makemigrations
$ python manage.py migrate
```
#### 서버 실행(택 1)
```
$ python manage.py runserver
```

## 기술 스택
* python 3.11.6, djanog 5.1.6, SQLite3
* html, css, js + Bootstrap

## 주요 기능
1. ~~로그인 및 회원가입~~
2. ~~글 CRUD~~
3. ~~댓글 CRUD~~
4. ~~조회수, 좋아요 기능~~
5. ~~markdown 미리보기~~
6. ~~markdown 가이드~~
7. topic에 따른 글 자동 생성

## API 명세서
### 로그인 및 회원가입
| 경로           | 메서드  | 설명   |
|--------------|------|------|
| /accounts/signup | post | 회원가입 |
| /accounts/login | post | 로그인  |
| /accounts/logout | post | 로그아웃 |
| /accounts/logout | post | 로그아웃 |
| /accounts/logout | post | 로그아웃 |

### 블로그 관련 API
| 경로           | 메서드  | 설명   |
|--------------|------|------|
| /blog/ | get | 게시글 조회 |
| /blog/post/new/ | post | 게시글 작성 |
| /post/<int:pk>/ | get | 게시글 상세 조회 |
| /post/<int:pk>/edit | post | 게시글 수정 |
| /post/<int:pk>/delete | post | 게시글 삭제 |
| /post/<int:pk>/like | post | 좋아요 추가 |
| comment/<int:pk>/create/ | post | 댓글 추가 |
| comment/<int:pk>/update/ | post | 댓글 수정 |
| comment/<int:pk>/delete/ | post | 댓글 삭제 |

