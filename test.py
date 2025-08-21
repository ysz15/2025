import streamlit as st
import pandas as pd
import altair as alt
import os
from datetime import datetime
import random

# =====================
# 파일 경로
# =====================
DATA_FILE = "study_data.csv"

# =====================
# CSV 로드/저장 함수
# =====================
def load_data():
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
        df['날짜'] = pd.to_datetime(df['날짜'], errors='coerce')
        df['공부시간'] = pd.to_numeric(df['공부시간'], errors='coerce').fillna(0)
        return df.dropna(subset=['날짜'])
    else:
        return pd.DataFrame(columns=['날짜', '과목', '공부시간', '목표', '공부내용', '메모'])

def save_data(df):
    df.to_csv(DATA_FILE, index=False)

# =====================
# 초기 데이터
# =====================
df = load_data()

# =====================
# 페이지 설정
# =====================
st.set_page_config(page_title="📚 공부 기록 다이어리", layout="wide")
st.title("📚 공부 기록 다이어리")

# =====================
# 사이드바
# =====================
st.sidebar.header("⚙️ 설정")
theme_color = st.sidebar.color_picker("테마 색상", "#4CAF50")
icon = st.sidebar.selectbox("아이콘 선택", ["📚","📝","🎯","🔥","📖"])

# =====================
# 공부 기록 입력
# =====================
st.subheader(f"{icon} 오늘의 공부 기록 추가")
with st.form("record_form"):
    date = st.date_input("날짜", datetime.today())
    subject = st.text_input("과목")
    hours = st.number_input("공부 시간 (시간)", min_value=0.0, step=0.5)
    goal = st.text_area("오늘의 목표")
    details = st.text_area("공부 내용")
    memo = st.text_area("간단 메모")
    submitted = st.form_submit_button("저장")

if submitted:
    if subject.strip() == "" or hours <= 0:
        st.warning("과목과 공부 시간을 올바르게 입력해주세요.")
    else:
        new_row = pd.DataFrame({
            "날짜":[pd.to_datetime(date)],
            "과목":[subject],
            "공부시간":[hours],
            "목표":[goal],
            "공부내용":[details],
            "메모":[memo]
        })
        df = pd.concat([df, new_row], ignore_index=True)
        save_data(df)
        st.success(f"{subject} 공부 기록이 저장되었습니다!")

# =====================
# 동기부여 문구
# =====================
quotes = [
    "작은 한 걸음이 큰 변화를 만든다! 💪",
    "오늘의 노력이 내일의 성장을 만든다 🌱",
    "포기하지 않는 것이 성공의 비결이다 🔥",
    "꾸준함이 최고의 실력이다 ✨",
    "오늘도 멋지게 해냈어! 🙌"
]
st.subheader("💡 오늘의 동기부여")
st.info(random.choice(quotes))

# =====================
# 전체 기록 확인
# =====================
st.subheader("📖 전체 공부 기록")
if df.empty:
    st.info("아직 기록이 없습니다.")
else:
    subjects_list = ["전체"] + df['과목'].dropna().unique().tolist()
    selected_subject = st.selectbox("과목 선택 (전체 포함)", subjects_list)

    filtered_df = df if selected_subject == "전체" else df[df['과목']==selected_subject]
    filtered_df = filtered_df.sort_values("날짜", ascending=False)
    for _, row in filtered_df.iterrows():
        with st.expander(f"{row['날짜'].strftime('%Y-%m-%d')} - {row['과목']} ({row['공부시간']}시간)"):
            st.markdown(f"**목표:** {row['목표']}")
            st.markdown(f"**공부 내용:** {row['공부내용']}")
            st.markdown(f"**메모:** {row['메모']}")

# =====================
# 공부 시간 통계
# =====================
if not df.empty:
    st.subheader("📊 공부 시간 통계")
    
    # 컬럼 추가
    df['주차'] = df['날짜'].dt.to_period('W').apply(lambda r: r.start_time)
    df['월'] = df['날짜'].dt.to_period('M').apply(lambda r: r.start_time)

    # --- 전체 공부 통계 ---
    st.markdown("### 🏆 전체 공부 시간")
    daily = df.groupby('날짜', as_index=False)['공부시간'].sum()
    weekly = df.groupby('주차', as_index=False)['공부시간'].sum()
    monthly = df.groupby('월', as_index=False)['공부시간'].sum()

    st.altair_chart(
        alt.Chart(daily).mark_bar(color=theme_color).encode(
            x='날짜:T', y='공부시간:Q'
        ).properties(title="일별 공부 시간"), use_container_width=True
    )
    st.altair_chart(
        alt.Chart(weekly).mark_line(point=True, color=theme_color).encode(
            x='주차:T', y='공부시간:Q'
        ).properties(title="주차별 공부 시간"), use_container_width=True
    )
    st.altair_chart(
        alt.Chart(monthly).mark_area(opacity=0.6, color=theme_color).encode(
            x='월:T', y='공부시간:Q'
        ).properties(title="월별 공부 시간"), use_container_width=True
    )

    st.markdown("### 📌 과목별 공부 시간 합계")
    subject_total = df.groupby('과목', as_index=False)['공부시간'].sum().sort_values('공부시간', ascending=False)
    st.dataframe(subject_total, use_container_width=True)

    # --- 선택 과목별 통계 ---
    if selected_subject != "전체":
        st.markdown(f"### 📊 '{selected_subject}' 과목 공부 시간 통계")
        daily_subj = filtered_df.groupby('날짜', as_index=False)['공부시간'].sum()
        weekly_subj = filtered_df.groupby('주차', as_index=False)['공부시간'].sum()
        monthly_subj = filtered_df.groupby('월', as_index=False)['공부시간'].sum()

        st.altair_chart(
            alt.Chart(daily_subj).mark_bar(color=theme_color).encode(
                x='날짜:T', y='공부시간:Q'
            ).properties(title=f"{selected_subject} 일별 공부 시간"), use_container_width=True
        )
        st.altair_chart(
            alt.Chart(weekly_subj).mark_line(point=True, color=theme_color).encode(
                x='주차:T', y='공부시간:Q'
            ).properties(title=f"{selected_subject} 주차별 공부 시간"), use_container_width=True
        )
        st.altair_chart(
            alt.Chart(monthly_subj).mark_area(opacity=0.6, color=theme_color).encode(
                x='월:T', y='공부시간:Q'
            ).properties(title=f"{selected_subject} 월별 공부 시간"), use_container_width=True
        )




