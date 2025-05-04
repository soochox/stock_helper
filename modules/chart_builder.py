import plotly.graph_objects as go
from plotly.subplots import make_subplots


def build_chart(df, title, ma_list, date_min, date_max, height=1000):
    """
    Plotly로 구성한 봉차트 + 이동평균 + 거래량 + RSI 시각화
    - 색약 대응: 상승 = 흰색, 하락 = 검정색
    - 날짜 라벨 회전 및 형식 축소
    - 모바일 대응 시 legend 위치 조정 가능
    - 범례 크기 축소 및 사용자 차트 리사이징 제한
    """
    fig = make_subplots(
        rows=3, cols=1, shared_xaxes=True,
        row_heights=[0.5, 0.25, 0.25],
        vertical_spacing=0.04,
        subplot_titles=(title, "거래량", "RSI")
    )

    # 봉차트
    fig.add_trace(go.Candlestick(
        x=df['Date'],
        open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'],
        name='Price',
        increasing_line_color='black', increasing_fillcolor='white', increasing_line_width=0.5,
        decreasing_line_color='yellow', decreasing_fillcolor='black', decreasing_line_width=0.5,
        showlegend=True
    ), row=1, col=1)

    # 이동평균선
    for ma in ma_list:
        fig.add_trace(go.Scatter(
            x=df['Date'], y=df[f"SMA{ma}"],
            mode='lines', name=f"SMA{ma}", line=dict(width=1.5)
        ), row=1, col=1)

    # 거래량
    fig.add_trace(go.Bar(
        x=df['Date'], y=df['Volume'], name='거래량',
        marker=dict(color='rgba(150, 150, 250, 0.6)')
    ), row=2, col=1)
    fig.update_yaxes(title_text='', row=2, col=1)

    # RSI
    fig.add_trace(go.Scatter(
        x=df['Date'], y=df['RSI'],
        mode='lines', name='RSI', line=dict(color='orange')
    ), row=3, col=1)
    fig.add_shape(type='line', x0=df['Date'].min(), x1=df['Date'].max(), y0=70, y1=70,
                  line=dict(dash='dot', color='gray'), row=3, col=1)
    fig.add_shape(type='line', x0=df['Date'].min(), x1=df['Date'].max(), y0=30, y1=30,
                  line=dict(dash='dot', color='gray'), row=3, col=1)

    # X축 포맷 일괄 적용: 세로 회전
    for r in [1, 2, 3]:
        fig.update_xaxes(type='category', tickangle=90, row=r, col=1)

    # 범례 위치 및 크기 조정, 드래그 확대 제한
    fig.update_layout(
        height=height,
        xaxis_rangeslider_visible=False,
        showlegend=True,
        dragmode=False,
        legend=dict(
        orientation="v",
        yanchor="top",
        y=0.99,
        xanchor="left",
        x=0.01,
        font=dict(size=8),
        bgcolor="rgba(255,255,255,0.5)",  # 반투명 배경
        borderwidth=0)
    )
        
    return fig
