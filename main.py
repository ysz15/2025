import streamlit as st

# MBTI 데이터
mbti_jobs = {
    "INTJ": {
        "jobs": ["데이터 분석가", "전략 기획가", "연구원"],
        "description": "분석적이고 계획적인 사고로 장기 전략을 설계하는 데 강합니다."
    },
    "ENFP": {
        "jobs": ["광고 기획자", "콘텐츠 크리에이터", "이벤트 플래너"],
        "description": "창의적이고 사람들과 교류하는 걸 즐기며 새로운 시도를 두려워하지 않습니다."
    }
    # 나머지 MBTI 데이터도 추가
}

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

