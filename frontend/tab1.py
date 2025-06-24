import os
import requests
import streamlit as st


BASE_URL = os.getenv('BACKEND_URL', 'http://127.0.0.1:8000')

def movie_add_tab():
    st.subheader("➕ 영화 추가")

    with st.form(key="movie_form"):
        title = st.text_input("영화 제목")
        release_date = st.text_input("개봉일 (YYYY-MM-DD)")
        director = st.text_input("감독")
        category = st.text_input("장르")
        poster_url = st.text_input("포스터 이미지 URL (선택)")
        
        if poster_url and not poster_url.startswith(("http://", "https://")):
            poster_url = None

        submit = st.form_submit_button("등록하기")

    if submit:
        new_movie = {
            "title": title,
            "release_date": release_date,
            "director": director,
            "category": category,
            "poster_url": poster_url
        }
        response = requests.post(f"{BASE_URL}/movies", json=new_movie)
        if response.status_code == 200:
            st.success("영화가 등록되었습니다.")
            st.rerun()
        else:
            st.error("영화 등록을 실패했습니다.")
