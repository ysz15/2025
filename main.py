# app.py
import streamlit as st
from mbti_data import mbti_jobs

st.set_page_config(page_title="MBTI 직업 추천", page_icon="💼")

st.title("💼 MBTI 기반 직업 추천")
st.write("MBTI를 선택하면 적합한 직업과 설명을 알려드립니다.")

# MBTI 선택
mbti_list = list(mbti_jobs.keys())
selected_mbti = st.selectbox("당신의 MBTI를 선택하세요:", mbti_list)

# 결과 출력
if selected_mbti:
    st.subheader(f"{selected_mbti} 추천 직업")
    jobs = mbti_jobs[selected_mbti]["jobs"]
    desc = mbti_jobs[selected_mbti]["description"]

    st.markdown(f"**설명:** {desc}")
    st.markdown("**추천 직업:**")
    for job in jobs:
        st.write(f"- {job}")

