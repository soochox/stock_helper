def add_moving_averages(df, ma_list):
    for ma in ma_list:
        df[f"SMA{ma}"] = df['Close'].rolling(window=ma).mean()
    return df

def compute_rsi(df, period=14):
    delta = df['Close'].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()
    rs = avg_gain / avg_loss
    df['RSI'] = 100 - (100 / (1 + rs))
    
    return df
