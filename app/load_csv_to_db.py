import pandas as pd
import mysql.connector
import os
import chardet
import re

# MySQL 연결
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="080703",
        database="roadkill_db",
        auth_plugin="caching_sha2_password"
    )
# reverse 매핑
reverse_column_mapping = {
    'latitude': ['위도', 'lat', 'Latitude'],
    'longitude': ['경도', 'lon', 'Longitude'],
    'cnt': ['발생건수',  '건수', 'count'],
    'address1': ['본부명', '지역1'],
    'address2': ['지사명', '지역2'],
    'address3': ['노선명', '도로명'],
    'description': ['구간', '세부위치', '비고']
}

def find_column(df, candidates):
    for col in df.columns:
        for candidate in candidates:
            if candidate in col:
                return col
    return None

def load_csv_to_db(csv_file):
    conn = get_db_connection()
    cursor = conn.cursor()

    # 연도 추출 (파일명에서 숫자 4자리 추출)
    match = re.search(r'(\d{4})', os.path.basename(csv_file))
    year = int(match.group(1)) if match else None

    with open(csv_file, 'rb') as f:
        result = chardet.detect(f.read())

    df = pd.read_csv(csv_file, encoding=result['encoding'])

    # 컬럼 자동 매핑
    mapped = {}
    for key, candidates in reverse_column_mapping.items():
        col_name = find_column(df, candidates)
        if col_name:
            mapped[key] = col_name

    df = df.rename(columns={v: k for k, v in mapped.items()})

    # 필요한 컬럼만 추출
    required_cols = ['latitude', 'longitude', 'cnt', 'address1', 'address2', 'address3', 'description']
    for col in required_cols:
        if col not in df.columns:
            df[col] = None  # 없는 컬럼은 NULL로 채움

    # 타입 정제
    df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce')
    df['longitude'] = pd.to_numeric(df['longitude'], errors='coerce')

    # year 컬럼 추가
    df['year'] = year

    insert_query = """
        INSERT INTO roadkill (latitude, longitude, cnt, address1, address2, address3, description, year)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """

    for _, row in df.iterrows():
        values = tuple(None if pd.isna(x) else x for x in [
            row['latitude'],
            row['longitude'],
            row['cnt'],
            row['address1'],
            row['address2'],
            row['address3'],
            row['description'],
            row['year']
        ])

        # 필수값이 없으면 스킵
        if values[0] is None or values[1] is None:
            print(f"[SKIP] 위치정보 없음: latitude={values[0]}, longitude={values[1]}")
            continue

        cursor.execute(insert_query, values)

    conn.commit()
    cursor.close()
    conn.close()
    print(f"{csv_file} → DB 저장 완료")


def load_stats_csv_to_db(csv_file):
    conn = get_db_connection()
    cursor = conn.cursor()

    # 파일 인코딩 감지
    with open(csv_file, 'rb') as f:
        result = chardet.detect(f.read())

    # CSV 파일 읽기
    df = pd.read_csv(csv_file, encoding=result['encoding'])
    
    # 컬럼명 확인
    print("📌 컬럼명 확인:", df.columns.tolist())
    print(df.head(3))

    # Null 처리 및 타입 변환
    df['month'] = pd.to_numeric(df['month'], errors='coerce')
    df['count'] = pd.to_numeric(df['count'], errors='coerce')

    # NaN을 None으로 변환
    df = df.where(pd.notnull(df), None)

    # ✅ NaN 또는 "null"/"nan" 같은 문자열을 확실하게 None으로 처리
    def safe(x):
        if pd.isna(x):
            return None
        x_str = str(x).strip().lower()
        if x_str in ["", "nan", "null", "none", "na"]:
            return None
        return x

    # 데이터 삽입 쿼리
    insert_query = """
        INSERT INTO roadkill_stats (year, month, region, road_type, animal, count, stat_type)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """

    for _, row in df.iterrows():
        values = tuple(safe(row[col]) for col in ['year', 'month', 'region', 'road_type', 'animal', 'count', 'stat_type'])

        # 필수값 누락 시 스킵
        if values[0] is None or values[5] is None or values[6] is None:
            print(f"[SKIP] 필수값 누락: {values}")
            continue

        # 데이터 삽입
        cursor.execute(insert_query, values)

    # DB에 커밋 후 연결 종료
    conn.commit()
    cursor.close()
    conn.close()

    print(f"{csv_file} → 통계 DB 저장 완료")

# 전체 폴더 반복
def load_all_csvs(data_dir):
    for file in os.listdir(data_dir):
        if file.endswith(".csv"):
            full_path = os.path.join(data_dir, file)

            # 파일 이름에 "통계" 또는 "stats" 등 키워드가 포함된 경우 구분
            if 'stats' in file.lower() or '통계' in file:
                load_stats_csv_to_db(full_path)
            else:
                load_csv_to_db(full_path)

if __name__ == "__main__":
    load_all_csvs("data")  # "data" 폴더 안의 모든 CSV 처리