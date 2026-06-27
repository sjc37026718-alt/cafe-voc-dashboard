import streamlit as st
import requests
from datetime import date, datetime
from shared_data import load_feedbacks, add_feedback

st.set_page_config(page_title="로스팅하우스 온도 | 성수", layout="centered")

# 사이드바 햄버거 아이콘 변경
st.markdown("""
<style>
    button[data-testid="stSidebarCollapseButton"] svg {
        display: none;
    }
    button[data-testid="stSidebarCollapseButton"]::before {
        content: "☰";
        font-size: 24px;
        color: #3E2723;
    }
    section[data-testid="stSidebar"] {
        background-color: #FFF9F3;
    }
</style>
""", unsafe_allow_html=True)

# 사이드바 메뉴
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding: 16px 0;">
        <span style="font-size: 32px;">☕</span>
        <div style="font-family: 'Noto Serif KR', serif; font-size: 18px; color: #3E2723; margin-top: 4px;">로스팅하우스 온도</div>
        <div style="font-size: 12px; color: #A1887F;">MENU</div>
    </div>
    """, unsafe_allow_html=True)
    st.divider()

    with st.expander("☕ 커피", expanded=False):
        st.markdown("""
| 메뉴 | 가격 |
|------|------|
| 아메리카노 (HOT/ICE) | 4,500원 |
| 에스프레소 | 3,500원 |
| 콜드브루 | 5,000원 |
| 콜드브루 라떼 | 5,500원 |
| 더치커피 | 5,500원 |
""")

    with st.expander("🥛 라떼", expanded=False):
        st.markdown("""
| 메뉴 | 가격 |
|------|------|
| 카페라떼 | 5,000원 |
| 바닐라라떼 | 5,500원 |
| 카라멜라떼 | 5,500원 |
| 말차라떼 | 5,500원 |
| 흑임자라떼 | 6,000원 |
""")

    with st.expander("🍰 디저트", expanded=False):
        st.markdown("""
| 메뉴 | 가격 |
|------|------|
| 시그니처 케이크 | 6,500원 |
| 티라미수 | 7,000원 |
| 크루아상 | 4,500원 |
| 마들렌 세트 (3개) | 5,000원 |
| 스콘 & 클로티드크림 | 5,500원 |
""")

    with st.expander("🌿 비건", expanded=False):
        st.markdown("""
| 메뉴 | 가격 |
|------|------|
| 오트밀크 라떼 | 5,500원 |
| 아몬드밀크 카푸치노 | 5,500원 |
| 비건 당근 케이크 | 6,500원 |
| 비건 블루베리 머핀 | 5,000원 |
| 과일 그래놀라 볼 | 6,000원 |
""")

    with st.expander("🐶 펫", expanded=False):
        st.markdown("""
| 메뉴 | 가격 |
|------|------|
| 강아지 우유 (무유당) | 3,000원 |
| 펫 쿠키 세트 (3개) | 4,000원 |
| 강아지 생일 케이크 | 12,000원 |
| 펫 아이스크림 | 3,500원 |
""")

    st.divider()
    st.markdown("##### 매장 정보")
    st.markdown("📍 서울 성수동 연무장길 43 2층")
    st.markdown("📞 02-1234-5678")
    st.markdown(r"⏰ 평일 08:00 ~ 22:00 / 주말 10:00 ~ 21:00")
    st.divider()

    st.markdown("##### 🔒 사장님 전용")
    owner_pw = st.text_input("비밀번호", type="password", placeholder="비밀번호를 입력하세요")
    if owner_pw == "1234":
        st.success("인증 완료!")
        st.markdown("[📊 VoC 대시보드 열기](https://cafe-voc-dashboard-hb9atextc7ta3ffxzxp7uj.streamlit.app/)", unsafe_allow_html=True)
    elif owner_pw:
        st.error("비밀번호가 틀립니다.")

# 날씨 API (Open-Meteo, 무료/키 불필요)
@st.cache_data(ttl=1800)
def get_weather():
    try:
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": 37.5445,
            "longitude": 127.0567,
            "current": "temperature_2m,weather_code",
            "timezone": "Asia/Seoul",
        }
        res = requests.get(url, params=params, timeout=5)
        data = res.json()["current"]
        temp = data["temperature_2m"]
        code = data["weather_code"]
        if code <= 1:
            icon, desc = "☀️", "맑음"
        elif code <= 3:
            icon, desc = "⛅", "구름 조금"
        elif code <= 48:
            icon, desc = "☁️", "흐림"
        elif code <= 67:
            icon, desc = "🌧️", "비"
        elif code <= 77:
            icon, desc = "❄️", "눈"
        else:
            icon, desc = "⛈️", "폭우"
        return f"{icon} {temp}°C {desc}"
    except Exception:
        return "☀️ 날씨 정보를 불러오는 중..."

weather = get_weather()
today = datetime.now().strftime("%m월 %d일 %A")

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Serif+KR:wght@400;700&display=swap');

    .stApp {{
        background-color: #FFF9F3;
    }}
    .block-container {{
        background-color: #FFF9F3;
    }}
    .weather-bar {{
        text-align: center;
        padding: 10px;
        background: linear-gradient(90deg, #F5F0EB, #FFF8F0, #F5F0EB);
        border-radius: 12px;
        margin-bottom: 16px;
        font-size: 14px;
        color: #78716C;
        letter-spacing: 0.5px;
    }}
    .hero-section {{
        text-align: center;
        padding: 48px 20px 28px 20px;
        background: linear-gradient(160deg, #3E2723, #5D4037, #4E342E);
        border-radius: 24px;
        margin-bottom: 24px;
        color: white;
        position: relative;
        overflow: hidden;
    }}
    .hero-section::before {{
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        background: radial-gradient(circle at 30% 40%, rgba(255,183,77,0.15) 0%, transparent 60%),
                    radial-gradient(circle at 70% 60%, rgba(188,143,95,0.1) 0%, transparent 50%);
    }}
    .hero-section * {{ position: relative; z-index: 1; }}
    .hero-section h1 {{
        font-family: 'Noto Serif KR', serif;
        font-size: 36px;
        margin-bottom: 4px;
        letter-spacing: 2px;
    }}
    .hero-section .sub {{
        font-size: 15px;
        color: #D7CCC8;
        margin-bottom: 16px;
        font-style: italic;
    }}
    .hero-section .hours {{
        font-size: 13px;
        color: #BCAAA4;
        margin-top: 12px;
    }}
    .info-chip {{
        display: inline-block;
        background: rgba(255,255,255,0.12);
        backdrop-filter: blur(4px);
        color: #EFEBE9;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 12px;
        margin: 4px;
        border: 1px solid rgba(255,255,255,0.08);
    }}
    .steam {{
        font-size: 48px;
        margin-bottom: 8px;
        animation: float 3s ease-in-out infinite;
    }}
    @keyframes float {{
        0%, 100% {{ transform: translateY(0); }}
        50% {{ transform: translateY(-6px); }}
    }}
    .stat-box {{
        text-align: center;
        padding: 16px;
        background: linear-gradient(135deg, #FFF8E1, #FFF3E0);
        border-radius: 16px;
        border: 1px solid #FFE0B2;
    }}
    .stat-num {{ font-size: 24px; font-weight: bold; color: #BF360C; }}
    .stat-label {{ font-size: 12px; color: #8D6E63; margin-top: 2px; }}
    .section-title {{
        font-family: 'Noto Serif KR', serif;
        font-size: 22px;
        color: #3E2723;
        margin-bottom: 4px;
    }}
    .review-card {{
        background: #FFFDF9;
        border-radius: 16px;
        padding: 20px 24px;
        margin-bottom: 12px;
        border-left: 4px solid #A1887F;
        box-shadow: 0 2px 12px rgba(62,39,35,0.06);
    }}
    .review-stars {{ font-size: 16px; margin-bottom: 4px; }}
    .review-content {{
        font-size: 15px;
        color: #3E2723;
        line-height: 1.7;
        margin-bottom: 6px;
    }}
    .review-meta {{ font-size: 12px; color: #A1887F; }}
    .form-section {{
        background: linear-gradient(135deg, #EFEBE9, #FFF8F0);
        padding: 28px;
        border-radius: 20px;
        border: 1px solid #D7CCC8;
    }}
    .footer {{
        text-align: center;
        padding: 24px;
        color: #A1887F;
        font-size: 13px;
        font-family: 'Noto Serif KR', serif;
    }}
</style>
""", unsafe_allow_html=True)

# 날씨 바
st.markdown(f'<div class="weather-bar">📍 성수동 오늘 · {today} · {weather} — 커피 한 잔 어떠세요?</div>', unsafe_allow_html=True)

# 히어로
st.markdown("""
<div class="hero-section">
    <div class="steam">☕</div>
    <h1>로스팅하우스 온도</h1>
    <p class="sub">한 잔의 커피에 온기를 담다</p>
    <div>
        <span class="info-chip">📍 서울 성수동 연무장길 43 2층</span>
        <span class="info-chip">🐶 반려동물 동반</span>
        <span class="info-chip">🔌 콘센트 다수</span>
        <span class="info-chip">🌿 비건 디저트</span>
    </div>
    <p class="hours">⏰ 평일 08:00 ~ 22:00 · 주말 10:00 ~ 21:00 · 매주 월요일 휴무</p>
</div>
""", unsafe_allow_html=True)

# 통계
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown('<div class="stat-box"><div class="stat-num">⭐ 4.8</div><div class="stat-label">평균 별점</div></div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="stat-box"><div class="stat-num">1,200+</div><div class="stat-label">누적 리뷰</div></div>', unsafe_allow_html=True)
with col3:
    st.markdown('<div class="stat-box"><div class="stat-num">96%</div><div class="stat-label">재방문 의사</div></div>', unsafe_allow_html=True)

st.markdown("")

# 리뷰
st.markdown('<div class="section-title">💬 고객 리뷰</div>', unsafe_allow_html=True)
st.caption("실제 고객님들이 남겨주신 생생한 후기")

all_data = load_feedbacks()
reviews = [d for d in all_data if d.get("유형") == "칭찬" or (d.get("별점") and d["별점"] >= 4)]
reviews = sorted(reviews, key=lambda x: x["날짜"], reverse=True)

for r in reviews:
    star_val = r.get("별점")
    stars = "⭐" * int(star_val) if star_val else "💬"
    st.markdown(f"""
<div class="review-card">
    <div class="review-stars">{stars}</div>
    <div class="review-content">"{r["내용"]}"</div>
    <div class="review-meta">{r["날짜"]} · {r["경로"]}</div>
</div>
""", unsafe_allow_html=True)

st.markdown("")

# 리뷰 입력
st.markdown("""
<style>
    div[data-testid="stForm"] {
        background: #FFFFFF;
        border: 2px solid #D7CCC8;
        border-radius: 20px;
        padding: 32px;
        box-shadow: 0 4px 16px rgba(62,39,35,0.08);
    }
</style>
""", unsafe_allow_html=True)

with st.form("feedback_form", clear_on_submit=True):
    st.markdown("""
    <div style="text-align: center; margin-bottom: 16px;">
        <span style="font-size: 36px;">✍️</span>
        <div style="font-family: 'Noto Serif KR', serif; font-size: 22px; color: #3E2723; margin-top: 4px;">리뷰 남기기</div>
        <div style="font-size: 14px; color: #A1887F;">소중한 의견을 남겨주세요. 더 나은 카페가 되겠습니다.</div>
    </div>
    """, unsafe_allow_html=True)

    form_top = st.columns([1, 1])
    with form_top[0]:
        input_date = st.date_input("📅 방문 날짜", value=date.today())
    with form_top[1]:
        input_channel = st.selectbox("📍 작성 경로", ["선택해주세요", "앱리뷰", "설문", "전화메모", "인스타DM"])

    input_star = st.select_slider(
        "⭐ 별점을 선택해주세요",
        options=[1, 2, 3, 4, 5],
        value=5,
        format_func=lambda x: "★" * x + "☆" * (5 - x) + f"  ({x}점)",
    )

    input_content = st.text_area("💬 리뷰 내용", height=100, placeholder="카페에서의 경험을 자유롭게 작성해주세요...")

    st.markdown("""
    <div style="text-align: center; font-size: 14px; color: #8D6E63; margin-bottom: 4px;">
        📸 방문 인증 사진 <span style="color: #EF4444;">(필수)</span>
    </div>
    <div style="text-align: center; font-size: 12px; color: #A1887F; margin-bottom: 8px;">
        매장에서 촬영한 음료, 영수증, 매장 사진을 올려주세요
    </div>
    """, unsafe_allow_html=True)
    uploaded_photo = st.file_uploader("사진 업로드", type=["jpg", "jpeg", "png"], label_visibility="collapsed")

    if uploaded_photo:
        st.image(uploaded_photo, caption="📸 인증 사진 미리보기", use_container_width=True)

    submitted = st.form_submit_button("리뷰 등록하기", use_container_width=True, type="primary")

    if submitted:
        missing = []
        if not input_date:
            missing.append("방문 날짜")
        if input_channel == "선택해주세요":
            missing.append("작성 경로")
        if not input_content.strip():
            missing.append("리뷰 내용")
        if not uploaded_photo:
            missing.append("방문 인증 사진")

        if missing:
            st.warning(f"⚠️ 다음 항목을 입력해주세요: **{', '.join(missing)}**")
        else:
            keywords_complaint = ["불만", "오류", "느려", "오래", "잘못", "안 돼", "안돼", "불편", "식었", "끊겨", "달아", "좁아", "부담", "환불"]
            keywords_request = ["있으면", "좋겠", "해주세요", "가능한가", "되나요", "해주셔"]
            keywords_inquiry = ["어떻게", "몇 시", "되나요", "찾으러", "할인"]
            content_lower = input_content
            if any(k in content_lower for k in keywords_complaint) or input_star <= 2:
                유형 = "불만"
            elif any(k in content_lower for k in keywords_request):
                유형 = "요청"
            elif any(k in content_lower for k in keywords_inquiry):
                유형 = "문의"
            else:
                유형 = "칭찬"
            add_feedback(input_date, input_channel, input_star, input_content, 유형)
            st.success("✅ 리뷰가 등록되었습니다! 감사합니다 ☕")
            st.balloons()

st.markdown('<div class="footer">© 2026 로스팅하우스 온도 · 성수<br>Brewed with ♥ and good beans</div>', unsafe_allow_html=True)
