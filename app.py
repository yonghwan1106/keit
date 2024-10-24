import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# 페이지 설정
st.set_page_config(layout="wide", page_title="KEIT R&D 트렌드 대시보드")

# CSS 스타일 적용
st.markdown("""
    <style>
        .main {
            padding: 2rem;
        }
        .stButton>button {
            background: linear-gradient(to right, #3b82f6, #8b5cf6);
            color: white;
            border: none;
            padding: 0.5rem 1rem;
            border-radius: 0.5rem;
        }
        .metric-card {
            background: white;
            padding: 1rem;
            border-radius: 0.5rem;
            box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
        }
    </style>
""", unsafe_allow_html=True)

# 타이틀
st.title("KEIT R&D 트렌드 대시보드")

# 분야 선택
fields = ["소재부품장비", "수송기기", "바이오헬스"]
selected_field = st.sidebar.selectbox("분야 선택", fields)

# 샘플 데이터 생성
@st.cache_data
def load_data():
    # 기술 성숙도 데이터
    tech_maturity = pd.DataFrame({
        'name': ['2020', '2021', '2022', '2023', '2024'],
        '소재': [65, 70, 75, 80, 85],
        '부품': [60, 65, 70, 75, 80],
        '장비': [55, 60, 65, 70, 75]
    })
    
    # 투자 현황 데이터
    investment = pd.DataFrame({
        'category': ['자동차', '항공', '조선', '철도'],
        'value': [40, 25, 20, 15]
    })
    
    # 연구 성과 데이터
    research_output = pd.DataFrame({
        'date': pd.date_range(start='2020-01-01', end='2024-12-31', freq='M'),
        'value': range(60, 120)
    })
    
    return tech_maturity, investment, research_output

tech_maturity, investment, research_output = load_data()

# 소재부품장비 대시보드
def show_materials_dashboard():
    # 메트릭스 표시
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="특허 출원", value="1,256건", delta="156건")
    with col2:
        st.metric(label="기술 이전", value="89건", delta="-5건")
    with col3:
        st.metric(label="참여 기업", value="342개", delta="28개")
    
    # 기술 성숙도 차트
    st.subheader("소재부품 기술 성숙도 매트릭스")
    fig = go.Figure()
    for column in ['소재', '부품', '장비']:
        fig.add_trace(go.Bar(
            name=column,
            x=tech_maturity['name'],
            y=tech_maturity[column],
        ))
    fig.update_layout(barmode='stack')
    st.plotly_chart(fig, use_container_width=True)

# 수송기기 대시보드
def show_transport_dashboard():
    # 투자 현황 파이 차트
    st.subheader("기술별 R&D 투자 현황")
    fig = px.pie(investment, values='value', names='category')
    st.plotly_chart(fig, use_container_width=True)
    
    # 프로젝트 진행 현황
    st.subheader("진행 과제 현황")
    progress_data = {
        "기획단계": 80,
        "연구개발": 60,
        "실증단계": 40,
        "상용화": 20
    }
    for phase, progress in progress_data.items():
        st.progress(progress/100)
        st.write(f"{phase}: {progress}%")

# 바이오헬스 대시보드
def show_biohealth_dashboard():
    # 연구 단계 타임라인
    st.subheader("연구 단계별 진행 현황")
    phases = ["기초연구", "임상 1상", "임상 2상", "임상 3상", "승인"]
    timeline = go.Figure(data=[go.Scatter(
        x=list(range(len(phases))),
        y=[1]*len(phases),
        mode='markers+text',
        text=phases,
        textposition="bottom center"
    )])
    timeline.update_layout(showlegend=False)
    st.plotly_chart(timeline, use_container_width=True)
    
    # 연구 성과 차트
    st.subheader("분야별 연구 성과")
    fig = px.area(research_output, x='date', y='value')
    st.plotly_chart(fig, use_container_width=True)

# 선택된 분야에 따라 대시보드 표시
if selected_field == "소재부품장비":
    show_materials_dashboard()
elif selected_field == "수송기기":
    show_transport_dashboard()
else:
    show_biohealth_dashboard()

# 데이터 업데이트 시간
st.sidebar.markdown(f"마지막 업데이트: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
