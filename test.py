import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import random
from datetime import datetime
import os

# -------------------------------
# CSV 데이터 로드 / 저장 함수
# -------------------------------
DATA_FILE = "study_data.csv"

def load_data():
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE, parse_dates=["날짜"])
        return df
    else:
        return pd.DataFrame(columns=["날짜", "과목", "공부시간", "목표", "공부내용", "메모"])

def save_data(df):
    df.to_csv(DATA_FILE, index=False)

# -------------------------------
# 초기 데이터 불러오기
# -------------------------------
df = load_data()

# -------------------------------
# 앱 제목
# -------------------------------
st.set_page_config(page_title="📚 공부 기록 다이어리", layout="wide")
st.title("📚 공부 기록 다이어리")

# -------------------------------
# 사이드바 설정
# -------------------------------
st.sidebar.header("⚙️ 설정")
theme_color = st.sidebar.color_picker("테마 색상 선택", "#4CAF50")
icon = st.sidebar.selectbox("아이콘 선택", ["📚", "📝", "📖", "🎯", "🔥"])

# -------------------------------
# 입력 영역
# -------------------------------
st.subheader(f"{icon} 오늘의 공부 기록 추가")
with st.form("record_form"):
    date = st.date_input("날짜", datetime.today())
    subject = st.text_input("공부 과목", placeholder="예: 수학, 영어, 과학")
    hours = st.number_input("공부 시간 (시간 단위)", min_value=0.0, step=0.5)
    goal = st.text_area("오늘의 목표", placeholder="오늘 공부 목표를 적어주세요")
    details = st.text_area("공부 내용", placeholder="오늘 공부한 세부 내용을 적어주세요")
    memo = st.text_area("간단 메모", placeholder="특이사항이나 메모를 적어주세요")
    submitted = st.form_submit_button("저장하기")

if submitted:
    if subject.strip() == "" or hours == 0.0:
        st.warning("⚠️ 과목과 공부 시간을 입력해주세요.")
    else:
        new_data = pd.DataFrame({
            "날짜": [pd.to_datetime(date)],
            "과목": [subject],
            "공부시간": [hours],
            "목표": [goal],
            "공부내용": [details],
            "메모": [memo]
        })
        df = pd.concat([df, new_data], ignore_index=True)
        save_data(df)
        st.success(f"✅ {subject} 공부 기록이 저장되었습니다!")

# -------------------------------
# 랜덤 동기부여 문구
# -------------------------------
motivations = [
    "작은 한 걸음이 큰 변화를 만든다! 💪",
    "오늘의 노력이 내일의 성장을 만든다 🌱",
    "포기하지 않는 것이 성공의 비결이다 🔥",
    "꾸준함이 최고의 실력이다 ✨",
    "오늘도 멋지게 해냈어! 🙌"
]
st.subheader("💡 오늘의 동기부여")
st.info(random.choice(motivations))

# -------------------------------
# 공부 기록 보기
# -------------------------------
st.subheader("📖 전체 공부 기록")
if df.empty:
    st.warning("아직 기록이 없습니다. 새로운 기록을 추가해주세요.")
else:
    subject_filter = st.multiselect("과목별 필터", options=df["과목"].unique())
    if subject_filter:
        filtered_df = df[df["과목"].isin(subject_filter)]
    else:
        filtered_df = df

    st.dataframe(filtered_df.sort_values("날짜", ascending=False))

# -------------------------------
# 공부 시간 분석 (그래프)
# -------------------------------
if not df.empty:
    st.subheader("📊 공부 시간 분석")

    # 날짜 변환
    df["날짜"] = pd.to_datetime(df["날짜"])
    df["주차"] = df["날짜"].dt.to_period("W").apply(lambda r: r.start_time)
    df["월"] = df["날짜"].dt.to_period("M").apply(lambda r: r.start_time)

    tab1, tab2, tab3 = st.tabs(["일별 그래프", "주별 그래프", "월별 그래프"])

    with tab1:
        daily = df.groupby("날짜")["공부시간"].sum()
        plt.figure(figsize=(8, 4))
        daily.plot(kind="bar")
        plt.title("일별 공부 시간")
        plt.ylabel("시간")
        st.pyplot(plt)

    with tab2:
        weekly = df.groupby("주차")["공부시간"].sum()
        plt.figure(figsize=(8, 4))
        weekly.plot(kind="bar")
        plt.title("주별 공부 시간")
        plt.ylabel("시간")
        st.pyplot(plt)

    with tab3:
        monthly = df.groupby("월")["공부시간"].sum()
        plt.figure(figsize=(8, 4))
        monthly.plot(kind="bar")
        plt.title("월별 공부 시간")
        plt.ylabel("시간")
        st.pyplot(plt)

# -------------------------------
# 과목별 상세 기록 확인
# -------------------------------
st.subheader("🔍 과목별 상세 기록")
if not df.empty:
    subject_select = st.selectbox("과목 선택", options=df["과목"].unique())
    subject_data = df[df["과목"] == subject_select].sort_values("날짜", ascending=False)

    if subject_data.empty:
        st.warning(f"'{subject_select}'에 대한 기록이 없습니다.")
    else:
        for idx, row in subject_data.iterrows():
            st.markdown(
                f"""
                **📅 날짜:** {row['날짜'].date()}  
                **⏳ 공부 시간:** {row['공부시간']}시간  
                **🎯 목표:** {row['목표']}  
                **📝 공부 내용:** {row['공부내용']}  
                **💡 메모:** {row['메모']}  
                ---
                """
            )
else:
    st.warning("과목별 기록을 확인할 데이터가 없습니다.")



