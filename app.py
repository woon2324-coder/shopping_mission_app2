import streamlit as st
import pandas as pd

# Load product data
def load_products():
    try:
        return pd.read_csv('products.csv')
    except Exception:
        st.error('products.csv 파일이 없거나 비어 있습니다. 업로드를 확인하세요.')
        return pd.DataFrame()

# Initialize session state
if 'stage' not in st.session_state:
    st.session_state.stage = 'start'
if 'budget' not in st.session_state:
    st.session_state.budget = None
if 'cart' not in st.session_state:
    st.session_state.cart = []

products = load_products()

st.title("📘 학생 쇼핑 미션 앱")

# -----------------------------
# 1. Start Screen
# -----------------------------
if st.session_state.stage == 'start':
    st.header("미션 선택하기")
    st.write("3가지 예산 중 하나를 선택하세요.")

    budget_options = {
        '미션 1: 10,000원': 10000,
        '미션 2: 20,000원': 20000,
        '미션 3: 30,000원': 30000
    }

    selected_mission = st.selectbox("미션 선택", list(budget_options.keys()))

    if st.button("쇼핑 시작하기"):
        st.session_state.budget = budget_options[selected_mission]
        st.session_state.stage = 'shopping'
        st.rerun()

# -----------------------------
# 2. Shopping Screen
# -----------------------------
elif st.session_state.stage == 'shopping':
    st.header("🛒 쇼핑하기")
    st.write(f"**예산: {st.session_state.budget:,}원**")

    if products.empty:
        st.stop()

    categories = products['category'].unique()
    category = st.selectbox("카테고리 선택", categories)

    filtered = products[products['category'] == category]
    item = st.selectbox("상품 선택", filtered['name'])

    quantity = st.number_input("수량", min_value=1, max_value=20, value=1)

    selected_row = filtered[filtered['name'] == item].iloc[0]
    price = selected_row['price']
    total_price = price * quantity

    st.write(f"가격: {price:,}원 → 총 {total_price:,}원")

    if st.button("장바구니 담기"):
        st.session_state.cart.append({
            'name': item,
            'price': price,
            'quantity': quantity,
            'total': total_price,
            'image': selected_row.get('image_url', '')
        })
        st.success("장바구니에 추가되었습니다!")

    st.subheader("🧺 장바구니")
    cart_df = pd.DataFrame(st.session_state.cart)
    if not cart_df.empty:
        st.table(cart_df[['name', 'price', 'quantity', 'total']])
        sum_total = cart_df['total'].sum()
        st.write(f"### 총합: {sum_total:,}원")
    else:
        st.write("장바구니가 비어 있습니다.")

    if st.button("결과보기"):
        st.session_state.stage = 'result'
        st.rerun()

# -----------------------------
# 3. Result Screen
# -----------------------------
elif st.session_state.stage == 'result':
    st.header("📊 결과 화면")

    cart_df = pd.DataFrame(st.session_state.cart)
    if cart_df.empty:
        st.write("장바구니가 비어 있습니다.")
        st.stop()

    st.write("### 장바구니 내역")
    st.table(cart_df[['name', 'price', 'quantity', 'total']])

    total_cost = cart_df['total'].sum()
    st.write(f"### 총 사용 금액: {total_cost:,}원")
    st.write(f"### 남은 금액: {st.session_state.budget - total_cost:,}원")

    st.write("---")
    reason = st.text_area("📝 구매 이유를 작성하세요", height=200)

    if st.button("이미지로 결과 저장하기"):
        st.success("이미지 저장 기능은 추후 구현 가능합니다.")

    if st.button("처음으로 돌아가기"):
        st.session_state.stage = 'start'
        st.session_state.cart = []
        st.rerun()
