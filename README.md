# 🦊 Roadkill Dashboard

> 도로 위 로드킬 데이터를 시각화하여 지역별 현황을 쉽게 파악할 수 있도록 만든 대시보드입니다.

---

## 📌 프로젝트 소개

로드킬은 운전자와 야생동물 모두에게 치명적인 사고로 이어질 수 있습니다.  
본 대시보드는 **공공데이터 포털의 로드킬 데이터를 시각화**하여,  
지역별 발생 현황을 분석하고 **사고 예방을 위한 인사이트**를 제공하는 것을 목표로 합니다.

- 🗺️ 지역별 로드킬 발생 분포 시각화  
- 📊 연도별, 계절별, 도로 유형별 분석  
- 📍 Streamlit 기반 웹 대시보드 UI  

---

## 🛠 기술 스택

| 목적 | 기술 |
|------|------|
| 데이터 처리 | Python, Pandas |
| 시각화 | Plotly, Altair, Streamlit |
| 프론트엔드 대시보드 | Streamlit |
| 배포(예정) | Docker, GitHub Pages (또는 Streamlit Community Cloud) |

---

## 📂 프로젝트 구조

```bash
roadlkill-dashboard/
├── data/                  # 원본 및 전처리된 CSV 파일
├── dashboard.py           # Streamlit 앱 메인 파일
├── preprocessing.py       # 데이터 전처리 모듈
├── requirements.txt       # 의존성 목록
└── README.md              # 프로젝트 소개 문서
