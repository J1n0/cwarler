import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from konlpy.tag import Okt

# 페이지 설정
st.set_page_config(layout="wide")
st.title("📊 Google Play 리뷰 감정 워드클라우드")
st.markdown("**지정된 로컬 파일**을 불러와 중립을 제외한 긍정/부정 리뷰 워드클라우드를 생성합니다.")

# ✅ 파일 경로 설정 (CSV 또는 Excel)
file_path = "./google_play_reviews_labeled.csv" 
ext = os.path.splitext(file_path)[-1].lower()

# ✅ 파일 불러오기
try:
    if ext == ".csv":
        df = pd.read_csv(file_path)
    elif ext in [".xlsx", ".xls"]:
        df = pd.read_excel(file_path, engine="openpyxl")
    else:
        st.error("지원하지 않는 파일 형식입니다.")
        st.stop()
except Exception as e:
    st.error(f"❗ 파일을 읽는 중 오류 발생: {e}")
    st.stop()



st.write(df['재분석_감정'].value_counts())
# 중립 제외
filtered_df = df[df['감정'] != '중립']

# 감정 분포 데이터프레임 생성
sentiment_counts = (
    df['감정'].value_counts()
    .rename_axis('감정')
    .reset_index(name='리뷰 수')
)

# 감정 분포 시각화
st.subheader("📊 감정 분포 그래프")
fig, ax = plt.subplots()
colors = ['green' if label == '긍정' else 'red' if label == '부정' else 'gray' for label in sentiment_counts['감정']]
ax.bar(sentiment_counts['감정'], sentiment_counts['리뷰 수'], color=colors)
ax.set_xlabel("감정")
ax.set_ylabel("리뷰 수")
ax.set_title("긍정 / 부정 / 중립 감정 분포")
st.pyplot(fig)




if filtered_df.empty:
    st.warning("⚠️ 중립 이외의 리뷰가 없습니다.")
    st.stop()


col1, col2 = st.columns(2)

