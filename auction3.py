import streamlit as st

def calculate_bid_price(appraisal_price, lowest_price, leverage_interest_rate, interior_cost, acquisition_cost, vacancy_cost, auction_rate, sell_price, non_recognized_expenses):
    # 백만 원 단위 입력을 원 단위로 변환
    appraisal_price = appraisal_price * 1000000
    lowest_price = lowest_price * 1000000
    interior_cost = interior_cost * 1000000
    acquisition_cost = acquisition_cost * 1000000
    vacancy_cost = vacancy_cost * 1000000
    sell_price = sell_price * 1000000
    non_recognized_expenses = non_recognized_expenses * 1000000

    bid_price = appraisal_price * auction_rate
    leverage = min(appraisal_price * 0.6, bid_price * 0.8)
    required_cash = bid_price - leverage

    if bid_price <= 600000000:
        registration_tax = bid_price * 0.01 - acquisition_cost
    elif bid_price >= 900000000:
        registration_tax = bid_price * 0.03 - acquisition_cost
    else:
        registration_tax = bid_price * (0.01 + 0.02 * (bid_price - 600000000) / 300000000) -acquisition_cost

    if bid_price <= 100000000:
        national_housing_bond = 300000
    elif bid_price <= 200000000:
        national_housing_bond = 700000
    elif bid_price <= 300000000:
        national_housing_bond = 1200000
    elif bid_price <= 400000000:
        national_housing_bond = 1550000
    elif bid_price <= 500000000:
        national_housing_bond = 1900000
    elif bid_price <= 600000000:
        national_housing_bond = 2300000
    elif bid_price <= 700000000:
        national_housing_bond = 2700000
    else:
        national_housing_bond = 4000000

    registration_fee = 200000
    legal_fee = 300000
    loan_prepayment_fee = leverage * 0.0075
    brokerage_fee = sell_price * 0.0055
    leverage_interest = leverage * leverage_interest_rate

    total_costs = (registration_tax + national_housing_bond + registration_fee +
                   legal_fee + interior_cost + leverage_interest +
                   loan_prepayment_fee + brokerage_fee + vacancy_cost)

    capital_gain = sell_price - bid_price
    net_capital_gain = capital_gain - total_costs
    capital_gains_tax = calculate_capital_gains_tax(net_capital_gain)
    net_profit = net_capital_gain - capital_gains_tax - non_recognized_expenses

    required_cash_for_bid = required_cash + total_costs + non_recognized_expenses + capital_gains_tax
    profit_rate = 2* (net_profit / required_cash_for_bid) * 100

    return {
        "감정가": round(appraisal_price / 1000000, 1),
        "최저가": round(lowest_price / 1000000, 1),
        "낙찰가": round(bid_price / 1000000, 1),
        "레버리지": round(leverage / 1000000, 1),
        "입찰시 필요한 현금": round(required_cash / 1000000, 1),
        "필요비용(취등록세,국민주택채권,법무비,수선비,6개월대출이자,중개수수료,명도비)": round(total_costs / 1000000, 1),
        "양도차익": round(capital_gain / 1000000, 1),
        "실양도차익": round(net_capital_gain / 1000000, 1),
        "양도세": round(capital_gains_tax / 1000000, 1),
        "비인정필요비용(관리비,강제집행비)": round(non_recognized_expenses / 1000000, 1),
        "순수익": round(net_profit / 1000000, 1),
        "총투입비용": round(required_cash_for_bid / 1000000, 1),
        "수익률": round(profit_rate, 1),
        "취등록세": round(registration_tax / 1000000, 1)
    }

def calculate_capital_gains_tax(capital_gain):
    if capital_gain <= 12000000:
        tax_rate = 0.06
        deduction = 0
    elif capital_gain <= 46000000:
        tax_rate = 0.15
        deduction = 1080000
    elif capital_gain <= 88000000:
        tax_rate = 0.24
        deduction = 5220000
    elif capital_gain <= 150000000:
        tax_rate = 0.35
        deduction = 14900000
    elif capital_gain <= 300000000:
        tax_rate = 0.38
        deduction = 19400000
    elif capital_gain <= 500000000:
        tax_rate = 0.40
        deduction = 25400000
    elif capital_gain <= 1000000000:
        tax_rate = 0.42
        deduction = 35400000
    else:
        tax_rate = 0.45
        deduction = 65400000

    capital_gains_tax = capital_gain * tax_rate - deduction
    return capital_gains_tax

def format_currency(value):
    return f"{value:,.1f} 백만 원"

def main():
    st.set_page_config(page_title="경매 수익률 계산기", layout="wide")

    st.title("경매 수익률 계산기")

    st.markdown("""
    <style>
    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
        padding-left: 3rem;
        padding-right: 3rem;
    }
    .stButton button {
        background-color: #007bff;
        color: white;
    }
    .stMarkdown p {
        margin-bottom: 0.5rem;
    }
    .result {
        color: blue;
        font-weight: bold;
        font-size: 1.2em;
    }
    </style>
    """, unsafe_allow_html=True)

    with st.form("auction_form"):
        st.header("입력 데이터")
        col1, col2, col3 = st.columns(3)
        with col1:
            auction_rate = st.number_input("낙찰가율(%)", min_value=0, step=1, format="%d")
            sell_price = st.number_input("매도가(백만원)", min_value=0, step=1, format="%d")
            appraisal_price = st.number_input("감정가(백만원)", min_value=0, step=1, format="%d")

        with col2:
            lowest_price = st.number_input("최저가(백만원)", min_value=0, step=1, format="%d")
            leverage_interest_rate = st.number_input("대출이자율(%)", min_value=0, step=1, format="%d")
            interior_cost = st.number_input("수선비용(백만원)", min_value=0, step=1, format="%d")

        with col3:
            acquisition_cost = st.number_input("인수비용(백만원)", min_value=0, step=1, format="%d")
            vacancy_cost = st.number_input("명도비용(백만원)", min_value=0, step=1, format="%d")
            non_recognized_expenses = st.number_input("비인정필요비용(백만원)", min_value=0, step=1, format="%d")

        submit_button = st.form_submit_button("계산하기")

    if submit_button:
        result = calculate_bid_price(appraisal_price, lowest_price, leverage_interest_rate / 100, interior_cost, acquisition_cost, vacancy_cost, auction_rate / 100, sell_price, non_recognized_expenses)

        st.header("계산 결과")

        st.markdown(f"<p class='result'>낙찰가: {format_currency(result['낙찰가'])}</p>", unsafe_allow_html=True)
        st.markdown(f"<p class='result'>순수익: {format_currency(result['순수익'])}</p>", unsafe_allow_html=True)
        st.markdown(f"<p class='result'>수익률: {result['수익률']:.1f}%</p>", unsafe_allow_html=True)
        st.markdown(f"<p class='result'>입찰시 필요한 현금: {format_currency(result['입찰시 필요한 현금'])}</p>", unsafe_allow_html=True)

        result.pop("낙찰가")
        result.pop("순수익")
        result.pop("수익률")
        result.pop("입찰시 필요한 현금")

        st.subheader("상세 계산 결과")
        formatted_result = {k: f"{v:,.1f} 백만원" for k, v in result.items()}
        st.table(formatted_result)

if __name__ == "__main__":
    main()
