import streamlit as st

st.title("10주차 스트림릿 연습")

st.info("안녕하세요. 소개페이지")
st.error("빨간 박스 에러창")
st.success("초록 박스 성공창")
st.warning("노란 박스 경고창")

st.header("메인페이지")
st.subheader("그다음 중제목")
st.write("모든 내용 다 쓰기 가능")
st.markdown("이것은 **텍스트** 쓰기")
st.latex("ax^2+bx+c=0")
st.write("codecogs에서 수식 가져올 수 있음")
st.code("print('hello teachers')")
st.write("---")

st.image("image1.jpg", width=300)
st.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSv8Cxao-PXuLM9YnEcLYSS33KWxki0c5i5fVOi-jFFfw&s=10", width=300)
#st.video("")

st.write("https://www.desmos.com/matrix?lang=ko")
st.link_button("데스모스 행렬 계산기 바로가기", "https://www.desmos.com/matrix?lang=ko")
st.components.v1.iframe("https://www.desmos.com/matrix?lang=ko", height=500)