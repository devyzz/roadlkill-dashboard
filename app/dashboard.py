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

# DB에서 로드킬 데이터를 가져오는 함수
def get_roadkill_data():
    conn = get_db_connection()
    cursor = conn.cursor()

    # 데이터베이스에서 로드킬 데이터 가져오기
    cursor.execute("SELECT latitude, longitude, year, address1, address2, address3, description FROM roadkill")
    data = cursor.fetchall()

    # 데이터프레임으로 변환
    df = pd.DataFrame(data, columns=["latitude", "longitude", "year", "address1", "address2", "address3", "description"])

    cursor.close()
    conn.close()

    return df


def get_roadkill_stat_data():
    conn = get_db_connection()
    cursor = conn.cursor()

    # 데이터베이스에서 로드킬 데이터 가져오기
    cursor.execute("SELECT year, month, region, road_type, animal, count, stat_type FROM roadkill_stats")
    data = cursor.fetchall()

    # 데이터프레임으로 변환
    df = pd.DataFrame(data, columns=["year", "month", "region", "road_type", "animal", "count", "stat_type"])

    cursor.close()
    conn.close()

    return df

# Streamlit 대시보드 생성
def create_dashboard():
    st.title("로드킬 발생 현황 대시보드")

    # DB에서 로드킬 데이터 가져오기
    df = get_roadkill_data()
    df_stat = get_roadkill_stat_data()

    st.subheader("로드킬 발생 지도")
    
    # latitude, longitude가 float 타입인지 확인
    df['latitude'] = df['latitude'].astype(float)
    df['longitude'] = df['longitude'].astype(float)

    # 지도 시각화
    st.map(df[['latitude', 'longitude']])


    st.subheader("지역별 발생 현황")
    region_counts = df['address1'].value_counts()
    st.bar_chart(region_counts)
    
    st.subheader("연도별 발생 현황")
    year_counts = df['year'].value_counts()
    st.bar_chart(year_counts)
    
    
    #---------------------------------------------
    # 국립 생태원 통계데이터를 통해 그린 차트
    #---------------------------------------------

    # 연도별 월별 꺾은선 그래프
    st.subheader("월별 로드킬 추이 꺾은선 그래프")
    month_df = df_stat[df_stat["stat_type"] == "월별"].dropna(subset=["month"])
    chart2 = alt.Chart(month_df).mark_line(point=True).encode(
        x=alt.X("month:O", title="월", axis=alt.Axis(labelAngle=0)),
        y=alt.Y("count:Q", title="로드킬 수"),
        color="year:N",
        tooltip=["year", "month", "count"]
    ).properties(width=700, height=400)
    st.altair_chart(chart2)


    # 연도 + 지역 통합그래프
    st.subheader("연도별 권역별 로드킬 수 연도통합")
    region_df = df_stat[df_stat["stat_type"] == "권역별"].dropna(subset=["region"])
    chart3 = alt.Chart(region_df).mark_bar().encode(
        x=alt.X("region:N", title="지역", sort='x', axis=alt.Axis(labelAngle=0)),
        y=alt.Y("count:Q", title="로드킬 수"),
        color="year:N",
        tooltip=["year", "region", "count"]
    ).properties(width=700, height=400)
    st.altair_chart(chart3)
    
    # 연도 + 동물 통합그래프
    st.subheader("연도별 동물별 로드킬 수 연도통합")
    a_df = df_stat[df_stat["stat_type"] == "종별"].dropna(subset=["animal"])
    chart3 = alt.Chart(a_df).mark_bar().encode(
        x=alt.X("animal:N", title="종", sort='x', axis=alt.Axis(labelAngle=0)),
        y=alt.Y("count:Q", title="로드킬 수"),
        color="year:N",
        tooltip=["year", "animal", "count"]
    ).properties(width=700, height=400)
    st.altair_chart(chart3)
    
    #---------------------------------------------
    # 하나의 셀렉트 박스로 3개의 막대그래프 통제
    #---------------------------------------------

    # 연도 선택 박스 (하나의 selectbox로 두 그래프 연동)
    selected_year = st.selectbox(
        "연도를 선택하세요",
        options=df_stat["year"].unique(),
        index=0  # 기본값은 첫 번째 연도
    )

    # 1. 권역별 데이터 필터링
    st.subheader("연도별 권역별 로드킬 발생 수 (막대 그래프)")
    region_df = df_stat[(df_stat["stat_type"] == "권역별") & (df_stat["year"] == selected_year)].dropna(subset=["region"])
    
    chart_region = alt.Chart(region_df).mark_bar().encode(
        x=alt.X("region:N", title="지역", sort='x', axis=alt.Axis(labelAngle=0)),
        y=alt.Y("count:Q", title="로드킬 수"),
        color="year:N",
        tooltip=["year", "region", "count"]
    ).properties(width=700, height=400)

    st.altair_chart(chart_region)

    # 2. 동물종별 데이터 필터링
    st.subheader("연도별 동물종별 로드킬 수 (막대 그래프)")
    animal_df = df_stat[(df_stat["stat_type"] == "종별") & (df_stat["year"] == selected_year)].dropna(subset=["animal"])

    chart_animal = alt.Chart(animal_df).mark_bar().encode(
        x=alt.X("animal:N", title="동물", sort='x', axis=alt.Axis(labelAngle=0)),
        y=alt.Y("count:Q", title="로드킬 수"),
        color="year:N",
        tooltip=["year", "animal", "count"]
    ).properties(width=700, height=400)

    st.altair_chart(chart_animal)

    # 3. 월별 데이터 필터링
    st.subheader("연도별 월별 로드킬 수 (막대 그래프)")
    month_df = df_stat[(df_stat["stat_type"] == "월별") & (df_stat["year"] == selected_year)].dropna(subset=["month"])

    chart_month = alt.Chart(month_df).mark_bar().encode(
        x=alt.X("month:N", title="월", sort='x', axis=alt.Axis(labelAngle=0)),
        y=alt.Y("count:Q", title="로드킬 수"),
        color="year:N",
        tooltip=["year", "month", "count"]
    ).properties(width=700, height=400)

    st.altair_chart(chart_month)
    
    
    #---------------------------------------------
    # 종별 스택형태 그래프
    #---------------------------------------------
    
    stack_df = df_stat[df_stat["stat_type"] == "종별"].dropna(subset=["animal", "year", "count"])

    # 누적 가로 막대 그래프
    chart = alt.Chart(stack_df).mark_bar().encode(
        y=alt.Y("animal:N", title="종"),
        x=alt.X("count:Q", title="로드킬 수", stack="zero"),
        color=alt.Color("year:N", title="연도"),
        tooltip=["animal", "year", "count"]
    ).properties(
        width=700,
        height=400,
        title="종별 연도별 로드킬 수"
    )

    st.subheader("종별 연도별 로드킬 누적 가로 막대그래프")
    st.altair_chart(chart)
    #---------------------------------------------
    # 셀렉트박스 + 기준2개
    #---------------------------------------------

    # st.subheader("연도별 동물 종별 로드킬 수 (막대 그래프)")

    # # 동물 유형 리스트 (전체 포함)
    # available_animal_types = df_stat[df_stat["stat_type"] == "종별"]["animal"].dropna().unique().tolist()
    # available_animal_types.sort()

    # # selectbox로 도로 유형 선택
    # selected_animal_type = st.selectbox("동물을 선택하세요:", available_animal_types)

    # # 필터링
    # species_df = df_stat[(df_stat["stat_type"] == "종별") &
    #                     (df_stat["animal"] == selected_animal_type)].dropna(subset=["road_type"])

    # # 차트 그리기
    # chart_all = alt.Chart(species_df).mark_bar().encode(
    #     x=alt.X("road_type:N", title="도로유형", axis=alt.Axis(labelAngle=0)),
    #     y=alt.Y("count:Q", title="로드킬 수"),
    #     color="year:N",
    #     column=alt.Column("year:N", title="연도별", spacing=10),
    #     tooltip=["year", "animal", "count", "road_type"]
    # ).properties(width=150, height=300)
    # st.altair_chart(chart_all)

if __name__ == "__main__":
    create_dashboard()
