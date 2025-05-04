import yfinance as yf
import pandas as pd

def load_stock_data(ticker, period):
    """ yfinance를 사용해 주가 데이터 로드 및 전처리 """
    data = yf.download(ticker, period=period, interval='1d', group_by='ticker')
    if data.empty:
        return None
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.droplevel(0)  # 다중 컬럼 제거
    data = data.reset_index()
    data['Date'] = pd.to_datetime(data['Date'])
    data['DateStr'] = data['Date'].dt.strftime('%Y-%m-%d')  # 문자열로 변환된 날짜 컬럼 추가
    return data