import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# ----------------------
# 앱 제목
# ----------------------
st.title("🌿 교실 환기 방식 분석 프로그램")
st.write(
    "학생 설문 데이터를 기반으로 환기 방식별 쾌적성, 답답함, 집중도를 분석하고 "
    "효율적인 환기 방식을 추천합니다."
)


# ----------------------
# 데이터 입력
# ----------------------

st.sidebar.header("설문 데이터 입력")

uploaded_file = st.sidebar.file_uploader(
    "CSV 파일 업로드",
    type=["csv"]
)


# 예시 데이터 제공
if uploaded_file is None:
    data = pd.DataFrame({
        "환기방식": [
            "외부창문",
            "외부+문",
            "외부+복도"
        ],
        "답답함": [
            3.7,
            2.5,
            1.8
        ],
        "쾌적함": [
            2.8,
            3.7,
            4.5
        ],
        "집중도": [
            3.0,
            3.8,
            4.3
        ]
    })

    st.info("현재 예시 데이터를 사용 중입니다.")

else:
    data = pd.read_csv(uploaded_file)


# ----------------------
# 데이터 전처리
# ----------------------

st.subheader("1. 데이터 전처리")

st.write("원본 데이터")
st.dataframe(data)


# 결측치 확인
missing = data.isnull().sum()

st.write("결측치 확인")
st.write(missing)


# 결측치 제거
data = data.dropna()


st.write("결측치 제거 후 데이터")
st.dataframe(data)



# ----------------------
# 평균 계산
# ----------------------

st.subheader("2. 환기 방식별 평균 분석")


mean_data = data.groupby("환기방식").mean(numeric_only=True)

st.dataframe(mean_data)


# ----------------------
# 히트맵
# ----------------------

st.subheader("3. 환기 방식별 평가 요소 비교 (히트맵)")


fig, ax = plt.subplots(figsize=(8,4))

sns.heatmap(
    mean_data[["답답함", "쾌적함", "집중도"]],
    annot=True,
    cmap="YlGnBu",
    fmt=".2f"
)

plt.xlabel("평가 항목")
plt.ylabel("환기 방식")

st.pyplot(fig)



# ----------------------
# 환기 효과 지수 계산
# ----------------------

st.subheader("4. 환기 효과 지수")


result = mean_data.copy()


# 답답함은 낮을수록 좋으므로 변환
result["환기효과지수"] = (
    result["쾌적함"]
    + result["집중도"]
    + (5 - result["답답함"])
)


st.write(result)


# 막대그래프

fig2, ax2 = plt.subplots(figsize=(8,4))

ax2.bar(
    result.index,
    result["환기효과지수"]
)

ax2.set_ylabel("환기 효과 지수")
ax2.set_xlabel("환기 방식")

plt.xticks(rotation=30)

st.pyplot(fig2)



# ----------------------
# 최종 추천
# ----------------------

best = result["환기효과지수"].idxmax()


st.success(
    f"추천 환기 방식: {best}"
)

st.write(
    "분석 결과, 해당 환기 방식은 학생들이 느끼는 쾌적함과 집중도를 높이고 "
    "답답함을 감소시키는 경향을 보여 가장 효과적인 방식으로 평가되었습니다."
)
