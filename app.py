import streamlit as st
import pandas as pd
import time



st.title("통합데이터 서비스")
st.image('image.jpg')
data = pd.read_csv("members.csv")
data["PW"] = data["PW"].astype(str)

with st.form("login_form"):
    ID = st.text_input("ID", placeholder="아이디를 입력하세요")
    PW = st.text_input("Password", type="password", placeholder="비밀번호를 입력하세요")
    submit_button = st.form_submit_button("로그인")

if submit_button:
    if not ID or not PW:
        st.warning("ID와 비밀번호를 모두 입력해주세요.")
    else:
        # 사용자 확인
        user = data[(data["ID"] == ID) & (data["PW"] == str(PW))]
        
        if not user.empty:
            st.success(f"{ID}님 환영합니다!")
            st.session_state["ID"]=ID
            
            progress_text = "로그인 중입니다."
            my_bar = st.progress(0, text=progress_text)
            for percent_complete in range(100):
                time.sleep(0.01)
                my_bar.progress(percent_complete + 1, text=progress_text)
            time.sleep(1)
            my_bar.empty()
            st.switch_page("pages/bike.py")
            
            
        else:
            st.error("아이디 또는 비밀번호가 일치하지 않습니다.")

# 데이터 로드 함수 추가
def load_bike_data():
    # 여기서 실제 데이터를 CSV 파일에서 로드하거나 임시 데이터를 사용할 수 있습니다.
    # 예시 데이터를 포함합니다.
    data = pd.DataFrame({
        "위도": [37.5665, 37.5678, 37.5654],
        "경도": [126.9780, 126.9795, 126.9767],
        "대여소명": ["대여소1", "대여소2", "대여소3"],
        "대여횟수": [120, 200, 150],
    })
    return data

def bike_usage_graph():
    data = load_bike_data()  # 데이터 로드
    st.write("### 속성별 공공자전거 데이터 분석")
    attribute = st.selectbox("분석할 속성을 선택하세요", ["대여횟수"])
    
    if attribute == "대여횟수":
        fig, ax = plt.subplots()
        ax.bar(data["대여소명"], data["대여횟수"], color='blue')
        ax.set_title("대여소별 대여횟수")
        ax.set_xlabel("대여소명")
        ax.set_ylabel("대여횟수")
        st.pyplot(fig)

def bike_location_map():
    data = load_bike_data()  # 데이터 로드
    st.write("### 공공자전거 대여소 위치")
    st.map(data[["위도", "경도"]])