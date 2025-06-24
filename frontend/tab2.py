import os
import requests
import streamlit as st


BASE_URL = os.getenv('BACKEND_URL', 'http://127.0.0.1:8000')

def movie_list_tab():
    st.subheader("📋 등록된 영화 목록")

    response = requests.get(f"{BASE_URL}/movies")
    movies = response.json() if response.status_code == 200 else []

    if not movies:
        st.warning("등록된 영화가 없습니다.")
        st.stop()
    else:
        movie_titles = [movie['title'] for movie in movies]
        selected_title = st.selectbox(label="조회할 영화를 선택하세요.", options=movie_titles, label_visibility="collapsed")

        selected_movie = next((m for m in movies if m["title"] == selected_title), None)
        st.text("")
        
        if selected_movie:
            # 영화 상세 정보
            st.markdown(f"### 🎞️ {selected_movie['title']}")
            st.write(f"**개봉일:** {selected_movie.get('release_date', '미정')}")
            st.write(f"**감독:** {selected_movie['director']}")
            st.write(f"**장르:** {selected_movie['category']}")
            if selected_movie.get("poster_url"):
                st.image(selected_movie["poster_url"], width=300)
            else:
                st.info("포스터 이미지 없음")

            # 영화 삭제 버튼
            if st.button("❌ 이 영화 삭제하기"):
                delete_res = requests.delete(f"{BASE_URL}/movies/{selected_title}")
                if delete_res.status_code == 200:
                    st.success("영화가 삭제되었습니다.")
                    st.rerun()
                else:
                    st.error("영화 삭제 실패")
            st.text("")
            
            # 리뷰 등록
            st.markdown("#### ✒️ 리뷰 작성 및 감정 분석")
            author = st.text_input("닉네임")
            review_content = st.text_area("리뷰 내용")

            if st.button("리뷰 등록 및 분석"):
                if author and review_content.strip():
                    review_data = {
                        "author": author,
                        "content": review_content
                    }
                    res = requests.post(f"{BASE_URL}/movies/{selected_title}/reviews", json=review_data)
                    if res.status_code == 200:
                        result = res.json()
                        st.success(f"감정 분석 결과: **{result['sentiment']}** (점수: {result['score']})")
                        st.rerun()
                    else:
                        st.error("리뷰 등록 또는 분석에 실패했습니다.")
                else:
                    st.warning("작성자와 리뷰 내용을 모두 입력해주세요.")

            st.text("")
            # 리뷰 목록 + 삭제 버튼
            st.markdown("#### 📢 최근 리뷰")
            res = requests.get(f"{BASE_URL}/movies/{selected_title}/reviews")
            if res.status_code == 200:
                reviews = res.json()
                if not reviews:
                    st.info("리뷰가 아직 없습니다.")
                else:
                    for r in reviews[::-1]:
                        col1, col2 = st.columns([9, 1])
                        with col1:
                            st.markdown(
                                f"▪️ {r['author']}: {r['content']} (감정: {r['sentiment']}, 점수: {r['score']})")
                        with col2:
                            if st.button("🗑️", key=f"delete_{r['id']}"):
                                del_res = requests.delete(
                                    f"{BASE_URL}/movies/{selected_title}/reviews/{r['id']}")
                                if del_res.status_code == 200:
                                    st.success("리뷰가 삭제되었습니다.")
                                    st.rerun()
                                else:
                                    st.error("리뷰 삭제 실패")
            else:
                st.error("리뷰를 불러오지 못했습니다.")

            # 평균 감성 점수
            avg_res = requests.get(f"{BASE_URL}/movies/{selected_title}/rating")
            if avg_res.status_code == 200:
                avg_data = avg_res.json()
                avg_score = avg_data.get("average_score")

                if avg_score is not None:
                    if avg_score >= 4:
                        emoji = "😍"
                    elif avg_score >= 3:
                        emoji = "🙂"
                    elif avg_score >= 2:
                        emoji = "😐"
                    elif avg_score >= 1:
                        emoji = "😕"
                    else:
                        emoji = "😡"

                    st.info(f"{emoji} 평균 감정 점수: **{avg_score}**")
