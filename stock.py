import pandas as pd
import yfinance as yf
import altair as alt
import streamlit as st

st.title('所有株　株価可視化アプリ')

st.sidebar.write("""
    # 所有株 株価
    こちらは自身所有の株の株価可視化ツールです。
    以下のオプションから表示日数を指定してください。
    """)

st.sidebar.write("""
    ## 表示日数選択
""")

days = st.sidebar.slider('日数',1,50,20)

st.write(f"""
    ### 過去 **{days}**の株価
""")

@st.cache_data
def get_data(days,tickers):
    df =pd.DataFrame()
    for company in tickers.keys():
        tkr = yf.Ticker(tickers[company])
        hist = tkr.history(period=f'{days}d')
        hist.head = hist.index.strftime('%d %B % Y')
        hist = hist[['Close']]
        hist.columns =[company]
        hist = hist.T
        hist.index.name = 'Name'
        df = pd.concat([df,hist])
    return df

try:
    st.sidebar.write("""
    ## 株価の範囲指定
    """)
    ymin,ymax = st.sidebar.slider(
        '範囲を指定してください。',
        0.0, 3500.0,(0.0, 1500.0)
    )

    tickers = {
        'kobelco':'5406.T',
        'rikei':'8226.T',
        'nsc':'3940.T',
        'tokaisoft':'4430.T'
    }

    df = get_data(days,tickers)
    companies = st.multiselect(
        '会社名を選択してください。',
        list(df.index),
        ['kobelco','rikei','nsc','tokaisoft']
    )

    if not companies:
        st.error('少なくとも一社は選んで下さい')
    else:
        data = df.loc[companies]
        st.write("### 株価(JPY)",data.sort_index())
        data = data.T.reset_index()
        data = pd.melt(data, id_vars=['Date']).rename(
            columns={'value': 'Stock Prices(JPY)'}
    )

    chart = (
        alt.Chart(data)
        .mark_line(opacity=0.8, clip=True)
        .encode(
            x="Date:T",
            y=alt.Y("Stock Prices(JPY):Q", stack=None, scale=alt.Scale(domain=[ymin, ymax])),
            color='Name:N'
        )
    )

    st.altair_chart(chart,use_container_width=True)
except:
    st.error(
        "何かエラーが起きています！"
    )
