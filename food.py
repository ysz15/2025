import streamlit as st
import random

st.set_page_config(page_title="오늘의 야식 추천기", page_icon="🍔")
st.title("🍕 오늘의 야식 추천기")
st.write("오늘 먹을 야식을 추천해드립니다!")

# -----------------------------
# 야식 메뉴 데이터
# -----------------------------
snacks = {
    "치킨": {"calories": 1200, "difficulty": "없음", "delivery": "가능"},
    "라면": {"calories": 500, "difficulty": "낮음", "delivery": "불가"},
    "떡볶이": {"calories": 600, "difficulty": "낮음", "delivery": "가능"},
    "피자": {"calories": 1300, "difficulty": "없음", "delivery": "가능"},
    "야식 도시락": {"calories": 800, "difficulty": "중간", "delivery": "불가"},
    "김밥": {"calories": 400, "difficulty": "낮음", "delivery": "가능"},
    "핫도그": {"calories": 450, "difficulty": "낮음", "delivery": "가능"},
    "샌드위치": {"calories": 350, "difficulty": "낮음", "delivery": "가능"},
    "만두": {"calories": 550, "difficulty": "중간", "delivery": "불가"},
    "치즈스틱": {"calories": 300, "difficulty": "낮음", "delivery": "불가"},
    "튀김": {"calories": 600, "difficulty": "중간", "delivery": "가능"},
    "순대": {"calories": 500, "difficulty": "낮음", "delivery": "가능"},
    "샐러드": {"calories": 250, "difficulty": "낮음", "delivery": "가능"},
    "커피/음료": {"calories": 150, "difficulty": "없음", "delivery": "가능"},
    "아이스크림": {"calories": 200, "difficulty": "없음", "delivery": "가능"},
}

# -----------------------------
# 사용자 선택
# -----------------------------
snack_list = list(snacks.keys())
preferences = st.multiselect("먹고 싶은 음식 종류를 선택하세요:", snack_list)

# -----------------------------
# 추천 기능
# -----------------------------
if st.button("추천받기"):
    if preferences:
        choice = random.choice(preferences)
        info = snacks[choice]
        
        st.subheader(f"오늘의 추천 야식: {choice} 🍴")
        st.write(f"**칼로리:** {info['calories']} kcal")
        st.write(f"**조리 난이도:** {info['difficulty']}")
        st.write(f"**배달 가능 여부:** {info['delivery']}")
    else:
        st.warning("하나 이상의 음식을 선택해주세요!")
