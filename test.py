import streamlit as st
import pandas as pd
import altair as alt
import random
import os
from datetime import datetime

# =========================
# 기본 설정
# =========================
st.set_page_config(page_title="공부 기록 다이어리", page_icon="📚", layout="wide")
DATA_FILE = "study_log.csv"

# 동기부여 문구
quotes = [
    "오늘의 작은 노력이 내일의 큰 성과를 만든다!",
    "포기하지 마라, 끝까지 해보자!",
    "너의 한 시간은 결코 헛되지 않다.",
    "꾸준함이 최고의 무기다.",
    "오늘도 한 걸음 성장했어!",
    "노력은 배신하지 않는다."
]

# =========================
# 데이터 불러오기
# =========================
if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
else:
    df = pd.DataFrame(columns=["날짜", "과목", "목표", "공부시간(분)", "메모", "공부 내용"])

# =========================
# 날짜 안전 처리
# =========================
if not df.empty:
    df["날짜"] = pd.to_datetime(df["날짜"], errors="coerce")
    df = df.dropna(subset=["날짜"])

# =========================
# 사이드바 설정
# =========================
st.sidebar.header("🎨 개인 설정")
theme_color = st.sidebar.color_picker("테마 색상 선택", "#4CAF50")
icon = st.sidebar.selectbox("아이콘 선택", ["📚", "📝", "⏳", "📈", "🎯"])

st.markdown(f"<h1 style='color:{theme_color}'>{icon} 공부 기록 다이어리</h1>", unsafe_allow_html=True)

# =========================
# 입력 폼
# =========================
with st.form("study_form"):
    st.subheader("✏️ 오늘의 공부 기록")
    subject = st.text_input("과목")
    goal = st.text_input("오늘 목표")
    time = st.number_input("공부시간(분)", min_value=0, step=10)
    memo = st.text_area("간단 메모")
    content = st.text_area("공부 내용", placeholder="오늘 공부한 내용을 기록해보세요.")
    submitted = st.form_submit_button("저장")

    if submitted:
        if not subject:
            st.warning("과목을 입력하세요")
        elif time <= 0:
            st.warning("공부 시간을 입력하세요")
        else:
            new_data = pd.DataFrame({
                "날짜": [datetime.now().strftime("%Y-%m-%d")],
                "과목": [subject],
                "목표": [goal],
                "공부시간(분)": [time],
                "메모": [memo],
                "공부 내용": [content]
            })
            df = pd.concat([df, new_data], ignore_index=True)
            df.to_csv(DATA_FILE, index=False)
            st.success("✅ 저장 완료!")

# =========================
# 동기부여 문구
# =========================
st.subheader("💬 오늘의 동기부여")
random.seed(datetime.now().date().toordinal())
quote = random.choice(quotes)
st.info(quote)

# =========================
# 전체 기록 확인
# =========================
st.subheader("📚 전체 공부 기록")
if not df.empty:
    df_sorted = df.sort_values(by="날짜", ascending=False)
    for i, row in df_sorted.iterrows():
        with st.expander(f"{row['날짜']} - {row['과목']} ({row['공부시간(분)']}분)"):
            st.markdown(f"**목표:** {row['목표']}")
            st.markdown(f"**메모:** {row.get('메모','')}")
            st.markdown(f"**공부 내용:** {row.get('공부 내용','')}")

# =========================
# 과목별 공부 내용 확인
# =========================
if not df.empty:
    st.subheader("📝 과목별 공부 내용 확인")
    subjects = df["과목"].unique().tolist()
    selected_subject = st.selectbox("확인할 과목 선택", ["전체"] + subjects)

    if selected_subject == "전체":
        filtered_df = df
    else:
        filtered_df = df[df["과목"] == selected_subject]

    if filtered_df.empty:
        st.info("해당 과목의 기록이 없습니다.")
    else:
        filtered_df = filtered_df.sort_values(by="날짜", ascending=False)
        for i, row in filtered_df.iterrows():
            with st.expander(f"{row['날짜']} - {row['과목']} ({row['공부시간(분)']}분)"):
                st.markdown(f"**목표:** {row['목표']}")
                st.markdown(f"**메모:** {row.get('메모','')}")
                st.markdown(f"**공부 내용:** {row.get('공부 내용','')}")

# =========================
# 공부 시간 통계
# =========================
if not df.empty:
    st.subheader("📊 공부 시간 통계")

    # 안전하게 datetime 변환
    df["날짜"] = pd.to_datetime(df["날짜"], errors="coerce")
    df = df.dropna(subset=["날짜"])

    # 일별 합계
    daily = df.groupby("날짜")["공부시간(분)"].sum().reset_index()
    daily_chart = alt.Chart(daily).mark_bar(color=theme_color).encode(
        x=alt.X("날짜:T", title="날짜"),
        y=alt.Y("공부시간(분):Q", title="공부 시간(분)")
    ).properties(title="일별 공부 시간")

    # 주차별 합계
    df["주차"] = df["날짜"].dt.to_period("W").apply(lambda r: r.start_time)
    weekly = df.groupby("주차")["공부시간(분)"].sum().reset_index()
    weekly_chart = alt.Chart(weekly).mark_line(point=True, color=theme_color).encode(
        x=alt.X("주차:T", title="주차 시작일"),
        y=alt.Y("공부시간(분):Q", title="공부 시간(분)")
    ).properties(title="주차별 공부 시간")

    # 월별 합계
    df["월"] = df["날짜"].dt.to_period("M").apply(lambda r: r.start_time)
    monthly = df.groupby("월")["공부시간(분)"].sum().reset_index()
    monthly_chart = alt.Chart(monthly).mark_area(color=theme_color, opacity=0.6).encode(
        x=alt.X("월:T", title="월"),
        y=alt.Y("공부시간(분):Q", title="공부 시간(분)")
    ).properties(title="월별 공부 시간")

    st.altair_chart(daily_chart, use_container_width=True)
    st.altair_chart(weekly_chart, use_container_width=True)
    st.altair_chart(monthly_chart, use_container_width=True)

    # 과목별 비율
    subject_total = df.groupby("과목")["공부시간(분)"].sum().reset_index()
    st.subheader("📌 과목별 공부 시간 비율")
    st.dataframe(subject_total)
else:
    st.warning("아직 기록이 없습니다. 오늘의 첫 공부를 기록해보세요! ✨")

