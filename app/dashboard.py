import streamlit as st
import pandas as pd
import mysql.connector
import folium
from folium.plugins import MarkerCluster

# MySQL 연결 함수
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="yezi",
        password="080703",
        database="roadkill_db"
    )

# DB에서 로드킬 데이터를 가져오는 함수
def get_roadkill_data():
    conn = get_db_connection()
    cursor = conn.cursor()

    # 데이터베이스에서 로드킬 데이터 가져오기
    cursor.execute("SELECT latitude, longitude, address1, address2, address3, description FROM roadkill")
    data = cursor.fetchall()

    # 데이터프레임으로 변환
    df = pd.DataFrame(data, columns=["latitude", "longitude", "address1", "address2", "address3", "description"])

    cursor.close()
    conn.close()

    return df

# Streamlit 대시보드 생성
def create_dashboard():
    st.title("로드킬 발생 현황 대시보드")

    # DB에서 로드킬 데이터 가져오기
    df = get_roadkill_data()

    # 지도 생성
    map_center = [df['latitude'].mean(), df['longitude'].mean()]  # 평균 위도, 경도로 지도 중심 설정
    roadkill_map = folium.Map(location=map_center, zoom_start=12)

    # 마커 클러스터링
    marker_cluster = MarkerCluster().add_to(roadkill_map)

    # 데이터에 따른 마커 추가
    for idx, row in df.iterrows():
        folium.Marker(
            location=[row['latitude'], row['longitude']],
            popup=f"{row['address1']}<br>{row['address2']}<br>{row['address3']}",
        ).add_to(marker_cluster)

    # Streamlit에 지도 표시
    st.subheader("로드킬 지도")
    st.write(roadkill_map)

    # 지역별 발생 현황
    st.subheader("지역별 발생 현황")
    region_counts = df['address1'].value_counts()
    st.bar_chart(region_counts)

if __name__ == "__main__":
    create_dashboard()
