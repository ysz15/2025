import streamlit as st
import pandas as pd


# ==========================
# 기본 설정
# ==========================

st.set_page_config(
    page_title="혈액 완충계 시뮬레이터",
    page_icon="🩸"
)

st.title("🩸 혈액 탄산-탄산수소 완충계 시뮬레이터")

st.markdown("""
이 프로그램은 혈액 내 탄산-탄산수소 이온 완충계를 단순화하여,
산 부하량 증가에 따른 완충 가능 범위를 계산하는 모델입니다.

**모델 가정**
- 혈액량 = 체중의 7.5%
- 혈액 내 HCO₃⁻ 농도 = 24 mmol/L
- 산 1 mmol이 증가하면 HCO₃⁻ 1 mmol이 소비됨

※ 실제 인체에서는 폐와 신장의 조절 과정도 함께 작용하므로 교육용 모델입니다.
""")


# ==========================
# 입력
# ==========================

st.header("① 입력")

weight = st.number_input(
    "체중 (kg)",
    min_value=30.0,
    max_value=150.0,
    value=60.0,
    step=0.5
)

acid = st.number_input(
    "산 부하량 (mmol)",
    min_value=0.0,
    max_value=500.0,
    value=20.0,
    step=1.0
)


# ==========================
# 계산
# ==========================

blood_volume = weight * 0.075

initial_HCO3 = blood_volume * 24

remaining_HCO3 = initial_HCO3 - acid

if remaining_HCO3 < 0:
    remaining_HCO3 = 0


buffer_rate = remaining_HCO3 / initial_HCO3 * 100


# ==========================
# 결과
# ==========================

st.header("② 계산 결과")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "혈액량",
        f"{blood_volume:.2f} L"
    )

with col2:
    st.metric(
        "초기 HCO₃⁻ 양",
        f"{initial_HCO3:.1f} mmol"
    )

with col3:
    st.metric(
        "남은 HCO₃⁻",
        f"{remaining_HCO3:.1f} mmol"
    )


# ==========================
# 최대 완충 가능량
# ==========================

st.header("③ 완충 한계 분석")

st.metric(
    "최대 완충 가능 산 부하량",
    f"{initial_HCO3:.1f} mmol"
)

st.metric(
    "남은 완충 여유량",
    f"{max(initial_HCO3-acid,0):.1f} mmol"
)


if acid < initial_HCO3:
    st.success(
        f"현재 산 부하는 완충 가능한 범위입니다.\n\n"
        f"추가로 약 {initial_HCO3-acid:.1f} mmol까지 "
        f"이론적으로 대응 가능합니다."
    )

else:
    st.error(
        "이론적인 완충 한계를 초과했습니다."
    )


# ==========================
# 그래프 1
# ==========================

st.header("④ 산 부하량에 따른 완충능 변화")


acid_values = []
buffer_values = []


for a in range(0, int(initial_HCO3)+50):

    remain = initial_HCO3 - a

    if remain < 0:
        remain = 0

    buffer = remain / initial_HCO3 * 100

    acid_values.append(a)
    buffer_values.append(buffer)


graph = pd.DataFrame(
    {
        "남은 완충능(%)": buffer_values
    },
    index=acid_values
)


graph.index.name = "산 부하량(mmol)"


st.line_chart(graph)


st.caption(
    "x축: 산 부하량(mmol) / y축: 남은 완충능(%)"
)


# ==========================
# 체중별 비교
# ==========================

st.header("⑤ 체중별 완충능 비교")


weights = [45, 60, 80]

comparison = {}


max_range = range(0,200)


for w in weights:

    blood = w * 0.075

    max_buffer = blood * 24

    values = []

    for a in max_range:

        remain = max_buffer - a

        if remain < 0:
            remain = 0

        values.append(remain/max_buffer*100)


    comparison[f"{w}kg"] = values


comparison_df = pd.DataFrame(
    comparison,
    index=list(max_range)
)

comparison_df.index.name = "산 부하량(mmol)"


st.line_chart(comparison_df)


# ==========================
# 계산 과정
# ==========================

st.header("⑥ 계산 과정")


st.write(
    f"""
1. 혈액량 계산

{weight:.1f}kg × 0.075 = {blood_volume:.2f}L


2. 초기 탄산수소 이온 양 계산

{blood_volume:.2f}L × 24mmol/L = {initial_HCO3:.1f}mmol


3. 산 첨가 후 남은 탄산수소 이온

{initial_HCO3:.1f} - {acid:.1f} = {remaining_HCO3:.1f}mmol


4. 완충능 계산

(남은 HCO₃⁻ ÷ 초기 HCO₃⁻) × 100

= {buffer_rate:.1f}%
"""
)


st.markdown("""
### 그래프 해석

- x축: 산 부하량(mmol)
- y축: 남은 완충능(%)

산 부하량이 증가하면 탄산수소 이온이 소비되어
완충 가능한 여유량이 감소한다.

곡선이 0%에 가까워지는 지점은
이 모델에서 탄산수소 이온이 거의 소모되는
이론적 완충 한계이다.
""")
