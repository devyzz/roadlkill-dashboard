import pandas as pd
import mysql.connector
import os
import chardet

# MySQL 연결
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="yezi",
        password="080703",
        database="roadkill_db"
    )

# CSV 파일을 DB에 저장하는 함수
def load_csv_to_db(csv_file):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    with open(csv_file, 'rb') as f:
        result = chardet.detect(f.read())
        print(result)

    # CSV 파일 읽기
    # df = pd.read_csv(csv_file)
    df = pd.read_csv(csv_file, encoding='EUC-KR')

    # 컬럼명 매핑
    column_mapping = {
        '위도': 'latitude',
        '경도': 'longitude',
        '발생건수': 'cnt',
        '본부명': 'address1',
        '지사명': 'address2',
        '노선명': 'address3',
        '구간': 'description'
    }
    df.rename(columns=column_mapping, inplace=True)

    # 데이터 타입 변환
    # df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce')
    df['longitude'] = pd.to_numeric(df['longitude'], errors='coerce')

    # DB 삽입 쿼리
    insert_query = """
        INSERT INTO roadkill (latitude, longitude, cnt, address1, address2, address3, description)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    
    # 데이터 삽입
    for index, row in df.iterrows():
        cursor.execute(insert_query, (
            row['latitude'],
            row['longitude'],
            row['cnt'],
            row['address1'],
            row['address2'],
            row['address3'],                   
            row['description']
        ))

    # 커밋 및 종료
    conn.commit()
    cursor.close()
    conn.close()

    print("CSV 데이터가 DB에 저장되었습니다.")

if __name__ == "__main__":
    csv_file = os.path.join("data", "roadkill_data_20231231.csv")  # CSV 파일 경로
    load_csv_to_db(csv_file)
