import streamlit as st
import pandas as pd
import math

st.set_page_config(page_title="Blood Buffer Simulator", page_icon="🩸")

st.title("🩸 혈액 완충계 시뮬레이터")
st.write("체중과 산 부하량에 따른 혈액 완충계의 변화를 단순 모델로 예측합니다.")

st.info("※ 본 프로그램은 탄산-탄산수소 이온 완충계를 단순화한 교육용 모델입니다.")

# ------------------------
# 입력
# ------------------------

weight = st.slider("체중 (kg)", 30, 100, 60)

acid = st.slider("산 부하량 (mmol)", 0, 150, 20)

# ------------------------
# 기본 상수
# ------------------------

blood_ratio = 0.075          # 혈액량 = 체중의 7.5%
HCO3_conc = 24               # mmol/L
CO2 = 1.2                    # mmol/L (고정)
pKa = 6.1

blood_volume = weight * blood_ratio
HCO3_total = blood_volume * HCO3_conc

# 산 첨가 후
HCO3_after = max(HCO3_total - acid, 0.01)

HCO3_conc_after = HCO3_after / blood_volume

pH = pKa + math.log10(HCO3_conc_after / CO2)

# ------------------------
# 결과 출력
# ------------------------

st.subheader("계산 결과")

col1, col2 = st.columns(2)

with col1:
    st.metric("예상 혈액량", f"{blood_volume:.2f} L")

with col2:
    st.metric("예상 혈액 pH", f"{pH:.2f}")

if pH >= 7.35:
    st.success("Good! 완충 작용이 비교적 잘 유지되는 상태")
elif pH >= 7.20:
    st.warning("Be careful! 완충능력이 감소하기 시작하는 구간")
else:
    st.error("Warning!!!! 완충 한계를 넘어 pH가 크게 감소한 상태")

# ------------------------
# 그래프
# ------------------------

acid_list = []
ph_list = []

for a in range(0,151):

    remain = max(HCO3_total-a,0.01)

    conc = remain/blood_volume

    ph = pKa + math.log10(conc/CO2)

    acid_list.append(a)
    ph_list.append(ph)

df = pd.DataFrame({
    "산 부하량 (mmol)":acid_list,
    "예상 pH":ph_list
})

st.subheader("산 부하량에 따른 pH 변화")

st.line_chart(df.set_index("산 부하량 (mmol)"))
