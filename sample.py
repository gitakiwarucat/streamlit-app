import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(page_title="学習メモアプリ", page_icon="📝", layout="centered")

# 背景画像＋スタイル
st.markdown("""
<style>
.stApp {
    background-image: url("https://images.unsplash.com/photo-1519389950473-47ba0277781c");
    background-size: cover;
    background-attachment: fixed;
}

.block-container {
    background: rgba(255, 255, 255, 0.85);
    padding: 2rem;
    border-radius: 15px;
}

h1, h2, h3 {
    color: #333;
}

.stButton>button {
    background-color: #4CAF50;
    color: white;
    border-radius: 10px;
    padding: 10px 20px;
    border: none;
}

.stButton>button:hover {
    background-color: #45a049;
}

</style>
""", unsafe_allow_html=True)

st.title("📝 学習メモアプリ")
st.write("学習内容を記録して、理解度を可視化できます")

# セッション保存
if "records" not in st.session_state:
    st.session_state.records = pd.DataFrame(
        columns=["日付", "名前", "カテゴリ", "内容", "理解度"]
    )

# 入力フォーム
with st.form("memo_form"):
    st.subheader("📌 学習入力")

    col1, col2 = st.columns(2)

    with col1:
        name = st.text_input("名前")
        category = st.selectbox(
            "カテゴリ",
            ["Python", "Streamlit", "Salesforce", "AWS", "C++", "その他"]
        )

    with col2:
        study_date = st.date_input("日付", date.today())
        level = st.slider("理解度", 0, 100, 50)

    today_task = st.text_area("今日勉強したこと")

    submitted = st.form_submit_button("記録する")

if submitted:
    if today_task:
        new_record = pd.DataFrame([{
            "日付": study_date,
            "名前": name,
            "カテゴリ": category,
            "内容": today_task,
            "理解度": level
        }])

        st.session_state.records = pd.concat(
            [st.session_state.records, new_record],
            ignore_index=True
        )

        st.success("記録しました！")
    else:
        st.warning("学習内容を入力してください")

st.divider()

# 表示
st.subheader("📊 学習記録一覧")

if not st.session_state.records.empty:
    st.dataframe(st.session_state.records, use_container_width=True)

    st.subheader("📈 理解度の推移")
    chart_data = st.session_state.records.set_index("日付")["理解度"]
    st.line_chart(chart_data)

    # ダウンロード
    csv = st.session_state.records.to_csv(index=False).encode("utf-8-sig")

    st.download_button(
        label="📥 CSVダウンロード",
        data=csv,
        file_name="study_records.csv",
        mime="text/csv"
    )

else:
    st.info("まだ記録がありません")