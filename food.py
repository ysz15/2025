import streamlit as st
import random

st.set_page_config(page_title="🍔 오늘의 야식 추천기", page_icon="🍕")
st.markdown("<h1 style='text-align: center; color: #FF6F61;'>🍕 오늘의 야식 추천기 🍟</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #555;'>오늘 밤 뭐 먹을지 고민된다면? 🎯</p>", unsafe_allow_html=True)

# -----------------------------
# 야식 메뉴 데이터 (이모지 포함)
# -----------------------------
snacks = {
    "치킨 🍗": {"calories": 1200, "difficulty": "없음", "delivery": "✅ 가능"},
    "라면 🍜": {"calories": 500, "difficulty": "낮음", "delivery": "❌ 불가"},
    "떡볶이 🌶️": {"calories": 600, "difficulty": "낮음", "delivery": "✅ 가능"},
    "피자 🍕": {"calories": 1300, "difficulty": "없음", "delivery": "✅ 가능"},
    "야식 도시락 🍱": {"calories": 800, "difficulty": "중간", "delivery": "❌ 불가"},
    "김밥 🍙": {"calories": 400, "difficulty": "낮음", "delivery": "✅ 가능"},
    "핫도그 🌭": {"calories": 450, "difficulty": "낮음", "delivery": "✅ 가능"},
    "샌드위치 🥪": {"calories": 350, "difficulty": "낮음", "delivery": "✅ 가능"},
    "만두 🥟": {"calories": 550, "difficulty": "중간", "delivery": "❌ 불가"},
    "치즈스틱 🧀": {"calories": 300, "difficulty": "낮음", "delivery": "❌ 불가"},
    "튀김 🍤": {"calories": 600, "difficulty": "중간", "delivery": "✅ 가능"},
    "순대 🌭": {"calories": 500, "difficulty": "낮음", "delivery": "✅ 가능"},
    "샐러드 🥗": {"calories": 250, "difficulty": "낮음", "delivery": "✅ 가능"},
    "커피/음료 ☕": {"calories": 150, "difficulty": "없음", "delivery": "✅ 가능"},
    "아이스크림 🍦": {"calories": 200, "difficulty": "없음", "delivery": "✅ 가능"},
}

# -----------------------------
# 사용자 선택
# -----------------------------
snack_list = list(snacks.keys())
preferences = st.multiselect("🍴 먹고 싶은 음식 종류를 선택하세요:", snack_list)

st.markdown("---")

# -----------------------------
# 추천 기능
# -----------------------------
if st.button("🎯 추천받기", use_container_width=True):
    if preferences:
        choice = random.choice(preferences)
        info = snacks[choice]
        
        st.markdown(f"<h2 style='text-align:center; color:#FF6347;'>오늘의 추천 야식: {choice} 🎉</h2>", unsafe_allow_html=True)
        
        st.markdown(f"<p style='font-size:18px; color:#FF4500;'>🔥 칼로리: {info['calories']} kcal</p>", unsafe_allow_html=True)
        st.markdown(f"<p style='font-size:18px; color:#32CD32;'>⚡ 조리 난이도: {info['difficulty']}</p>", unsafe_allow_html=True)
        st.markdown(f"<p style='font-size:18px; color:#1E90FF;'>📦 배달 가능 여부: {info['delivery']}</p>", unsafe_allow_html=True)
        
        st.snow()
    else:
        st.warning("하나 이상의 음식을 선택해주세요! ⚠️")

