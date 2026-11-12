import streamlit as st

classcode = "1234"
code = st.text_input("강의 코드를 입력하세요")

# 비어 있으면 안내, 1234이면 "환영합니다", 그 외에는 "코드가 일치하지 않습니다"
if code == "":
    st.warning("코드를 입력하세요")
elif code == classcode:
    st.success("환영합니다")
else:
    st.error("코드가 일치하지 않습니다")




st.subheader("다양한 인풋")

# 객관식(라디오버튼, 체크박스), 주관식(숫자만 입력, 텍스트 입력), 슬라이더, 파일업로드

# a가 답임!
answer = st.radio("일차방정식 2x+1=15를 풀어보세요.", ["5", "6", "7", "8"])
if answer == "7":
    st.success("정답입니다")
elif answer == "8":
    st.error("이항을 잘못 한 것 같아요")
else:    
    st.warning("오답입니다")

agree = st.checkbox("동의합니다.")
if agree == True:
    st.success("동의하셨습니다.")
else:
    st.error("동의하지 않으셨습니다.")

answer2 = st.text_input("일차함수를 입력하세요", placeholder="y=2x+1")
answer3 = st.number_input("숫자를 입력하세요", 
min_value=0, 
max_value=100, 
step=2,
value=50)

st.write(answer3*2+1)


if st.button("확인"):
    st.success("확인되었습니다.")


# 라디오버튼 문제에 대한 정답 제출하기 버튼 -> 피드백
answer = st.radio("일차방정식 2x+1=13를 풀어보세요.", ["5", "6", "7", "8"])
if st. button("정답 제출하기"):
    if answer == "7":
        st.success("정답입니다")
    elif answer == "8":
        st.error("이항을 잘못 한 것 같아요")
    else:    
        st.warning("오답입니다")



answer4 = st.slider("나이를 선택해주세요", min_value=0, max_value=100, value=20, step=1)
if answer4 > 30:
    st.success("30세 이상입니다.")
else:
    st.warning("30세 미만입니다.")


