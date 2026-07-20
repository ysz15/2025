import streamlit as st
import plotly.graph_objects as go


# ==========================
# 기본 설정
# ==========================

st.set_page_config(
    page_title="혈액 완충계 시뮬레이터",
    page_icon="🩸",
    layout="wide"
)

st.title("🩸 혈액 탄산-탄산수소 완충계 시뮬레이터")

st.markdown("""
이 프로그램은 혈액 내 탄산-탄산수소 이온 완충계를 단순화하여,
산 부하 증가에 따른 완충 가능 범위를 계산하는 모델입니다.

**가정**
- 혈액량 = 체중의 7.5%
- 혈액 내 HCO₃⁻ 농도 = 24 mmol/L
- 산 1 mmol 첨가 시 HCO₃⁻ 1 mmol 소비
""")

st.info(
    "※ 실제 인체에서는 폐와 신장 조절 등 다양한 항상성 과정이 함께 작용하므로 "
    "본 모델은 완충계의 원리를 이해하기 위한 단순화 모델입니다."
)


# ==========================
# 입력
# ==========================

st.header("① 입력")

col1, col2 = st.columns(2)


with col1:
    weight = st.number_input(
        "체중 (kg)",
        min_value=30.0,
        max_value=150.0,
        value=60.0,
        step=0.5
    )


with col2:
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


buffer_rate = (remaining_HCO3 / initial_HCO3) * 100


# ==========================
# 결과 출력
# ==========================

st.header("② 계산 결과")


c1, c2, c3 = st.columns(3)


with c1:
    st.metric(
        "예상 혈액량",
        f"{blood_volume:.2f} L"
    )


with c2:
    st.metric(
        "초기 HCO₃⁻ 총량",
        f"{initial_HCO3:.1f} mmol"
    )


with c3:
    st.metric(
        "남은 HCO₃⁻",
        f"{remaining_HCO3:.1f} mmol"
    )


# ==========================
# 최대 완충량 기능
# ==========================

st.header("③ 완충 한계 분석")


col4, col5 = st.columns(2)


with col4:
    st.metric(
        "최대 완충 가능 산 부하량",
        f"{initial_HCO3:.1f} mmol"
    )


with col5:
    st.metric(
        "남은 완충 여유량",
        f"{max(initial_HCO3-acid,0):.1f} mmol"
    )


if acid < initial_HCO3:

    st.success(
        f"현재 산 부하는 완충 가능한 범위입니다.\n\n"
        f"이론적으로 약 {initial_HCO3-acid:.1f} mmol의 "
        f"추가 산 부하까지 대응 가능합니다."
    )

else:

    st.error(
        "현재 산 부하는 이론적 완충 한계를 초과했습니다."
    )


# ==========================
# 산 부하량 변화 그래프
# ==========================

st.header("④ 산 부하량 증가에 따른 완충능 변화")


acid_values = list(range(0, int(initial_HCO3)+50))


buffer_values = []


for a in acid_values:

    remain = initial_HCO3 - a

    if remain < 0:
        remain = 0

    buffer = (remain / initial_HCO3) * 100

    buffer_values.append(buffer)



fig = go.Figure()


fig.add_trace(
    go.Scatter(
        x=acid_values,
        y=buffer_values,
        mode="lines",
        name="완충능"
    )
)


fig.add_trace(
    go.Scatter(
        x=[acid],
        y=[buffer_rate],
        mode="markers",
        marker=dict(size=12),
        name="현재 위치"
    )
)


fig.update_layout(
    title="산 부하량에 따른 남은 완충능",
    xaxis_title="산 부하량 (mmol)",
    yaxis_title="남은 완충능 (%)",
    height=500
)


st.plotly_chart(
    fig,
    use_container_width=True
)


# ==========================
# 체중별 비교
# ==========================

st.header("⑤ 체중별 완충 가능량 비교")


weights = [45, 60, 80]


fig2 = go.Figure()


for w in weights:

    blood = w * 0.075

    max_buffer = blood * 24

    buffer_list = []


    for a in acid_values:

        remain = max_buffer - a

        if remain < 0:
            remain = 0

        buffer = remain / max_buffer * 100

        buffer_list.append(buffer)



    fig2.add_trace(
        go.Scatter(
            x=acid_values,
            y=buffer_list,
            mode="lines",
            name=f"{w}kg"
        )
    )


fig2.update_layout(
    title="체중에 따른 완충능 변화 비교",
    xaxis_title="산 부하량 (mmol)",
    yaxis_title="남은 완충능 (%)",
    height=500
)


st.plotly_chart(
    fig2,
    use_container_width=True
)


# ==========================
# 계산 과정
# ==========================

st.header("⑥ 계산 과정")


st.latex(
    r"혈액량 = 체중 \times 0.075"
)

st.write(
    f"{weight} × 0.075 = {blood_volume:.2f} L"
)


st.latex(
    r"초기\ HCO_3^- = 혈액량 \times 24"
)


st.write(
    f"{blood_volume:.2f} × 24 = {initial_HCO3:.1f} mmol"
)


st.latex(
    r"남은\ HCO_3^- = 초기\ HCO_3^- - 산\ 부하량"
)


st.write(
    f"{initial_HCO3:.1f} - {acid:.1f} = {remaining_HCO3:.1f} mmol"
)


st.markdown("""
### 그래프 해석

- **x축:** 산 부하량(mmol)
- **y축:** 남은 완충능(%)

산 부하량이 증가할수록 탄산수소 이온이 소비되어
완충 가능한 여유량이 감소한다.

그래프가 0%에 가까워지는 지점은
이 모델에서 완충 물질이 모두 소모되는 이론적 한계점이다.
""")
