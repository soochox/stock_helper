import streamlit as st
import pandas as pd
from datetime import date

def show_checklist():
    st.markdown("---")
    st.header("✅ 진입 체크리스트")
    st.checkbox("RSI < 30")
    st.checkbox("최근 거래량 증가")
    st.checkbox("상승 추세")
    st.checkbox("캔들 패턴 출현")
    st.checkbox("시장 흐름 우호적")
    st.checkbox("시장 구조 변화")
    st.checkbox("지지선 근처")

def show_trade_input():
    st.markdown("---")
    st.header("🧾 매매 기록")

    symbol = st.text_input("종목명", "")
    entry_date = st.date_input("진입일", date.today())
    exit_date = st.date_input("청산일", date.today())
    entry_price = st.number_input("진입가", min_value=0.0)
    exit_price = st.number_input("청산가", min_value=0.0)
    stop_price = st.number_input("손절 예정가", min_value=0.0)
    target_price = st.number_input("익절 예정가", min_value=0.0)

    # 손익비 계산
    rrr_value = ""
    if entry_price > 0 and stop_price > 0 and target_price > 0:
        risk = abs(entry_price - stop_price)
        reward = abs(target_price - entry_price)
        if risk > 0:
            rrr_value = round(reward / risk, 2)

    st.text_input("손익비 (자동 계산됨)", value=str(rrr_value), disabled=True)

    reason = st.text_area("매매 판단 근거")
    feedback = st.text_area("결과 피드백")

    if st.button("기록 저장"):
        profit_pct = ((exit_price - entry_price) / entry_price * 100) if entry_price > 0 else 0
        new_record = {
            "종목": symbol,
            "진입일": entry_date,
            "청산일": exit_date,
            "진입가": entry_price,
            "청산가": exit_price,
            "손절 예정가": stop_price,
            "익절 예정가": target_price,
            "손익비": rrr_value,
            "수익률(%)": round(profit_pct, 2),
            "근거": reason,
            "피드백": feedback
        }

        if "records" not in st.session_state:
            st.session_state.records = []

        st.session_state.records.append(new_record)
        st.success("매매 기록이 저장되었습니다!")

def show_trade_log():
    st.markdown("---")
    st.subheader("📊 누적 매매 기록")

    if "records" in st.session_state and st.session_state.records:
        symbols = sorted({r['종목'] for r in st.session_state.records if r['종목']})
        selected_symbol = st.selectbox("📌 종목 필터", ["전체 보기"] + symbols)

        df = pd.DataFrame(st.session_state.records)
        if selected_symbol != "전체 보기":
            df = df[df['종목'] == selected_symbol]

        st.dataframe(df)
    else:
        st.info("아직 저장된 기록이 없습니다.")