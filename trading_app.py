import streamlit as st
from modules.data_loader import load_stock_data
from modules.indicators import add_moving_averages, compute_rsi
from modules.chart_builder import build_chart

st.title("📈 트레이딩 도우미 앱")

ticker = st.text_input("티커 입력 (예: TQQQ)", value="TQQQ")
period = st.selectbox("조회 기간", ["1mo", "3mo", "6mo", "1y"], index=0)

st.subheader("📊 이동평균선 설정")
ma_periods = []
for i in range(1, 6):
    col1, col2 = st.columns([1, 2])
    enable = col1.checkbox(f"이동평균선 {i} 사용", key=f"ma{i}_check")
    days = col2.number_input(f"기간 (일수)", min_value=1, max_value=100, value=20, key=f"ma{i}_days")
    if enable:
        ma_periods.append(days)

if st.button("차트 그리기"):
    df = load_stock_data(ticker, period)
    if df is None or df.empty:
        st.warning("유효한 데이터를 불러오지 못했습니다.")
    else:
        df = add_moving_averages(df, ma_periods)
        df = compute_rsi(df)
        fig = build_chart(df, ticker, ma_periods)
        st.plotly_chart(fig, use_container_width=True)
