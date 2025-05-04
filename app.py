import streamlit as st
import pandas as pd
from datetime import date

from modules.data_loader import load_stock_data
from modules.indicators import add_moving_averages, compute_rsi
from modules.chart_builder import build_chart
from modules.trade_logger import show_checklist, show_trade_input, show_trade_log

# 모바일 여부 자동 판별 (고정 높이 설정, 사용자 조정 불가)
st.session_state.is_mobile = False

st.title("📈 트레이딩 도우미 앱")

# 사용자 입력: 종목과 기간 선택
ticker = st.text_input("티커 입력 (예: TQQQ)", value="TQQQ")
period = st.selectbox("조회 기간", ["1mo", "3mo", "6mo", "1y"], index=0)

# 사용자 입력: 이동평균선 설정
st.subheader("📊 이동평균선 설정")
ma_defaults = [5, 20, 60, 200]  # 기본값
ma_periods = []
for i in range(4):
    col1, col2 = st.columns([1, 2])
    enable = col1.checkbox(f"이동평균선 {i+1} 사용", value=True, key=f"ma{i+1}_check")
    days = col2.number_input(f"기간 (일수)", min_value=1, max_value=300, value=ma_defaults[i], key=f"ma{i+1}_days")
    if enable:
        ma_periods.append(days)

# 버튼 클릭 시 차트 생성
if st.button("차트 그리기"):
    df = load_stock_data(ticker, period)
    if df is None or df.empty:
        st.warning("유효한 데이터를 불러오지 못했습니다.")
    else:
        df = add_moving_averages(df, ma_periods)
        df = compute_rsi(df)

        # ✅ 날짜 포맷 간결화
        df['Date'] = pd.to_datetime(df['Date']).dt.strftime('%y-%m-%d')

        # ✅ 최신 종가 및 전일 종가 추출
        current_price = df['Close'].iloc[-1]
        previous_close = df['Close'].iloc[-2] if len(df) > 1 else current_price

        # ✅ 전일 대비 변화율 계산
        price_change_pct = ((current_price - previous_close) / previous_close * 100) if previous_close > 0 else 0

        # ✅ 제목에 현재가 및 변화율 표시
        chart_height = 100
        chart_title = f"{ticker} (현재가: ${current_price:.2f},  {price_change_pct:.2f}%)"

        # ✅ 차트 그리기
        fig = build_chart(df, chart_title, ma_periods, df['Date'], df['Date'], height=chart_height)
        st.plotly_chart(fig, use_container_width=True)

# ✅ 2. 진입 체크리스트
show_checklist()

# ✅ 3. 매매 기록 입력
show_trade_input()

# ✅ 4. 매매 기록 확인
show_trade_log()
