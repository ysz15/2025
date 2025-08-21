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
QUOTES = [
    "오늘의 작은 노력이 내일의 큰 성과를 만든다!",
    "포기하지 마라, 끝까지 해보자!",
    "너의 한 시간은 결코 헛되지 않다.",
    "꾸준함이 최고의 무기다.",
    "오늘도 한 걸음 성장했어!",
    "노력은 배신하지 않는다."
]

REQUIRED_COLS = ["날짜", "과목", "목표", "공부시간(분)", "메모", "공부 내용"]

# =========================
# 데이터 불러오기 + 스키마 보정
# =========================
if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
else:
    df = pd.DataFrame(columns=REQUIRED_COLS)

# 누락 컬럼 보정
for col in REQUIRED_COLS:
    if col not in df.columns:
        df[col] = "" if col != "공부시간(분)" else 0

# 타입 보정
# 날짜 → datetime (안전 변환), 공부시간 → 숫자
if not df.empty:
    df["날짜"] = pd.to_datetime(df["날짜"], errors="coerce")
    df["공부시간(분)"] = pd.to_numeric(df["공부시간(분)"], errors="coerce")
    # NaT/NaN 제거 및 기본값 처리
    df = df.dropna(subset=["날짜"])
    df["공부시간(분)"] = df["공부시간(분)"].fillna(0).astype(int)

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
    time_min = st.number_input("공부시간(분)", min_value=0, step=10)
    memo = st.text_area("간단 메모")
    content = st.text_area("공부 내용", placeholder="오늘 공부한 내용을 기록해보세요.")
    submitted = st.form_submit_button("저장")

    if submitted:
        if not subject:
            st.warning("과목을 입력하세요.")
        elif time_min <= 0:
            st.warning("공부 시간을 1분 이상 입력하세요.")
        else:
            new_row = pd.DataFrame({
                "날짜": [datetime.now().strftime("%Y-%m-%d")],  # CSV엔 문자열로 저장
                "과목": [subject],
                "목표": [goal],
                "공부시간(분)": [int(time_min)],
                "메모": [memo],
                "공부 내용": [content]
            })
            # 메모리상 df 갱신
            df = pd.concat([df, new_row], ignore_index=True)
            # CSV 저장
            df.to_csv(DATA_FILE, index=False)
            st.success("✅ 저장 완료!")

# 저장 후/초기 로드 후에도 타입 보정 재확인
if not df.empty:
    df["날짜"] = pd.to_datetime(df["날짜"], errors="coerce")
    df["공부시간(분)"] = pd.to_numeric(df["공부시간(분)"], errors="coerce").fillna(0).astype(int)
    df = df.dropna(subset=["날짜"])

# =========================
# 동기부여 문구
# =========================
st.subheader("💬 오늘의 동기부여")
random.seed(datetime.now().date().toordinal())  # 하루 고정
st.info(random.choice(QUOTES))

# =========================
# 전체 공부 기록 (Expander)
# =========================
st.subheader("📚 전체 공부 기록")
if not df.empty:
    df_sorted = df.sort_values("날짜", ascending=False)
    for _, row in df_sorted.iterrows():
        title = f"{row['날짜'].strftime('%Y-%m-%d')} - {row['과목']} ({int(row['공부시간(분)'])}분)"
        with st.expander(title):
            st.markdown(f"**목표:** {row.get('목표','') or ''}")
            st.markdown(f"**메모:** {row.get('메모','') or ''}")
            st.markdown(f"**공부 내용:** {row.get('공부 내용','') or ''}")
else:
    st.info("아직 기록이 없습니다. 첫 기록을 추가해보세요!")

# =========================
# 과목별 공부 내용 확인 (필터)
# =========================
if not df.empty:
    st.subheader("📝 과목별 공부 내용 확인")
    subjects = ["전체"] + sorted([s for s in df["과목"].dropna().unique().tolist() if str(s).strip() != ""])
    selected_subject = st.selectbox("확인할 과목 선택", subjects, index=0)

    filtered = df if selected_subject == "전체" else df[df["과목"] == selected_subject]
    if filtered.empty:
        st.info("해당 조건에 맞는 기록이 없습니다.")
    else:
        filtered = filtered.sort_values("날짜", ascending=False)
        for _, row in filtered.iterrows():
            title = f"{row['날짜'].strftime('%Y-%m-%d')} - {row['과목']} ({int(row['공부시간(분)'])}분)"
            with st.expander(title):
                st.markdown(f"**목표:** {row.get('목표','') or ''}")
                st.markdown(f"**메모:** {row.get('메모','') or ''}")
                st.markdown(f"**공부 내용:** {row.get('공부 내용','') or ''}")

# =========================
# 공부 시간 통계 (일/주/월)
# =========================
if not df.empty:
    st.subheader("📊 공부 시간 통계")

    # 일별 합계
    daily = df.groupby("날짜", as_index=False)["공부시간(분)"].sum()
    daily_chart = alt.Chart(daily).mark_bar(color=theme_color).encode(
        x=alt.X("날짜:T", title="날짜"),
        y=alt.Y("공부시간(분):Q", title="공부 시간(분)")
    ).properties(title="일별 공부 시간")

    # 주차별 합계 (Period → Timestamp 시작일)
    df["주차"] = df["날짜"].dt.to_period("W").apply(lambda p: p.to_timestamp())
    weekly = df.groupby("주차", as_index=False)["공부시간(분)"].sum()
    weekly_chart = alt.Chart(weekly).mark_line(point=True, color=theme_color).encode(
        x=alt.X("주차:T", title="주차 시작일"),
        y=alt.Y("공부시간(분):Q", title="공부 시간(분)")
    ).properties(title="주차별 공부 시간")

    # 월별 합계
    df["월"] = df["날짜"].dt.to_period("M").apply(lambda p: p.to_timestamp())
    monthly = df.groupby("월", as_index=False)["공부시간(분)"].sum()
    monthly_chart = alt.Chart(monthly).mark_area(opacity=0.6, color=theme_color).encode(
        x=alt.X("월:T", title="월"),
        y=alt.Y("공부시간(분):Q", title="공부 시간(분)")
    ).properties(title="월별 공부 시간")

    st.altair_chart(daily_chart, use_container_width=True)
    st.altair_chart(weekly_chart, use_container_width=True)
    st.altair_chart(monthly_chart, use_container_width=True)

    # 과목별 비율(합계 테이블)
    st.subheader("📌 과목별 공부 시간 합계")
    subject_total = df.groupby("과목", as_index=False)["공부시간(분)"].sum().sort_values("공부시간(분)", ascending=False)
    st.dataframe(subject_total, use_container_width=True)



