import streamlit as st
import pandas as pd 
import matplotlib.pyplot as plt
import datetime

# layout wide
# st.set_page_config(layout='wide')
# hide menu
st.markdown(
    """
    <style>
    #root > div:nth-child(1) > div.withScreencast > div > header > div.stAppToolbar.st-emotion-cache-15ecox0.e4hpqof2 {
        visibility: hidden;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
# center of the layout
st.markdown('<h1 style="text-align: center;">Giá Vàng</h1>', unsafe_allow_html=True)
st.divider()

# st.header('Welcome to the dash board page!')
# st.markdown(f'Today: {datetime.datetime.now().strftime('%d-%m-%Y')}')


st.html('''
<style>
div[data-testid="stMultiSelect"] [data-baseweb="select"] > div > div {
    max-height: 38px !important; /* Fix the height */
    overflow: auto !important;
}
</style>
''')


# divide to 5 columns
col1, col2 = st.columns(2)
@st.cache_data
def get_data():
    link = r"https://docs.google.com/spreadsheets/d/e/2PACX-1vQxzmxnjv81baBSxDhGOR6eWEdAeRJrRJnMgLF8H-ctg6N1LDrqIX3Q3O0urcfImcQFbMeLrBxLk6wy/pub?gid=0&single=true&output=csv"
    df = pd.read_csv(link).iloc[1 :, [1, 4, 5]]
    df.columns = ["Date", "PNJ", "SJC"]
    df["Date"] = pd.to_datetime(df["Date"]).dt.date
    df["PNJ close"] = df["PNJ"].str.strip().str.replace(r".*mua.*", "", regex=True).str.split(" ", expand=True)[1].astype('float')
    df["SJC close"] = df["SJC"].str.strip().str.replace(r".*mua.*", "", regex=True).str.split(" ", expand=True)[1].astype('float')
    df = df.set_index("Date")
    # regex replace *mua* with empty string
    return df

df = get_data()
col1.write(f'Last updated {df.dropna().index[-1].strftime("%d-%m-%Y")}')
# st.dataframe(df)
st.line_chart(df[["PNJ close", "SJC close"]], width=1000, height=500, use_container_width=False)
# show legend


# fig, ax = plt.subplots()
# df.plot(x="Date", y=["PNJ close", "SJC close"], figsize=(10, 5), ax=ax)
# ax.spines['top'].set_visible(False)
# ax.spines['right'].set_visible(False)

# col1.pyplot(fig)