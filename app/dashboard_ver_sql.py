import streamlit as st
import pandas as pd
import mysql.connector
import altair as alt

# MySQL 연결 함수
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="080703",
        database="roadkill_db",
        auth_plugin="caching_sha2_password"
    )

# 지도 데이터
def fetch_map_data():
    query = """
        SELECT latitude, longitude 
        FROM roadkill 
        WHERE latitude IS NOT NULL AND longitude IS NOT NULL
    """
    conn = get_db_connection()
    df = pd.read_sql(query, conn)
    conn.close()
    return df.astype(float)

# 지역별 로드킬 수
def fetch_region_counts():
    query = """
        SELECT address1 AS region, COUNT(*) AS count
        FROM roadkill
        WHERE address1 IS NOT NULL
        GROUP BY address1
        ORDER BY count DESC
    """
    conn = get_db_connection()
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# 연도별 로드킬 수
def fetch_year_counts():
    query = """
        SELECT year, COUNT(*) AS count
        FROM roadkill
        WHERE year IS NOT NULL
        GROUP BY year
        ORDER BY year
    """
    conn = get_db_connection()
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# 월별 추이 (꺾은선 그래프용)
def fetch_monthly_trend():
    query = """
        SELECT year, month, SUM(count) AS count
        FROM roadkill_stats
        WHERE stat_type = '월별'
        GROUP BY year, month
        ORDER BY year, month
    """
    conn = get_db_connection()
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# 권역별 연도별 막대 그래프
def fetch_region_year_data():
    query = """
        SELECT year, region, SUM(count) AS count
        FROM roadkill_stats
        WHERE stat_type = '권역별'
        GROUP BY year, region
    """
    conn = get_db_connection()
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# 종별 연도별 막대 그래프
def fetch_animal_year_data():
    query = """
        SELECT year, animal, SUM(count) AS count
        FROM roadkill_stats
        WHERE stat_type = '종별'
        GROUP BY year, animal
    """
    conn = get_db_connection()
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# 대시보드
def create_dashboard():
    st.title("로드킬 발생 현황 대시보드")

    # 지도 시각화
    st.subheader("로드킬 발생 지도")
    st.map(fetch_map_data())

    # 지역별 발생 현황
    st.subheader("지역별 로드킬 수")
    region_df = fetch_region_counts()
    st.bar_chart(region_df.set_index("region"))

    # 연도별 발생 현황
    st.subheader("연도별 로드킬 수")
    year_df = fetch_year_counts()
    st.bar_chart(year_df.set_index("year"))

    # 월별 추이 꺾은선 그래프
    st.subheader("연도별 월별 로드킬 추이")
    month_df = fetch_monthly_trend()
    chart = alt.Chart(month_df).mark_line(point=True).encode(
        x=alt.X("month:O", title="월"),
        y=alt.Y("count:Q", title="로드킬 수"),
        color="year:N",
        tooltip=["year", "month", "count"]
    ).properties(width=700, height=400)
    st.altair_chart(chart)

    # 권역별 & 종별 데이터
    region_stat_df = fetch_region_year_data()
    animal_stat_df = fetch_animal_year_data()

    # 연도 선택
    st.subheader("연도 선택별 세부 통계")
    years = sorted(region_stat_df["year"].unique())
    selected_year = st.selectbox("연도를 선택하세요", years, index=0)

    # 권역별 막대 그래프
    st.subheader("권역별 로드킬 수")
    region_filtered = region_stat_df[region_stat_df["year"] == selected_year]
    chart1 = alt.Chart(region_filtered).mark_bar().encode(
        x=alt.X("region:N", title="지역"),
        y=alt.Y("count:Q", title="로드킬 수"),
        color="year:N",
        tooltip=["region", "count"]
    ).properties(width=700, height=400)
    st.altair_chart(chart1)

    # 동물종별 막대 그래프
    st.subheader("동물종별 로드킬 수")
    animal_filtered = animal_stat_df[animal_stat_df["year"] == selected_year]
    chart2 = alt.Chart(animal_filtered).mark_bar().encode(
        x=alt.X("animal:N", title="종"),
        y=alt.Y("count:Q", title="로드킬 수"),
        color="year:N",
        tooltip=["animal", "count"]
    ).properties(width=700, height=400)
    st.altair_chart(chart2)

    # 누적 가로 막대그래프
    st.subheader("종별 연도별 누적 로드킬 수")
    chart3 = alt.Chart(animal_stat_df).mark_bar().encode(
        y=alt.Y("animal:N", title="종"),
        x=alt.X("count:Q", title="로드킬 수", stack="zero"),
        color=alt.Color("year:N", title="연도"),
        tooltip=["animal", "year", "count"]
    ).properties(width=700, height=400)
    st.altair_chart(chart3)

if __name__ == "__main__":
    create_dashboard()
