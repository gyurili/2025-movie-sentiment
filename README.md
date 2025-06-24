![image](https://github.com/user-attachments/assets/82cf0095-37c1-491c-bee1-e6b99e5cbe54)# 🎬 영화 리뷰 감정 분석


<br>

본 프로젝트는 사용자가 영화 정보를 등록하고, 해당 영화에 리뷰를 작성하면 **koBERT 모델**로 리뷰의 감정을 다섯 가지로 분석해주는 웹 서비스이다.  
전체 시스템은 **FastAPI 기반 백엔드**, **Streamlit 기반 프론트엔드**, **SQLite 데이터베이스**로 구성되었으며, 감정 분석은 HuggingFace의 [`jeonghyeon97/koBERT-Senti5`](https://huggingface.co/jeonghyeon97/koBERT-Senti5) 모델을 활용하였다. 개발 및 배포는 Google Cloud Platform(GCP) 환경에서 이루어졌다.


<br>

## 🔍 주요 기능

### ➊ ➕ 영화 추가  
![image](https://github.com/user-attachments/assets/59fec9d2-af78-483d-8391-8c011c23d71c)
- 영화 제목, 개봉일, 감독, 장르, 포스터 이미지 URL을 입력하여 **새로운 영화를 등록**한다.
- 등록된 영화는 **📋 등록된 영화 목록**으로 넘어가 확인할 수 있다.

<br>

### ➋ 📋 등록된 영화 목록

1) **영화 목록 조회**
![image](https://github.com/user-attachments/assets/122f57b1-46b1-47dc-9f8b-3e8d233d60f9)
- 📋 등록된 영화 목록에서 영화를 선택하면 상세 정보를 조회할 수 있다.

2) **영화 상세 정보 조회**
![image](https://github.com/user-attachments/assets/d43be887-455c-49ef-ac4f-61a0edc5b5eb)
- 선택한 영화의 제목, 개봉일, 감독, 장르, 포스터 이미지를 확인할 수 있다.
- **❌ 버튼**을 누르면 해당 영화가 **데이터베이스에서 삭제**된다.

3) **리뷰 작성 및 감정 분석**
![image](https://github.com/user-attachments/assets/72ba7703-48a1-45be-9f2e-371b230d1725)
- 리뷰를 등록하면 BERT가 **감정 분석**을 수행하고, **📢 최근 리뷰**로 넘어간다.
- 각 리뷰는 **🗑️ 버튼**으로 **삭제**할 수 있다.
- 전체 리뷰의 **평균 감성 점수**가 계산되며, 1~5점에 따라 **표정 이모지**가 표시된다.


<br>

## 🛠️ 기술 스택

| 분류        | 사용 기술                                       |
|-------------|------------------------------------------------|
| 프론트엔드  | Streamlit                                      |
| 백엔드      | FastAPI                               |
| AI 모델   | jeonghyeon97/koBERT-Senti5       |
| 데이터베이스| SQLite                             |
| 배포 | Google Cloud Platform        |

<br>

## 📦 설치 및 실행 방법

### 1. 설치

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 2. 실행

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
python -m streamlit run app.py
```

<br>


## 📁 프로젝트 구조

```
📁 project-root/
├── backend/
│   ├── model/
│   │   ├── database.py           # DB 연결 설정
│   │   ├── dto.py                # API 데이터 형태 정의
│   │   └── models.py             # 테이블 구조 정의
│   ├── api.py                    # API 엔드포인트 정의
│   ├── main.py                   # 백엔드 시작 파일
│   ├── sentiment.py              # 감정 분석
│   └── movies.db                 # SQLite 파일
├── frontend/
│   ├── app.py                    # 프론트엔드 시작 파일
│   ├── tab1.py                   # 탭1 화면 구성
│   └── tab2.py                   # 탭2 화면 구성
├── .gitignore
├── requirements.txt
└── README.md
```

<br>
