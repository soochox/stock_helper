import plotly.graph_objects as go
from plotly.subplots import make_subplots


def build_chart(df, title, ma_list, date_min, date_max, height=1000):
    """
    Plotly를 이용한 봉차트 + MA + 거래량 + RSI 시각화 구성 (영업일만 표시)
    색약 고려: 상승 = 흰색, 하락 = 검정
    모바일 화면일 경우 높이 축소, 범례는 겹침 배치
    """
    fig = make_subplots(
        rows=3, cols=1, shared_xaxes=True,
        row_heights=[0.5, 0.25, 0.25],
        vertical_spacing=0.04,
        subplot_titles=(title, "거래량", "RSI (상대강도지수)")
    )

    # 1행: 봉차트 (상승: 흰색, 하락: 검정)
    fig.add_trace(go.Candlestick(
        x=df['Date'], open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'],
        name='Price',
        increasing_line_color='black', decreasing_line_color='black',
        increasing_fillcolor='white', decreasing_fillcolor='black',
        increasing_line_width=0.5, decreasing_line_width=0.5,
        showlegend=True
    ), row=1, col=1)

    # 이동평균선
    for ma in ma_list:
        fig.add_trace(go.Scatter(
            x=df['Date'], y=df[f"SMA{ma}"],
            mode='lines', name=f"SMA{ma}", line=dict(width=1.5)
        ), row=1, col=1)

    # 2행: 거래량 (Y축 레이블 제거)
    fig.add_trace(go.Bar(
        x=df['Date'], y=df['Volume'], name='거래량',
        marker=dict(color='rgba(150, 150, 250, 0.6)')
    ), row=2, col=1)
    fig.update_yaxes(title_text='', row=2, col=1)

    # 3행: RSI + 기준선
    fig.add_trace(go.Scatter(
        x=df['Date'], y=df['RSI'],
        mode='lines', name='RSI', line=dict(color='orange')
    ), row=3, col=1)
    fig.add_shape(type='line', x0=date_min.min(), x1=date_max.max(), y0=70, y1=70,
                  line=dict(dash='dot', color='gray'), row=3, col=1)
    fig.add_shape(type='line', x0=date_min.min(), x1=date_max.max(), y0=30, y1=30,
                  line=dict(dash='dot', color='gray'), row=3, col=1)

    # X축 날짜 포맷 간결화
    for i in [1, 2, 3]:
        fig.update_xaxes(type='category', tickangle=0, row=i, col=1)

    # 전역 설정 (모바일이면 legend 겹침)
    legend_position = dict(x=0.01, y=0.99) if height < 600 else dict()
    fig.update_layout(
        height=height,
        xaxis_rangeslider_visible=False,
        showlegend=True,
        legend=legend_position
    )

    return fig
