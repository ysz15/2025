import streamlit as st           # Streamlit 라이브러리 불러오기 (웹앱 UI 구성)
import pandas as pd              # 데이터 처리용 Pandas
import altair as alt             # 데이터 시각화용 Altair
import os                        # 파일 존재 여부 등 OS 관련 기능
from datetime import datetime    # 날짜/시간 처리
import random                    # 동기부여 문구 랜덤 출력용

# =====================
# 파일 경로
# =====================
DATA_FILE = "study_data.csv"    # 공부 기록을 저장할 CSV 파일 경로

# =====================
# CSV 로드/저장 함수
# =====================
def load_data():
    """CSV 파일이 존재하면 로드, 없으면 빈 데이터프레임 생성"""
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
        df['날짜'] = pd.to_datetime(df['날짜'], errors='coerce')  # 날짜 컬럼 안전하게 변환
        df['공부시간'] = pd.to_numeric(df['공부시간'], errors='coerce').fillna(0)  # 공부시간 숫자로 변환
        return df.dropna(subset=['날짜'])  # 날짜가 없는 행 제거
    else:
        # 초기 컬럼 정의
        return pd.DataFrame(columns=['날짜', '과목', '공부시간', '목표', '공부내용', '메모'])

def save_data(df):
    """데이터프레임을 CSV로 저장"""
    df.to_csv(DATA_FILE, index=False)

# =====================
# 초기 데이터 로드
# =====================
df = load_data()   # 앱 실행 시 CSV 파일 읽기 또는 빈 데이터 생성

# =====================
# 페이지 설정
# =====================
st.set_page_config(page_title="📚 공부 기록 다이어리", layout="wide")  # 페이지 타이틀/레이아웃
st.title("📚 공부 기록 다이어리")  # 웹앱 메인 타이틀

# =====================
# 사이드바
# =====================
st.sidebar.header("⚙️ 설정")
theme_color = st.sidebar.color_picker("테마 색상", "#4CAF50")  # 테마 색상 선택
icon = st.sidebar.selectbox("아이콘 선택", ["📚","📝","🎯","🔥","📖"])  # 상단 아이콘 선택

# =====================
# 공부 기록 입력
# =====================
st.subheader(f"{icon} 오늘의 공부 기록 추가")
with st.form("record_form"):  # Streamlit 입력 폼 생성
    date = st.date_input("날짜", datetime.today())   # 날짜 선택
    subject = st.text_input("과목")                  # 과목 입력
    hours = st.number_input("공부 시간 (시간)", min_value=0.0, step=0.5)  # 시간 입력
    goal = st.text_area("오늘의 목표")              # 오늘 목표 기록
    details = st.text_area("공부 내용")             # 공부한 내용 기록
    memo = st.text_area("간단 메모")                # 메모 입력
    submitted = st.form_submit_button("저장")       # 제출 버튼

if submitted:
    if subject.strip() == "" or hours <= 0:
        st.warning("과목과 공부 시간을 올바르게 입력해주세요.")  # 입력 체크
    else:
        # 새로운 행 생성
        new_row = pd.DataFrame({
            "날짜":[pd.to_datetime(date)],
            "과목":[subject],
            "공부시간":[hours],
            "목표":[goal],
            "공부내용":[details],
            "메모":[memo]
        })
        df = pd.concat([df, new_row], ignore_index=True)  # 기존 데이터에 추가
        save_data(df)                                   # CSV 저장
        st.success(f"{subject} 공부 기록이 저장되었습니다!")  # 저장 완료 메시지

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
st.info(random.choice(quotes))  # 랜덤으로 동기부여 문구 출력

# =====================
# 전체 기록 확인
# =====================
st.subheader("📖 전체 공부 기록")
if df.empty:
    st.info("아직 기록이 없습니다.")  # 데이터 없을 경우 안내
else:
    # 과목별 필터 생성
    subjects_list = ["전체"] + df['과목'].dropna().unique().tolist()
    selected_subject = st.selectbox("과목 선택", subjects_list)
    if selected_subject != "전체":
        filtered_df = df[df['과목']==selected_subject]  # 선택한 과목만 필터링
    else:
        filtered_df = df.copy()  # 전체 과목

    filtered_df = filtered_df.sort_values("날짜", ascending=False)  # 최근 기록 먼저
    for _, row in filtered_df.iterrows():
        # Expander로 개별 기록 표시
        with st.expander(f"{row['날짜'].strftime('%Y-%m-%d')} - {row['과목']} ({row['공부시간']}시간)"):
            st.markdown(f"**목표:** {row['목표']}")
            st.markdown(f"**공부 내용:** {row['공부내용']}")
            st.markdown(f"**메모:** {row['메모']}")

# =====================
# 공부 시간 분석 (일/주/월)
# =====================
if not df.empty:
    st.subheader("📊 공부 시간 통계")

    # 주차/월 컬럼 생성
    df['주차'] = df['날짜'].dt.to_period('W').apply(lambda r: r.start_time)  # 주 시작일
    df['월'] = df['날짜'].dt.to_period('M').apply(lambda r: r.start_time)    # 월 시작일

    # 일별 합계
    daily = df.groupby('날짜', as_index=False)['공부시간'].sum()
    daily_chart = alt.Chart(daily).mark_bar(color=theme_color).encode(
        x=alt.X('날짜:T', title='날짜'),
        y=alt.Y('공부시간:Q', title='공부시간(시간)')
    ).properties(title="일별 공부 시간")

    # 주별 합계
    weekly = df.groupby('주차', as_index=False)['공부시간'].sum()
    weekly_chart = alt.Chart(weekly).mark_line(point=True, color=theme_color).encode(
        x=alt.X('주차:T', title='주차 시작일'),
        y=alt.Y('공부시간:Q', title='공부시간(시간)')
    ).properties(title="주별 공부 시간")

    # 월별 합계
    monthly = df.groupby('월', as_index=False)['공부시간'].sum()
    monthly_chart = alt.Chart(monthly).mark_area(opacity=0.6, color=theme_color).encode(
        x=alt.X('월:T', title='월'),
        y=alt.Y('공부시간:Q', title='공부시간(시간)')
    ).properties(title="월별 공부 시간")

    # 차트 표시
    st.altair_chart(daily_chart, use_container_width=True)
    st.altair_chart(weekly_chart, use_container_width=True)
    st.altair_chart(monthly_chart, use_container_width=True)

    # 과목별 합계 테이블
    subject_total = df.groupby('과목', as_index=False)['공부시간'].sum().sort_values('공부시간', ascending=False)
    st.subheader("📌 과목별 공부 시간 합계")
    st.dataframe(subject_total, use_container_width=True)




