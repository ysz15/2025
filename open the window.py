import streamlit as st
import pandas as pd


# -----------------------------
# 제목
# -----------------------------

st.title("🌿 교실 환기 방식 분석 프로그램")

st.write(
    "학생 설문 데이터를 기반으로 환기 방식별 답답함, "
    "쾌적함, 집중도를 분석하여 효과적인 환기 방식을 탐색합니다."
)


# -----------------------------
# 데이터 입력
# -----------------------------

st.subheader("1. 설문 데이터")

# 예시 데이터 (25명 설문 결과 평균)
data = pd.DataFrame({
    "환기방식": [
        "외부쪽 창문",
        "외부쪽 창문 + 문",
        "외부쪽 창문 + 복도쪽 창문"
    ],
    "답답함": [
        3.4,
        2.5,
        1.9
    ],
    "쾌적함": [
        2.7,
        3.8,
        4.1
    ],
    "집중도": [
        2.8,
        3.6,
        3.7
    ]
})


st.dataframe(data)



# -----------------------------
# 데이터 전처리
# -----------------------------

st.subheader("2. 데이터 전처리")

st.write("결측치 확인")

missing = data.isnull().sum()

st.write(missing)


# 결측치 제거
data = data.dropna()



# -----------------------------
# 데이터 분석 및 시각화
# -----------------------------

st.subheader("3. 환기 방식별 결과 비교")


chart_data = data.set_index("환기방식")


# 쾌적함 그래프
st.write("🌱 쾌적함 정도 비교")

st.bar_chart(
    chart_data["쾌적함"]
)



# 답답함 그래프
st.write("😷 답답함 정도 비교")

st.bar_chart(
    chart_data["답답함"]
)



# 집중도 그래프
st.write("📚 집중도 비교")

st.bar_chart(
    chart_data["집중도"]
)



# -----------------------------
# 결과 분석
# -----------------------------

st.subheader("4. 분석 결과")


best_comfort = data.loc[
    data["쾌적함"].idxmax(),
    "환기방식"
]

best_focus = data.loc[
    data["집중도"].idxmax(),
    "환기방식"
]

lowest_stuffy = data.loc[
    data["답답함"].idxmin(),
    "환기방식"
]


st.success(
    f"""
    분석 결과
    
    ✅ 가장 높은 쾌적함:
    {best_comfort}
    
    ✅ 가장 높은 집중도:
    {best_focus}
    
    ✅ 가장 낮은 답답함:
    {lowest_stuffy}
    """
)


st.write(
    """
    세 가지 평가 요소를 종합적으로 비교한 결과,
    외부쪽 창문과 복도쪽 창문을 동시에 개방하는 방식이
    학생들이 체감하는 실내 환경 개선에 가장 효과적인 환기 방식으로 나타났습니다.
    """
)
