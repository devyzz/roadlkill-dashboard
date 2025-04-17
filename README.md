# Roadkill Dashboard

공공데이터 포털에서 제공하는 로드킬 발생 데이터를 활용하여, 특정 지역 및 시간대에 발생한 사고들을 시각화하고 분석하는 대시보드를 제공.
- 🗺️ 지역별 로드킬 발생 분포 시각화  
- 📊 연도별, 종류별, 도로 유형별 분석  

| 목적 | 기술 |
|------|------|
| 데이터 처리 | Python, Pandas |
| 시각화 | Plotly, Altair, Streamlit |
| 프론트엔드 대시보드 | Streamlit |

## 기능

- **Streamlit**을 이용한 대시보드 구현
- CSV 파일을 데이터베이스에 적재하는 기능
- 사고 데이터를 시각화하여 대시보드에 표시

## 📂 프로젝트 구조 (ing)

```bash
roadlkill-dashboard/
├── 📂 app/                               # 주요 애플리케이션 코드
│   ├── 📄 dashboarda.py                  # 로드킬 데이터를 시각화하는 대시보드 구현
│   └── 📄 load_csv_to_db.py              # CSV 데이터를 DB 테이블로 변환 및 적재
├── 📂 data/                              # 공공데이터 포털에서 수집한 지역별 사고 데이터 저장소
├── 📄 requirements.txt                  # 의존성 목록
└── 📄 README.md                         # 프로젝트 소개 문서
```

## 설치 방법

1. **Python 3.8 이상** 확인
2. 프로젝트를 클론:

    ```bash
    git clone https://github.com/devyzz/roadlkill-dashboard.git
    cd roadlkill-dashboard
    ```
3. 필요한 패키지 설치:

    ```bash
    pip install -r requirements.txt
    ```

4. 데이터베이스 연결 및 테이블 쿼리.  
   `load_csv_to_db.py` 파일에서 데이터베이스 연결 정보를 본인의 mysql 정보로 수정.
   mysql 테이블 추가
   ```mysql
    CREATE TABLE roadkill (
      id INT AUTO_INCREMENT PRIMARY KEY,
      latitude DOUBLE NOT NULL,
      longitude DOUBLE NOT NULL,
      cnt INT NOT NULL,
      address1 VARCHAR(255) NOT NULL,
      address2 VARCHAR(255) NOT NULL,
      address3 VARCHAR(255) NOT NULL,
      year INT NOT NULL,
      description TEXT
    );
   ```
   ```mysql
    CREATE TABLE roadkill_stats (
        id INT AUTO_INCREMENT PRIMARY KEY,
        year INT NOT NULL,
        month INT NULL,
        region VARCHAR(50),
        road_type VARCHAR(50),
        animal VARCHAR(50),
        count INT NOT NULL,
        stat_type VARCHAR(20) NOT NULL
    );
   ```

## 실행 방법

### 1. CSV 데이터 로드

`load_csv_to_db.py`를 실행하여 CSV 데이터를 mysql 데이터베이스에 로드

```bash
python app/load_csv_to_db.py
```

### 2. 대시보드 실행 
localhost:8051 에서 확인
```bash
streamlit run app/dashboarda.py
```

### 3. 현재 확인 가능한 대시보드
<img src="https://github.com/user-attachments/assets/a5075f00-c351-45f8-b7ac-3ab5ddfcf588" width="400" />
<img src="https://github.com/user-attachments/assets/7a6e74fe-abb9-4689-9e23-6c848f089922" width="400" />

* 경도, 위도를 통한 [맵](https://docs.streamlit.io/develop/api-reference/charts/st.map) 활용
* 연도별, 지역별 [simple bar chart](https://docs.streamlit.io/develop/api-reference/charts/st.bar_chart) 활용 
* [한국도로공사 로드킬 데이터정보](https://www.data.go.kr/data/15045544/fileData.do) 데이터셋 이용

<img src="https://github.com/user-attachments/assets/cde2df8c-b112-4e84-aaa6-2224a0bd0dce" width="400" />
<img src="https://github.com/user-attachments/assets/e1ffd714-2695-48f8-88f6-84d2e6c7f2da" width="400" />
<img src="https://github.com/user-attachments/assets/5a61e94b-5990-469a-a01c-6a2bec360493" width="400" />

* 연도별, 월별, 권역별 종별 [altair chart](https://docs.streamlit.io/develop/api-reference/charts/st.altair_chart) 활용 
* 데이터 형태 테스트 - (좌측) 꺾은선, 막대그래프, 가로막대그래프 / (우측) 연도를 셀렉트박스로 선택하는 형태의 막대그래프 
* [국립생태원 동물 찻길 사고 현황자료](https://www.data.go.kr/data/15100280/fileData.do) 를 직접 csv파일로 만든 후 데이터셋으로 이용

### 데이터 출처
[한국도로공사 로드킬 데이터정보](https://www.data.go.kr/data/15045544/fileData.do)<br>
[국립생태원 동물 찻길 사고 현황자료](https://www.data.go.kr/data/15100280/fileData.do)<br>
&rarr; data폴더 안에서 csv형태로 확인가능




