import streamlit as st
from tab1 import movie_add_tab
from tab2 import movie_list_tab


st.set_page_config(page_title="영화 리뷰 서비스", page_icon="🎬", layout="centered")
st.title("🎬 영화 리뷰 서비스")

tab1, tab2 = st.tabs(["➕ 영화 추가", "📋 등록된 영화 목록"])

with tab1:
    movie_add_tab()

with tab2:
    movie_list_tab()