import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np

# 페이지 설정
st.set_page_config(
    layout="wide",
    page_title="KEIT R&D 트렌드 대시보드",
    page_icon="📊"
)

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
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
        }
        .metric-card {
            background: white;
            padding: 1.5rem;
            border-radius: 1rem;
            box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
            transition: all 0.3s ease;
        }
        .metric-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 12px -1px rgb(0 0 0 / 0.2);
        }
        .stPlotlyChart {
            background: white;
            border-radius: 1rem;
            padding: 1rem;
            box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
        }
        .css-1d391kg {
            padding: 2rem 1rem;
        }
        .stMarkdown {
            font-size: 1.1rem;
        }
    </style>
""", unsafe_allow_html=True)

# 타이틀 섹션
st.markdown("""
    <div style='text-align: center; padding: 2rem 0;'>
        <h1 style='color: #1e40af; font-size: 2.5rem;'>KEIT R&D 트렌드 대시보드</h1>
        <p style='color: #6b7280; font-size: 1.2rem;'>산업기술 혁신을 위한 실시간 모니터링 시스템</p>
    </div>
""", unsafe_allow_html=True)

# 사이드바 스타일링
with st.sidebar:
    st.markdown("""
        <div style='text-align: center; padding: 1rem 0;'>
            <h2 style='color: #1e40af;'>분야 선택</h2>
        </div>
    """, unsafe_allow_html=True)
    
    fields = {
        "소재부품장비": "🔧",
        "수송기기": "🚗",
        "바이오헬스": "🧬"
    }
    selected_field = st.selectbox(
        "",
        list(fields.keys()),
        format_func=lambda x: f"{fields[x]} {x}"
    )

# 샘플 데이터 생성 함수 확장
@st.cache_data
def load_data():
    # 기술 성숙도 데이터
    tech_maturity = pd.DataFrame({
        'name': ['2020', '2021', '2022', '2023', '2024'],
        '소재': [65, 70, 75, 80, 85],
        '부품': [60, 65, 70, 75, 80],
        '장비': [55, 60, 65, 70, 75],
        'TRL': [4, 5, 6, 7, 8]
    })
    
    # 투자 현황 데이터
    investment = pd.DataFrame({
        'category': ['자동차', '항공', '조선', '철도'],
        'value': [40, 25, 20, 15],
        'growth': [12.3, 8.7, -2.1, 5.4]
    })
    
    # 연구 성과 데이터
    dates = pd.date_range(start='2020-01-01', end='2024-12-31', freq='M')
    research_output = pd.DataFrame({
        'date': dates,
        'value': [60 + i + np.sin(i/6)*10 for i in range(len(dates))],
        'papers': np.random.randint(10, 50, size=len(dates)),
        'patents': np.random.randint(5, 30, size=len(dates))
    })
    
    return tech_maturity, investment, research_output

tech_maturity, investment, research_output = load_data()

# 소재부품장비 대시보드
def show_materials_dashboard():
    # 헤더 섹션
    st.markdown("""
        <div style='background: linear-gradient(to right, #3b82f6, #1e40af); 
                    padding: 1.5rem; border-radius: 1rem; margin-bottom: 2rem;
                    color: white;'>
            <h2 style='margin: 0;'>소재부품장비 R&D 현황</h2>
            <p style='margin: 0.5rem 0 0 0; opacity: 0.9;'>
                첨단소재, 핵심부품, 제조장비 분야의 기술혁신 트렌드
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # 주요 지표
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(
            label="특허 출원",
            value="1,256건",
            delta="156건",
            delta_color="normal"
        )
    with col2:
        st.metric(
            label="기술 이전",
            value="89건",
            delta="-5건",
            delta_color="inverse"
        )
    with col3:
        st.metric(
            label="참여 기업",
            value="342개",
            delta="28개",
            delta_color="normal"
        )
    with col4:
        st.metric(
            label="평균 TRL",
            value="6.8",
            delta="0.5",
            delta_color="normal"
        )
    
    # 기술 성숙도 매트릭스
    st.markdown("### 📈 기술 성숙도 매트릭스")
    
    tab1, tab2 = st.tabs(["스택 차트", "트렌드 분석"])
    
    with tab1:
        fig = go.Figure()
        colors = ['#3b82f6', '#60a5fa', '#93c5fd']
        for i, column in enumerate(['소재', '부품', '장비']):
            fig.add_trace(go.Bar(
                name=column,
                x=tech_maturity['name'],
                y=tech_maturity[column],
                marker_color=colors[i]
            ))
        fig.update_layout(
            barmode='stack',
            plot_bgcolor='white',
            paper_bgcolor='white',
            title='연도별 기술 성숙도 변화',
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=tech_maturity['name'],
            y=tech_maturity['TRL'],
            mode='lines+markers',
            name='TRL',
            line=dict(color='#3b82f6', width=3),
            marker=dict(size=10)
        ))
        fig.update_layout(
            title='기술준비수준(TRL) 추이',
            plot_bgcolor='white',
            paper_bgcolor='white'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # 하단 분석 섹션
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🎯 핵심 성과 지표")
        
        # 게이지 차트
        fig = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = 420,
            domain = {'x': [0, 1], 'y': [0, 1]},
            delta = {'reference': 380},
            title = {'text': "연간 특허 출원 건수"},
            gauge = {
                'axis': {'range': [None, 500]},
                'bar': {'color': "#3b82f6"},
                'steps': [
                    {'range': [0, 250], 'color': '#dbeafe'},
                    {'range': [250, 400], 'color': '#bfdbfe'}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 450
                }
            }
        ))
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 📊 투자 효율성 분석")
        
        # 버블 차트
        investment_efficiency = pd.DataFrame({
            '분야': ['소재', '부품', '장비'],
            '투자금액': [450, 380, 290],
            '성과건수': [85, 72, 58],
            '성장률': [12, 8, 15]
        })
        
        fig = px.scatter(
            investment_efficiency,
            x='투자금액',
            y='성과건수',
            size='성장률',
            color='분야',
            size_max=30,
            title='투자 대비 성과 분석'
        )
        fig.update_layout(plot_bgcolor='white')
        st.plotly_chart(fig, use_container_width=True)

# 수송기기 대시보드
def show_transport_dashboard():
    # 헤더 섹션
    st.markdown("""
        <div style='background: linear-gradient(to right, #ef4444, #b91c1c); 
                    padding: 1.5rem; border-radius: 1rem; margin-bottom: 2rem;
                    color: white;'>
            <h2 style='margin: 0;'>수송기기 R&D 현황</h2>
            <p style='margin: 0.5rem 0 0 0; opacity: 0.9;'>
                자동차, 항공, 조선, 철도 분야의 기술혁신 현황
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # 투자 현황 분석
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 🚗 분야별 R&D 투자 현황")
        
        # 향상된 파이 차트
        fig = go.Figure(data=[go.Pie(
            labels=investment['category'],
            values=investment['value'],
            hole=.3,
            marker=dict(colors=['#ef4444', '#f87171', '#fca5a5', '#fecaca'])
        )])
        fig.update_layout(
            title='R&D 투자 비중',
            annotations=[dict(text='총 투자액', x=0.5, y=0.5, font_size=20, showarrow=False)]
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 📈 투자 증감률")
        
        # 증감률 막대 차트
        fig = go.Figure(data=[
            go.Bar(
                x=investment['growth'],
                y=investment['category'],
                orientation='h',
                marker=dict(
                    color=['#ef4444' if x > 0 else '#991b1b' for x in investment['growth']]
                )
            )
        ])
        fig.update_layout(
            title='전년 대비 증감률 (%)',
            xaxis_title='증감률 (%)',
            plot_bgcolor='white'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # 프로젝트 진행 현황
    st.markdown("### 🎯 프로젝트 진행 현황")
    
    progress_data = {
        "기획단계": {"progress": 80, "projects": 12},
        "연구개발": {"progress": 60, "projects": 28},
        "실증단계": {"progress": 40, "projects": 15},
        "상용화": {"progress": 20, "projects": 5}
    }
    
    cols = st.columns(len(progress_data))
    for col, (phase, data) in zip(cols, progress_data.items()):
        with col:
            st.markdown(f"""
                <div style='text-align: center; padding: 1rem;
                           background: white; border-radius: 0.5rem;
                           box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
                    <h4 style='margin: 0; color: #991b1b;'>{phase}</h4>
                    <p style='font-size: 2rem; margin: 0.5rem 0;'>{data['projects']}건</p>
                    <div style='margin-top: 0.5rem;'>
                        진행률: {data['progress']}%
                    </div>
                </div>
            """, unsafe_allow_html=True)
    
    # 진행 상황 타임라인
    st.progress(0.6)
    st.caption("전체 프로젝트 진행률: 60%")

# 바이오헬스 대시보드
def show_biohealth_dashboard():
   # 헤더 섹션
   st.markdown("""
       <div style='background: linear-gradient(to right, #059669, #047857); 
                   padding: 1.5rem; border-radius: 1rem; margin-bottom: 2rem;
                   color: white;'>
           <h2 style='margin: 0;'>바이오헬스 R&D 현황</h2>
           <p style='margin: 0.5rem 0 0 0; opacity: 0.9;'>
               의료기기, 제약, 바이오 분야의 연구개발 현황
           </p>
       </div>
   """, unsafe_allow_html=True)

   # 임상 단계별 현황
   st.markdown("### 🧬 연구 단계별 진행 현황")
   
   clinical_phases = {
       "기초연구": {"count": 45, "success_rate": 85},
       "임상 1상": {"count": 32, "success_rate": 70},
       "임상 2상": {"count": 18, "success_rate": 55},
       "임상 3상": {"count": 8, "success_rate": 40},
       "승인": {"count": 3, "success_rate": 100}
   }
   
   cols = st.columns(len(clinical_phases))
   for col, (phase, data) in zip(cols, clinical_phases.items()):
       with col:
           st.markdown(f"""
               <div style='text-align: center; padding: 1rem;
                          background: white; border-radius: 0.5rem;
                          box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
                   <h4 style='margin: 0; color: #059669;'>{phase}</h4>
                   <p style='font-size: 2rem; margin: 0.5rem 0;'>{data['count']}</p>
                   <div style='margin-top: 0.5rem;'>
                       성공률: {data['success_rate']}%
                   </div>
               </div>
           """, unsafe_allow_html=True)

   # 연구 성과 트렌드
   st.markdown("### 📈 연구 성과 트렌드")
   
   tab1, tab2 = st.tabs(["논문 실적", "특허 출원"])
   
   with tab1:
       fig = go.Figure()
       fig.add_trace(go.Scatter(
           x=research_output['date'],
           y=research_output['papers'],
           mode='lines',
           name='논문 수',
           line=dict(color='#059669', width=3),
           fill='tozeroy'
       ))
       fig.update_layout(
           title='월별 논문 발표 실적',
           plot_bgcolor='white',
           paper_bgcolor='white',
           xaxis_title='날짜',
           yaxis_title='논문 수'
       )
       st.plotly_chart(fig, use_container_width=True)
   
   with tab2:
       fig = go.Figure()
       fig.add_trace(go.Bar(
           x=research_output['date'],
           y=research_output['patents'],
           marker_color='#059669',
           name='특허 수'
       ))
       fig.update_layout(
           title='월별 특허 출원 현황',
           plot_bgcolor='white',
           paper_bgcolor='white',
           xaxis_title='날짜',
           yaxis_title='특허 출원 수'
       )
       st.plotly_chart(fig, use_container_width=True)

   # 투자 효율성 분석
   col1, col2 = st.columns(2)
   
   with col1:
       st.markdown("### 💰 연구비 집행 현황")
       
       # 도넛 차트로 연구비 집행 비율 표시
       expenditure_data = {
           '인건비': 40,
           '재료비': 25,
           '장비비': 20,
           '기타': 15
       }
       
       fig = go.Figure(data=[go.Pie(
           labels=list(expenditure_data.keys()),
           values=list(expenditure_data.values()),
           hole=.6,
           marker=dict(colors=['#059669', '#34d399', '#6ee7b7', '#a7f3d0'])
       )])
       fig.update_layout(
           title='연구비 항목별 비중',
           annotations=[dict(text='총 집행액', x=0.5, y=0.5, font_size=20, showarrow=False)]
       )
       st.plotly_chart(fig, use_container_width=True)
   
   with col2:
       st.markdown("### 🎯 목표 달성률")
       
       # 게이지 차트로 목표 달성률 표시
       fig = go.Figure(go.Indicator(
           mode = "gauge+number+delta",
           value = 75,
           domain = {'x': [0, 1], 'y': [0, 1]},
           delta = {'reference': 50},
           title = {'text': "전체 목표 달성률"},
           gauge = {
               'axis': {'range': [None, 100]},
               'bar': {'color': "#059669"},
               'steps': [
                   {'range': [0, 50], 'color': '#d1fae5'},
                   {'range': [50, 75], 'color': '#a7f3d0'}
               ],
               'threshold': {
                   'line': {'color': "red", 'width': 4},
                   'thickness': 0.75,
                   'value': 80
               }
           }
       ))
       st.plotly_chart(fig, use_container_width=True)

# 선택된 분야에 따라 대시보드 표시
if selected_field == "소재부품장비":
   show_materials_dashboard()
elif selected_field == "수송기기":
   show_transport_dashboard()
else:
   show_biohealth_dashboard()

# 사이드바 추가 정보
with st.sidebar:
   st.markdown("---")
   st.markdown("### 📊 데이터 현황")
   st.info(f"마지막 업데이트: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
   
   # 데이터 신뢰도 표시
   st.markdown("### 🎯 데이터 신뢰도")
   st.progress(0.95)
   st.caption("95% 신뢰도")
   
   # 필터 옵션
   st.markdown("### 🔍 필터 옵션")
   year_range = st.slider("연도 범위", 2020, 2024, (2020, 2024))
   
   # 도움말
   with st.expander("ℹ️ 도움말"):
       st.markdown("""
           - 좌측 상단의 분야를 선택하여 각 분야별 상세 현황을 확인할 수 있습니다.
           - 그래프는 마우스 오버시 상세 정보를 제공합니다.
           - 데이터는 실시간으로 업데이트됩니다.
       """)
