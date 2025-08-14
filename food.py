import streamlit as st
import random
from streamlit_lottie import st_lottie
import requests

# -----------------------------
# Lottie 애니메이션 함수
# -----------------------------
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# -----------------------------
# 페이지 설정
# -----------------------------
st.set_page_config(page_title="🎮 미니 게임 월드", page_icon="🕹️")
st.markdown("<h1 style='text-align:center; color:#FF6F61;'>🎮 미니 게임 월드 🕹️</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#555;'>여러 재미있는 게임을 즐기며 스트레스 날리기! ✨</p>", unsafe_allow_html=True)
st.markdown("---")

# -----------------------------
# 게임 선택
# -----------------------------
games = ["가위바위보 ✊✌️✋", "숫자 맞추기 🔢", "틱택토 ❌⭕"]
selected_game = st.selectbox("🎯 플레이할 게임을 선택하세요:", games)

st.markdown("---")

# -----------------------------
# 가위바위보 게임
# -----------------------------
if selected_game.startswith("가위바위보"):
    st.subheader("✂️ 가위바위보 게임 ✋")
    user_choice = st.radio("선택하세요:", ["가위 ✌️", "바위 ✊", "보 ✋"])
    if st.button("🕹️ 결과 보기"):
        computer_choice = random.choice(["가위 ✌️", "바위 ✊", "보 ✋"])
        st.markdown(f"💻 **컴퓨터 선택:** {computer_choice}")
        if user_choice == computer_choice:
            st.info("무승부! 🤝")
        elif (user_choice == "가위 ✌️" and computer_choice == "보 ✋") or \
             (user_choice == "바위 ✊" and computer_choice == "가위 ✌️") or \
             (user_choice == "보 ✋" and computer_choice == "바위 ✊"):
            st.success("🎉 승리! 축하합니다! 🎊")
            st.balloons()
        else:
            st.error("😢 패배! 다음엔 잘 할 수 있어요!")

# -----------------------------
# 숫자 맞추기 게임
# -----------------------------
elif selected_game.startswith("숫자 맞추기"):
    st.subheader("🔢 숫자 맞추기 게임 🔢")
    number_to_guess = random.randint(1, 10)
    guess = st.number_input("1~10 사이 숫자를 입력하세요:", min_value=1, max_value=10, step=1)
    if st.button("🕹️ 확인"):
        if guess == number_to_guess:
            st.success(f"🎉 정답! 숫자는 {number_to_guess}였습니다.")
            # Lottie 불꽃 애니메이션
            lottie_fire = load_lottieurl("https://assets2.lottiefiles.com/packages/lf20_touohxv0.json")
            if lottie_fire:
                st_lottie(lottie_fire, height=200, key="fire")
        else:
            st.error(f"❌ 틀렸어요. 숫자는 {number_to_guess}였습니다.")

# -----------------------------
# 틱택토 게임 (간단 버전)
# -----------------------------
elif selected_game.startswith("틱택토"):
    st.subheader("❌⭕ 틱택토 게임 (간단)")
    st.info("틱택토는 간단히 표시만 해주는 예시입니다. 확장하여 실제 플레이 가능!")
    st.markdown("⬜⬜⬜  ⬜⬜⬜  ⬜⬜⬜\n⬜⬜⬜  ⬜⬜⬜  ⬜⬜⬜\n⬜⬜⬜  ⬜⬜⬜  ⬜⬜⬜")

        st.warning("하나 이상의 음식을 선택해주세요! ⚠️")

