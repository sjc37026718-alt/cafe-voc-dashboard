import streamlit as st
import pandas as pd
import plotly.express as px
from shared_data import load_feedbacks

st.set_page_config(page_title="로스팅하우스 온도 | 대시보드", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Serif+KR:wght@400;700&display=swap');

    /* 배경 */
    .stApp, .block-container { background-color: #FFF9F3; }

    /* 전체 텍스트 브라운 통일 */
    .stApp * { color: #3E2723 !important; }

    /* 헤더만 흰색 유지 */
    .dash-header * { color: white !important; }
    .dash-header p { color: #D7CCC8 !important; }
    .dash-header {
        text-align: center;
        padding: 28px 20px;
        background: linear-gradient(160deg, #3E2723, #5D4037, #4E342E);
        border-radius: 20px;
        margin-bottom: 24px;
    }
    .dash-header h1 {
        font-family: 'Noto Serif KR', serif;
        font-size: 28px;
        margin: 0;
        letter-spacing: 2px;
    }

    /* 데이터프레임 */
    [data-testid="glideDataEditor"],
    [data-testid="glideDataEditor"] * {
        --gdg-bg-cell: #FFFDF9 !important;
        --gdg-bg-header: #F5F0EB !important;
        --gdg-bg-header-has-focus: #EDE7E3 !important;
        --gdg-text-dark: #3E2723 !important;
        --gdg-text-header: #5D4037 !important;
        --gdg-border-color: #D7CCC8 !important;
        --gdg-bg-cell-medium: #FFF8F0 !important;
        --gdg-bg-bubble: #F5F0EB !important;
        --gdg-text-medium: #5D4037 !important;
        --gdg-text-light: #8D6E63 !important;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="dash-header">
    <h1>☕ 로스팅하우스 온도 — VoC 대시보드</h1>
    <p>사장님, 지금 가장 급한 불만이 뭔지 한눈에 보세요</p>
</div>
""", unsafe_allow_html=True)

if st.button("🔄 새로고침"):
    st.cache_data.clear()

data = load_feedbacks()
df = pd.DataFrame(data)
df["날짜"] = pd.to_datetime(df["날짜"])

color_map = {"불만": "#F8A0A0", "요청": "#FADA7A", "칭찬": "#A0E4CB", "문의": "#B4B0F8"}

# 상단 지표
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("전체 피드백", f"{len(df)}건")
col2.metric("🔴 불만", f"{len(df[df['유형']=='불만'])}건")
col3.metric("🟡 요청", f"{len(df[df['유형']=='요청'])}건")
col4.metric("🟢 칭찬", f"{len(df[df['유형']=='칭찬'])}건")
col5.metric("🟣 문의", f"{len(df[df['유형']=='문의'])}건")

st.divider()

# 급한 불만 Top 3
st.markdown('<h3 style="color: #3E2723;">🚨 지금 가장 급한 불만 Top 3</h3>', unsafe_allow_html=True)
complaints = df[df["유형"] == "불만"].copy()
complaints["우선순위점수"] = complaints["별점"].apply(lambda x: x if pd.notna(x) else 2)
top3 = complaints.sort_values("우선순위점수").head(3)

for i, (_, row) in enumerate(top3.iterrows(), 1):
    star = f"⭐ {int(row['별점'])}" if pd.notna(row['별점']) else "별점 없음"
    st.error(f"**{i}위 | {row['경로']} | {star}**\n\n{row['내용']}")

st.divider()

# 인사이트 요약 3줄
st.markdown('<h3 style="color: #3E2723;">💡 이번 달 핵심 인사이트</h3>', unsafe_allow_html=True)
complaint_ratio = len(df[df["유형"]=="불만"]) / len(df) * 100
top_channel = complaints["경로"].value_counts().index[0]
top_channel_count = complaints["경로"].value_counts().values[0]

st.info(f"""
1. **불만 비율이 {complaint_ratio:.0f}%로 높습니다** — 전체 {len(df)}건 중 {len(complaints)}건이 불만. 즉각 대응이 필요합니다.
2. **'{top_channel}'에서 불만이 가장 많습니다** ({top_channel_count}건) — 이 채널의 고객 응대를 우선 점검하세요.
3. **결제/포인트 오류, 대기 시간, 주문 실수가 반복됩니다** — 운영 프로세스(POS·진동벨·주문 확인) 개선을 권장합니다.
""")

st.divider()

# 차트 영역
left, right = st.columns(2)

chart_layout = dict(
    margin=dict(t=20, b=20),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font_color="#3E2723",
)

with left:
    st.markdown('<h4 style="color: #3E2723;">유형별 분포</h4>', unsafe_allow_html=True)
    type_counts = df["유형"].value_counts().reset_index()
    type_counts.columns = ["유형", "건수"]
    fig1 = px.pie(type_counts, names="유형", values="건수", color="유형", color_discrete_map=color_map)
    fig1.update_layout(**chart_layout)
    fig1.update_traces(textfont_color="#3E2723")
    st.plotly_chart(fig1, use_container_width=True)

with right:
    st.markdown('<h4 style="color: #3E2723;">경로별 유형 분포</h4>', unsafe_allow_html=True)
    channel = df.groupby(["경로", "유형"]).size().reset_index(name="건수")
    fig2 = px.bar(channel, x="경로", y="건수", color="유형", color_discrete_map=color_map, barmode="stack")
    fig2.update_layout(**chart_layout)
    st.plotly_chart(fig2, use_container_width=True)

st.divider()

# 전체 피드백 테이블
st.markdown('<h3 style="color: #3E2723;">📋 전체 피드백 목록</h3>', unsafe_allow_html=True)

type_filter = st.multiselect("유형 필터", ["불만", "요청", "칭찬", "문의"], default=["불만", "요청", "칭찬", "문의"])
filtered = df[df["유형"].isin(type_filter)].sort_values("날짜", ascending=False)

st.dataframe(
    filtered[["날짜", "경로", "별점", "유형", "내용"]],
    column_config={
        "날짜": st.column_config.DateColumn("날짜", format="YYYY-MM-DD"),
        "별점": st.column_config.NumberColumn("별점", format="%d ⭐"),
        "유형": st.column_config.TextColumn("유형"),
    },
    use_container_width=True,
    hide_index=True,
)
