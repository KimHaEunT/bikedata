import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


data = pd.read_csv("학생현황.csv")

if "ID" not in st.session_state:
    st.session_state["ID"] = "None"

ID = st.session_state["ID"]

with st.sidebar:
    st.caption(f'{ID}님 접속중')
    
with st.form("input"):
    region = st.multiselect("지역", data['Region'].unique())
    gender = st.multiselect("성별", data['Gender'].unique())
    school = st.multiselect("학교", data['School'].unique())
    submitted = st.form_submit_button("조회")
    
    if submitted:
        name_list = []
        result = data["Year"].drop_duplicates().sort_values().reset_index(drop=True)
        for re in region:
            for ge in gender:
                for sc in school:
                    name = f"{re}_{ge}_{sc}"
                    name_list.append(name)
                    selected_df = data[(data['Region'] == re) & (data['Gender'] == ge)& (data['School'] == sc)]
                    selected_df = selected_df[["Year","Students"]].rename(columns={"Students": name})
                    result = pd.merge(result, selected_df, on='Year').sort_values('Year')
        
        st.line_chart(data=result, x='Year', y=name_list,use_container_width=True)
        
# 학생현황 데이터 로드 함수
def load_school_data():
    # 임시 데이터 예시
    data = pd.DataFrame({
        "위도": [37.5641, 37.5635, 37.5628],
        "경도": [126.9752, 126.9745, 126.9738],
        "학교명": ["학교1", "학교2", "학교3"],
        "학생수": [300, 450, 500],
    })
    return data

def school_population_graph():
    data = load_school_data()
    st.write("### 속성별 학생현황 데이터 분석")
    attribute = st.selectbox("분석할 속성을 선택하세요", ["학생수"])
    
    if attribute == "학생수":
        fig, ax = plt.subplots()
        ax.bar(data["학교명"], data["학생수"], color='green')
        ax.set_title("학교별 학생 수")
        ax.set_xlabel("학교명")
        ax.set_ylabel("학생 수")
        st.pyplot(fig)

def school_location_map():
    data = load_school_data()
    st.write("### 학교 위치 지도")
    st.map(data[["위도", "경도"]])