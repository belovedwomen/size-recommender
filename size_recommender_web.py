import streamlit as st

# ✅ 페이지 스타일 (브랜드 컬러 적용 & 고급스러운 디자인)
st.markdown("""
    <style>
    .stApp {
        background-color: #EDE6F2; /* 브랜드 컬러 배경 */
        font-family: 'Noto Sans', sans-serif; /* 고급스러운 폰트 */
    }
    .stButton>button {
        background-color: #222 !important; /* 블랙 버튼 */
        color: #FFFFFF !important; /* 글씨 하얀색 */
        font-size: 18px !important;
        border-radius: 8px !important;
        padding: 12px 20px !important;
        font-weight: bold !important;
        border: 2px solid #A68A64 !important; /* 골드 테두리 유지 */
    }

    /* 버튼 내부 텍스트 색상을 강제로 흰색으로 지정 */
    .stButton>button * {
        color: #FFFFFF !important;
    }
    .stMarkdown, h1, h2, h3, h4, h5, h6, p, div {
        color: #333 !important; /* 검정색 텍스트 */
        font-family: 'Noto Sans', sans-serif;
    }
    .recommend-box {
        background-color: #E1D7EB; /* 조금 더 진한 배경색 */
        padding: 15px;
        border-radius: 15px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
        font-size: 18px;
        color: #333;
        display: flex;
        align-items: center;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# ✅ 제목 (고급스럽게 Bold 처리)
st.title("💜 **빌러드우먼 체형보완 코디**")
st.subheader("✨ **코로듀이 골덴 원피스 사이즈 추천**")

# ✅ 로고 이미지 표시
logo_url = "logo.png"
fallback_logo_url = "https://via.placeholder.com/200"
try:
    st.image(logo_url, width=200)
except Exception:
    st.image(fallback_logo_url, width=200)

# ✅ 상품 이미지 표시
dress_image_url = "dress_image.jpg"
fallback_dress_url = "https://via.placeholder.com/300"
try:
    st.image(dress_image_url, caption="코로듀이 골덴 원피스", width=300)
except Exception:
    st.image(fallback_dress_url, caption="코로듀이 골덴 원피스", width=300)

# ✅ 브래지어 사이즈를 가슴 둘레로 변환
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

# ✅ 사이즈 추천 함수 (보정값 추가)
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
        initial_size = "XXL"

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

    # ✅ BMI 보정값 추가 (23 이상도 보정)
    bmi = weight / (height / 100) ** 2
    bmi_adjustment = 0
    if bmi >= 23:
        bmi_adjustment = 1
    if bmi >= 27:
        bmi_adjustment = 2
    if bmi >= 30:
        bmi_adjustment = 3

    # ✅ 키가 170 이상이고 XXL 이상이면 한 단계 추가 보정
    if height >= 170 and initial_size in ["XXL", "XXXL"]:
        bmi_adjustment += 1

    # 최종 사이즈 결정
    size_order = ["M", "L", "XL", "XXL", "XXXL"]
    initial_index = size_order.index(initial_size)
    weight_index = size_order.index(weight_based_size)
    combined_index = max(initial_index, weight_index) + bmi_adjustment
    recommended_size = size_order[min(combined_index, len(size_order) - 1)]

    return recommended_size, bust

# ✅ 입력 UX 개선 (슬라이더 적용)
st.subheader("신체 정보 입력")

height = st.slider("키 (cm)", 140, 190, 170, step=1)
weight = st.slider("몸무게 (kg)", 40, 100, 68, step=1)

st.subheader("브래지어 정보 입력")

bra_size_options = ["65A", "65B", "65C", "65D", "70A", "70B", "70C", "70D", "75A", "75B", "75C", "75D",
                    "80A", "80B", "80C", "80D", "85A", "85B", "85C", "85D", "90A", "90B", "90C", "90D",
                    "95A", "95B", "95C", "95D"]
bra_size = st.selectbox("브래지어 사이즈", bra_size_options, index=bra_size_options.index("85C"))

if st.button("✨ 사이즈 추천 받기"):
    result = recommend_size(height, weight, bra_size)
    if result is not None:
        recommended_size, bust = result

        # ✅ 판매자 얼굴 + 추천 박스 내부 배치
        col1, col2 = st.columns([1, 4])
        with col1:
            st.image("eune.JPG", width=120)  # 얼굴 크기 증가
        with col2:
            st.markdown(
                f"""
                <div style="
                    background-color: #F7F7F7; 
                    padding: 15px; 
                    border-radius: 15px;
                    box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
                    font-size: 16px;
                    display: flex;
                    align-items: center;
                ">
                    <strong>🎯 추천 사이즈: {recommended_size}</strong><br>
                    <span style="color: #666;">브래지어 사이즈({bra_size}) → 가슴 둘레 추정: {bust}cm</span>
                </div>
                """,
                unsafe_allow_html=True
            )

        # ✅ "왜 이 사이즈가 추천되었나요?" 유지
        st.markdown(f"### 📝 왜 **{recommended_size}** 사이즈가 추천되었나요?")
        st.info(
            f"✔ 키({height}cm)와 몸무게({weight}kg)를 기준으로 분석된 결과입니다.\n"
            f"✔ 브래지어 사이즈({bra_size}) 기준 가슴 둘레가 {bust}cm로 측정되었습니다.\n"
            f"✔ BMI({round(weight / (height / 100) ** 2, 1)}) 기준으로 적절한 사이즈가 추천되었습니다."
        )

# ✅ ESG 메시지 추가
st.info("이 추천으로 반품을 줄여 환경에 기여합니다! 😊")