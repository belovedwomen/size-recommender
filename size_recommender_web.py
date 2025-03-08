import streamlit as st
import os

# 파일 경로 확인 함수
def check_image_exists(image_path):
    if os.path.exists(image_path):
        return image_path
    else:
        st.error(f"이미지 파일이 존재하지 않습니다: {image_path}")
        return None

# 로고 표시
logo_path = "logo.png"
logo = check_image_exists(logo_path)
if logo:
    st.image(logo, width=200)  # 로고 이미지 표시

st.title("빌러드우먼 코로듀이 골덴 원피스 사이즈 추천")

# 상품 사진 표시
dress_image_path = "dress_image.jpg"
dress_image = check_image_exists(dress_image_path)
if dress_image:
    st.image(dress_image, caption="코로듀이 골덴 원피스", width=300)

# 브래지어 사이즈를 가슴 둘레로 변환
def convert_bra_to_bust(bra_size):
    bra_chart = {
        "65A": 76, "65B": 78, "65C": 80, "65D": 82,
        "70A": 81, "70B": 83, "70C": 85, "70D": 87,
        "75A": 86, "75B": 88, "75C": 90, "75D": 92,
        "80A": 91, "80B": 93, "80C": 95, "80D": 97,
        "85A": 96, "85B": 98, "85C": 100, "85D": 102,
        "90A": 101, "90B": 103, "90C": 105, "90D": 107,
        "95A": 106, "95B": 108, "95C": 110, "95D": 112
    }
    return bra_chart.get(bra_size.upper(), None)

# 사이즈 추천 함수
def recommend_size(height, weight, bra_size):
    size_chart = {
        "M": {"bust": 90, "length": 103},
        "L": {"bust": 94, "length": 104},
        "XL": {"bust": 98, "length": 105},
        "XXL": {"bust": 102, "length": 106},
        "XXXL": {"bust": 106, "length": 107}
    }

    bust = convert_bra_to_bust(bra_size)
    if bust is None:
        return None, None

    # 기본 추천 사이즈 설정
    initial_size = "M"
    for size, data in size_chart.items():
        if abs(data["bust"] - bust) <= 4:
            initial_size = size
            break
    if bust >= 100:
        initial_size = "XXL"  # 기존 XL를 XXL로 조정

    # 몸무게 기반 사이즈 조정
    weight_based_size = "M"
    if weight <= 50:
        weight_based_size = "M"
    elif 50 < weight <= 60:
        weight_based_size = "L"
    elif 60 < weight <= 70:
        weight_based_size = "XL"
    elif 70 < weight <= 80:
        weight_based_size = "XXL"
    else:
        weight_based_size = "XXXL"

    # BMI 계산 & 보정값 적용
    bmi = weight / (height / 100) ** 2
    bmi_adjustment = 0
    if bmi >= 23:
        bmi_adjustment = 1
    if bmi >= 27:
        bmi_adjustment = 2
    if bmi >= 30:
        bmi_adjustment = 3

    # 최종 사이즈 결정
    size_order = ["M", "L", "XL", "XXL", "XXXL"]
    initial_index = size_order.index(initial_size)
    weight_index = size_order.index(weight_based_size)
    combined_index = max(initial_index, weight_index) + bmi_adjustment
    recommended_size = size_order[min(combined_index, len(size_order) - 1)]

    return recommended_size, bust

# 입력 폼
height = st.number_input("키 (cm)", min_value=100, max_value=200, value=170)
weight = st.number_input("몸무게 (kg)", min_value=30, max_value=150, value=68)
bra_size_options = ["65A", "65B", "65C", "65D", "70A", "70B", "70C", "70D", "75A", "75B", "75C", "75D",
                    "80A", "80B", "80C", "80D", "85A", "85B", "85C", "85D", "90A", "90B", "90C", "90D",
                    "95A", "95B", "95C", "95D"]
bra_size = st.selectbox("브래지어 사이즈", bra_size_options, index=bra_size_options.index("85C"))

if st.button("추천 받기"):
    result = recommend_size(height, weight, bra_size)
    if result is not None:
        recommended_size, bust = result
        st.success(f"입력하신 브래지어 사이즈({bra_size})를 기준으로 가슴 둘레는 약 {bust}cm로 추정됩니다.")
        st.success(f"추천 사이즈: {recommended_size}")
        st.info("이 추천으로 반품을 줄여 환경에 기여합니다! 😊")

# 디자인 개선
st.markdown("""
    <style>
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        font-size: 16px;
    }
    .stApp {background-color: #f0f0f0;}
    </style>
""", unsafe_allow_html=True)
