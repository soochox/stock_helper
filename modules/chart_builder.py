import plotly.graph_objects as go
from plotly.subplots import make_subplots

def build_chart(df, ticker, ma_list, date_min, date_max, height=1000):
    """Plotly를 이용한 봉차트 + MA + 거래량 + RSI 시각화 구성 (영업일만 표시)
       색약 고려: 상승 = 투명, 하락 = 검정색
    """
    fig = make_subplots(
        rows=3, cols=1, shared_xaxes=True,
        row_heights=[0.5, 0.25, 0.25],
        vertical_spacing=0.04,
        subplot_titles=(f"{ticker}", "거래량", "RSI (상대강도지수)")
    )

    # 1행: 봉차트 (상승: 투명, 하락: 검정색)
    fig.add_trace(go.Candlestick(
        x=df['Date'], open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'],
        name='Price',
        increasing_line_color='black',
        decreasing_line_color='black',
        increasing_fillcolor='white',
        increasing_line_width=0.4,
        decreasing_fillcolor='black'
    ), row=1, col=1)

    # 이동평균선 겹쳐서 표시
    for ma in ma_list:
        fig.add_trace(go.Scatter(
            x=df['Date'], y=df[f"SMA{ma}"],
            mode='lines', name=f"SMA{ma}", line=dict(width=1.5)
        ), row=1, col=1)

    # 2행: 거래량
    fig.add_trace(go.Bar(
        x=df['Date'], y=df['Volume'], name='거래량',
        marker=dict(color='rgba(150, 150, 250, 0.6)')
    ), row=2, col=1)

    fig.update_yaxes(title_text='Volume', row=2, col=1)
    fig.update_xaxes(type='category', tickformat="%y-%m-%d", row=2, col=1)

    # 3행: RSI
    fig.add_trace(go.Scatter(
        x=df['Date'], y=df['RSI'],
        mode='lines', name='RSI', line=dict(color='orange')
    ), row=3, col=1)

    fig.add_shape(type='line', x0=df['Date'].min(), x1=df['Date'].max(), y0=70, y1=70,
                  line=dict(dash='dot', color='gray'), row=3, col=1)
    fig.add_shape(type='line', x0=df['Date'].min(), x1=df['Date'].max(), y0=30, y1=30,
                  line=dict(dash='dot', color='gray'), row=3, col=1)

    fig.update_xaxes(type='category', tickformat="%y-%m-%d", row=3, col=1)
    fig.update_xaxes(type='category', tickformat="%y-%m-%d", row=1, col=1)

    # 전역 설정
    fig.update_layout(
        height=height,
        xaxis_rangeslider_visible=False,
        showlegend=True
    )

    return fig
