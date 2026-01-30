import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
from utils.firebase_handler import FirebaseHandler
from utils.auth import check_password, logout
from utils.ml_predictor import HealthPredictor

# ページ設定
st.set_page_config(
    page_title="YASU Health — 未来の健康管理",
    page_icon="favicon.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Awwwards級カスタムCSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=Inter:wght@300;400;600;700&family=Oswald:wght@500;700&display=swap');
    
    /* ===== グローバルリセット & ベース ===== */
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    :root {
        --deep-navy: #0F172A;
        --indigo: #818CF8;
        --emerald: #34D399;
        --glass-bg: rgba(255, 255, 255, 0.05);
        --glass-border: rgba(255, 255, 255, 0.1);
    }
    
    /* ===== Aurora背景 + Grainy Gradient ===== */
    .stApp {
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 50%, #0F172A 100%);
        position: relative;
        overflow-x: hidden;
    }
    
    .stApp::before {
        content: '';
        position: fixed;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: 
            radial-gradient(circle at 20% 30%, rgba(129, 140, 248, 0.15) 0%, transparent 50%),
            radial-gradient(circle at 80% 70%, rgba(52, 211, 153, 0.12) 0%, transparent 50%),
            radial-gradient(circle at 50% 50%, rgba(129, 140, 248, 0.08) 0%, transparent 70%);
        animation: aurora 20s ease-in-out infinite;
        pointer-events: none;
        z-index: 0;
    }
    
    .stApp::after {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 400 400' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)' opacity='0.03'/%3E%3C/svg%3E");
        pointer-events: none;
        z-index: 1;
    }
    
    @keyframes aurora {
        0%, 100% { transform: translate(0, 0) rotate(0deg); }
        33% { transform: translate(5%, -5%) rotate(5deg); }
        66% { transform: translate(-5%, 5%) rotate(-5deg); }
    }
    
    /* ===== コンテンツラッパー ===== */
    .main .block-container {
        position: relative;
        z-index: 2;
        padding: 3rem 2rem;
        max-width: 1400px;
        margin: 0 auto;
    }
    
    /* ===== ヒーローセクション ===== */
    .hero-section {
        text-align: center;
        margin-bottom: 4rem;
        animation: fadeInUp 1s ease-out;
    }
    
    .main-title {
        font-family: 'Playfair Display', serif;
        font-size: clamp(2.5rem, 5vw, 4.5rem);
        font-weight: 900;
        background: linear-gradient(135deg, #818CF8 0%, #34D399 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 1rem;
        letter-spacing: -0.02em;
        line-height: 1.1;
    }
    
    .subtitle {
        font-family: 'Inter', sans-serif;
        font-size: 1.1rem;
        font-weight: 300;
        color: rgba(255, 255, 255, 0.6);
        letter-spacing: 0.05em;
        text-transform: uppercase;
    }
    
    /* ===== Glassmorphism カード ===== */
    .glass-card {
        background: var(--glass-bg);
        backdrop-filter: blur(20px) saturate(180%);
        -webkit-backdrop-filter: blur(20px) saturate(180%);
        border: 1px solid var(--glass-border);
        border-radius: 24px;
        padding: 2.5rem;
        margin-bottom: 2rem;
        box-shadow: 
            0 8px 32px rgba(0, 0, 0, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        animation: fadeInUp 0.8s ease-out backwards;
    }
    
    .glass-card:hover {
        transform: translateY(-8px) scale(1.01);
        box-shadow: 
            0 20px 60px rgba(129, 140, 248, 0.2),
            inset 0 1px 0 rgba(255, 255, 255, 0.15);
        border-color: rgba(129, 140, 248, 0.3);
    }
    
    /* ===== ジム称号バッジ ===== */
    .gym-badge {
        background: linear-gradient(135deg, rgba(129, 140, 248, 0.2) 0%, rgba(52, 211, 153, 0.2) 100%);
        backdrop-filter: blur(20px);
        border: 2px solid rgba(129, 140, 248, 0.3);
        border-radius: 20px;
        padding: 2rem 3rem;
        text-align: center;
        margin-bottom: 3rem;
        position: relative;
        overflow: hidden;
        animation: fadeInUp 0.6s ease-out 0.2s backwards;
    }
    
    .gym-badge::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent, rgba(255, 255, 255, 0.05), transparent);
        animation: shimmer 3s infinite;
    }
    
    @keyframes shimmer {
        0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
        100% { transform: translateX(100%) translateY(100%) rotate(45deg); }
    }
    
    .gym-badge-title {
        font-family: 'Playfair Display', serif;
        font-size: 2.2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
        position: relative;
        z-index: 1;
    }
    
    .gym-badge-days {
        font-family: 'Oswald', sans-serif;
        font-size: 1.2rem;
        color: rgba(255, 255, 255, 0.7);
        letter-spacing: 0.1em;
        position: relative;
        z-index: 1;
    }
    
    /* ===== メトリクスカード ===== */
    .metric-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 3px;
        background: linear-gradient(90deg, var(--indigo), var(--emerald));
        transform: scaleX(0);
        transition: transform 0.3s ease;
    }
    
    .metric-card:hover {
        transform: scale(1.05);
        border-color: rgba(129, 140, 248, 0.3);
    }
    
    .metric-card:hover::before {
        transform: scaleX(1);
    }
    
    /* ===== Streamlit要素のオーバーライド ===== */
    .stMetric {
        background: transparent !important;
        padding: 0 !important;
    }
    
    .stMetric label {
        font-family: 'Inter', sans-serif !important;
        font-size: 0.85rem !important;
        font-weight: 600 !important;
        color: rgba(255, 255, 255, 0.5) !important;
        text-transform: uppercase !important;
        letter-spacing: 0.1em !important;
        margin-bottom: 0.5rem !important;
    }
    
    .stMetric [data-testid="stMetricValue"] {
        font-family: 'Oswald', sans-serif !important;
        font-size: 2.5rem !important;
        font-weight: 700 !important;
        color: #fff !important;
    }
    
    .stMetric [data-testid="stMetricDelta"] {
        font-family: 'Inter', sans-serif !important;
        font-size: 0.9rem !important;
    }
    
    /* ===== ボタンスタイル ===== */
    .stButton > button {
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        background: linear-gradient(135deg, var(--indigo) 0%, var(--emerald) 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-size: 1rem;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 15px rgba(129, 140, 248, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
        transition: left 0.5s;
    }
    
    .stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 8px 25px rgba(129, 140, 248, 0.5);
    }
    
    .stButton > button:hover::before {
        left: 100%;
    }
    
    .stButton > button:active {
        transform: scale(0.95);
    }
    
    /* ===== インプットフィールド ===== */
    .stNumberInput > div > div > input,
    .stDateInput > div > div > input,
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        color: white !important;
        font-family: 'Inter', sans-serif !important;
        padding: 0.75rem 1rem !important;
        transition: all 0.3s ease !important;
    }
    
    .stNumberInput > div > div > input:focus,
    .stDateInput > div > div > input:focus,
    .stTextInput > div > div > input:focus {
        border-color: var(--indigo) !important;
        box-shadow: 0 0 0 3px rgba(129, 140, 248, 0.2) !important;
        outline: none !important;
    }
    
    /* ===== チェックボックス ===== */
    .stCheckbox {
        color: rgba(255, 255, 255, 0.8) !important;
    }
    
    .stCheckbox > label {
        font-family: 'Inter', sans-serif !important;
        font-weight: 500 !important;
    }
    
    /* ===== セレクトボックス ===== */
    .stSelectbox > div > div {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
    }
    
    /* ===== エキスパンダー ===== */
    .streamlit-expanderHeader {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
        color: white !important;
        transition: all 0.3s ease !important;
    }
    
    .streamlit-expanderHeader:hover {
        background: rgba(255, 255, 255, 0.08) !important;
        border-color: var(--indigo) !important;
    }
    
    /* ===== サイドバー ===== */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(15, 23, 42, 0.95) 0%, rgba(30, 41, 59, 0.95) 100%) !important;
        backdrop-filter: blur(20px) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.1) !important;
    }
    
    [data-testid="stSidebar"] .stRadio > label {
        font-family: 'Inter', sans-serif !important;
        color: rgba(255, 255, 255, 0.9) !important;
        font-weight: 600 !important;
    }
    
    [data-testid="stSidebar"] .stRadio > div {
        gap: 0.5rem !important;
    }
    
    [data-testid="stSidebar"] .stRadio > div > label {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        padding: 1rem 1.5rem !important;
        transition: all 0.3s ease !important;
        font-family: 'Inter', sans-serif !important;
        color: rgba(255, 255, 255, 0.8) !important;
    }
    
    [data-testid="stSidebar"] .stRadio > div > label:hover {
        background: rgba(255, 255, 255, 0.1) !important;
        border-color: var(--indigo) !important;
        transform: translateX(5px) !important;
    }
    
    [data-testid="stSidebar"] .stRadio > div > label[data-baseweb="radio"] > div:first-child {
        background: linear-gradient(135deg, var(--indigo), var(--emerald)) !important;
    }
    
    /* ===== データテーブル ===== */
    .stDataFrame {
        background: rgba(255, 255, 255, 0.03) !important;
        border-radius: 16px !important;
        overflow: hidden !important;
    }
    
    .stDataFrame [data-testid="stDataFrameResizable"] {
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }
    
    /* ===== アラート ===== */
    .stAlert {
        background: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        color: white !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    /* ===== アニメーション ===== */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    /* ===== スクロールバー ===== */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.05);
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, var(--indigo), var(--emerald));
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #9CA3FF, #4AE4A8);
    }
    
    /* ===== レスポンシブ ===== */
    @media (max-width: 768px) {
        .main-title {
            font-size: 2rem;
        }
        
        .glass-card {
            padding: 1.5rem;
        }
        
        .gym-badge {
            padding: 1.5rem 2rem;
        }
        
        .gym-badge-title {
            font-size: 1.5rem;
        }
    }
    
    /* ===== Plotlyグラフのスタイル ===== */
    .js-plotly-plot {
        border-radius: 16px !important;
        overflow: hidden !important;
    }
    
    /* ===== セクションヘッダー ===== */
    .section-header {
        font-family: 'Playfair Display', serif;
        font-size: 2rem;
        font-weight: 700;
        color: white;
        margin-bottom: 1.5rem;
        position: relative;
        padding-left: 1.5rem;
    }
    
    .section-header::before {
        content: '';
        position: absolute;
        left: 0;
        top: 50%;
        transform: translateY(-50%);
        width: 4px;
        height: 80%;
        background: linear-gradient(180deg, var(--indigo), var(--emerald));
        border-radius: 2px;
    }
    
    /* ===== AIアドバイスカード ===== */
    .ai-advice-card {
        background: linear-gradient(135deg, rgba(129, 140, 248, 0.1) 0%, rgba(52, 211, 153, 0.1) 100%);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(129, 140, 248, 0.2);
        border-radius: 20px;
        padding: 2rem;
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
        animation: fadeInUp 0.8s ease-out 0.4s backwards;
    }
    
    .ai-advice-card::before {
        content: '🤖';
        position: absolute;
        top: -20px;
        right: -20px;
        font-size: 8rem;
        opacity: 0.05;
        animation: float 3s ease-in-out infinite;
    }
    
    /* ===== レシピカード ===== */
    .recipe-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        transition: all 0.3s ease;
    }
    
    .recipe-card:hover {
        background: rgba(255, 255, 255, 0.05);
        border-color: var(--emerald);
        transform: translateX(10px);
    }
    
    .recipe-title {
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        color: white;
        font-size: 1.1rem;
        margin-bottom: 0.5rem;
        text-decoration: none;
    }
    
    .recipe-title:hover {
        color: var(--emerald);
    }
    
    /* ===== 入力ページスタイル ===== */
    .input-section {
        animation: fadeInUp 0.6s ease-out;
    }
    
    .input-label {
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        color: rgba(255, 255, 255, 0.8);
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-bottom: 0.5rem;
    }
    
    /* ===== 設定ページスタイル ===== */
    .settings-section {
        animation: fadeInUp 0.6s ease-out;
    }
    
    .settings-group {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 2rem;
        margin-bottom: 2rem;
    }
    
    .settings-group-title {
        font-family: 'Playfair Display', serif;
        font-size: 1.5rem;
        font-weight: 700;
        color: white;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* ===== ローディングアニメーション ===== */
    .stSpinner > div {
        border-color: var(--indigo) transparent transparent transparent !important;
    }
    
    /* ===== 成功メッセージ ===== */
    .stSuccess {
        background: linear-gradient(135deg, rgba(52, 211, 153, 0.2) 0%, rgba(16, 185, 129, 0.2) 100%) !important;
        border-left: 4px solid var(--emerald) !important;
    }
    
    /* ===== 警告メッセージ ===== */
    .stWarning {
        background: linear-gradient(135deg, rgba(251, 191, 36, 0.2) 0%, rgba(245, 158, 11, 0.2) 100%) !important;
        border-left: 4px solid #FBBF24 !important;
    }
    
    /* ===== 情報メッセージ ===== */
    .stInfo {
        background: linear-gradient(135deg, rgba(129, 140, 248, 0.2) 0%, rgba(99, 102, 241, 0.2) 100%) !important;
        border-left: 4px solid var(--indigo) !important;
    }
    
    /* ===== エラーメッセージ ===== */
    .stError {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.2) 0%, rgba(220, 38, 38, 0.2) 100%) !important;
        border-left: 4px solid #EF4444 !important;
    }
</style>
""", unsafe_allow_html=True)

# ジムの称号を取得
def get_gym_title(consecutive_days):
    titles = {
        30: "ジム神",
        15: "ジム仙人",
        10: "ジム師範代",
        7: "ジムマスター",
        5: "ジムの常連さん",
        3: "ジム慣れ",
        2: "ジム初心者",
        1: "ジム練習生"
    }
    
    for days in sorted(titles.keys(), reverse=True):
        if consecutive_days >= days:
            return titles[days]
    return "ジム未経験者"

# 認証チェック
if not check_password():
    st.stop()

# Firebase初期化
@st.cache_resource
def init_firebase():
    return FirebaseHandler()

fb = init_firebase()

# メイン画面
def main_page():
    # ヒーローセクション
    st.markdown("""
    <div class="hero-section">
        <div class="main-title">YASU Health</div>
        <div class="subtitle">Future of Personal Wellness</div>
    </div>
    """, unsafe_allow_html=True)
    
    # データ読み込み
    weight_df = fb.get_weight_data()
    gym_df = fb.get_gym_data()
    calorie_df = fb.get_calorie_data()
    settings = fb.get_user_settings()
    
    # 連続日数と称号
    consecutive_days = fb.calculate_consecutive_gym_days()
    title = get_gym_title(consecutive_days)
    
    # ジム称号バッジ
    st.markdown(f"""
    <div class="gym-badge">
        <div class="gym-badge-title">🏆 {title}</div>
        <div class="gym-badge-days">連続 {consecutive_days} 日達成</div>
    </div>
    """, unsafe_allow_html=True)
    
    # AI提案
    if len(weight_df) >= 30:
        with st.expander("🤖 今日のAIアドバイス", expanded=True):
            st.markdown('<div class="ai-advice-card">', unsafe_allow_html=True)
            predictor = HealthPredictor(weight_df, gym_df, calorie_df)
            result = predictor.get_daily_advice()
            
            st.markdown(result['advice'])
            
            if result['recipes']:
                st.markdown("---")
                st.markdown(f"### 🍽️ おすすめレシピ ({result['recipes']['category']})")
                
                for recipe in result['recipes']['recipes']:
                    st.markdown(f"""
                    <div class="recipe-card">
                        <a href="{recipe['url']}" target="_blank" class="recipe-title">{recipe['title']}</a>
                        <p style="color: rgba(255,255,255,0.6); font-size: 0.9rem; margin: 0.5rem 0;">{recipe['snippet']}</p>
                        <p style="color: rgba(255,255,255,0.4); font-size: 0.8rem;">📍 {recipe['source']}</p>
                    </div>
                    """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        days_left = 30 - len(weight_df)
        st.info(f"📊 AIアドバイスまであと **{days_left}日** です。毎日記録を続けましょう!")
    
    # 期間選択
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        period = st.selectbox("表示期間", ["週", "月", "年"], key="period_select")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 期間に応じたデータフィルタリング
    today = datetime.now().date()
    if period == "週":
        start_date = today - timedelta(days=7)
    elif period == "月":
        start_date = today - timedelta(days=30)
    else:
        start_date = today - timedelta(days=365)
    
    filtered_weight = weight_df[weight_df['date'] >= pd.Timestamp(start_date)]
    filtered_gym = gym_df[gym_df['date'] >= pd.Timestamp(start_date)]
    filtered_calorie = calorie_df[calorie_df['date'] >= pd.Timestamp(start_date)]
    
    # メトリクス表示
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        if not filtered_weight.empty:
            current_weight = filtered_weight.iloc[-1]['weight']
            weight_change = current_weight - filtered_weight.iloc[0]['weight']
            st.metric("現在の体重", f"{current_weight:.1f} kg", f"{weight_change:+.1f} kg")
        else:
            st.metric("現在の体重", "-- kg")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        weight_goal = settings.get('weight_goal', 70.0)
        if not filtered_weight.empty:
            diff = current_weight - weight_goal
            st.metric("目標体重", f"{weight_goal:.1f} kg", f"{diff:+.1f} kg")
        else:
            st.metric("目標体重", f"{weight_goal:.1f} kg")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        gym_count = filtered_gym['went_to_gym'].sum() if not filtered_gym.empty else 0
        st.metric("ジム回数", f"{gym_count}回")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        avg_calories = filtered_calorie['calories'].mean() if not filtered_calorie.empty else 0
        calorie_goal = settings.get('calorie_goal', 2000)
        st.metric("平均消費カロリー", f"{avg_calories:.0f} kcal", f"目標: {calorie_goal} kcal")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # グラフ表示
    if not filtered_weight.empty:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<h2 class="section-header">📈 体重推移グラフ</h2>', unsafe_allow_html=True)
        
        fig = go.Figure()
        
        # 体重ライン
        fig.add_trace(go.Scatter(
            x=filtered_weight['date'],
            y=filtered_weight['weight'],
            mode='lines+markers',
            name='体重',
            line=dict(color='#818CF8', width=3),
            marker=dict(size=8, color='#818CF8', line=dict(color='#6366F1', width=2)),
            hovertemplate='<b>日付</b>: %{x|%Y-%m-%d}<br><b>体重</b>: %{y:.1f} kg<extra></extra>',
            fill='tozeroy',
            fillcolor='rgba(129, 140, 248, 0.1)'
        ))
        
        # 目標体重ライン
        fig.add_trace(go.Scatter(
            x=filtered_weight['date'],
            y=[weight_goal] * len(filtered_weight),
            mode='lines',
            name='目標体重',
            line=dict(color='#34D399', width=2, dash='dash'),
            hovertemplate='<b>目標</b>: %{y:.1f} kg<extra></extra>'
        ))
        
        # ジムに行った日をマーク
        if not filtered_gym.empty:
            gym_dates = filtered_gym[filtered_gym['went_to_gym'] == True]['date']
            gym_weights = []
            
            for date in gym_dates:
                weight_on_date = filtered_weight[filtered_weight['date'] == date]
                if not weight_on_date.empty:
                    gym_weights.append(weight_on_date.iloc[0]['weight'])
                else:
                    gym_weights.append(None)
            
            fig.add_trace(go.Scatter(
                x=gym_dates,
                y=gym_weights,
                mode='markers',
                name='ジム',
                marker=dict(
                    size=18,
                    color='#34D399',
                    symbol='star',
                    line=dict(color='#10B981', width=2)
                ),
                hovertemplate='<b>ジムに行った日</b><br>%{x|%Y-%m-%d}<extra></extra>'
            ))
        
        fig.update_layout(
            title=None,
            xaxis_title="日付",
            yaxis_title="体重 (kg)",
            hovermode="x unified",
            height=500,
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                bgcolor='rgba(255, 255, 255, 0.05)',
                bordercolor='rgba(255, 255, 255, 0.1)',
                borderwidth=1,
                font=dict(color='white', family='Inter')
            ),
            plot_bgcolor='rgba(0, 0, 0, 0)',
            paper_bgcolor='rgba(0, 0, 0, 0)',
            font=dict(color='white', family='Inter'),
            xaxis=dict(
                gridcolor='rgba(255, 255, 255, 0.1)',
                showgrid=True,
                zeroline=False
            ),
            yaxis=dict(
                gridcolor='rgba(255, 255, 255, 0.1)',
                showgrid=True,
                zeroline=False
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # データテーブル
        with st.expander("📊 詳細データを表示"):
            st.markdown('<div class="glass-card" style="margin-top: 1rem;">', unsafe_allow_html=True)
            merged_data = filtered_weight.copy()
            merged_data['date_str'] = merged_data['date'].dt.strftime('%Y-%m-%d')
            
            if not filtered_gym.empty:
                gym_dict = dict(zip(
                    filtered_gym['date'].dt.strftime('%Y-%m-%d'),
                    filtered_gym['went_to_gym']
                ))
                merged_data['ジム'] = merged_data['date_str'].map(gym_dict).fillna(False)
                merged_data['ジム'] = merged_data['ジム'].map({True: '✅', False: '❌'})
            else:
                merged_data['ジム'] = '❌'
            
            if not filtered_calorie.empty:
                calorie_dict = dict(zip(
                    filtered_calorie['date'].dt.strftime('%Y-%m-%d'),
                    filtered_calorie['calories']
                ))
                merged_data['消費カロリー'] = merged_data['date_str'].map(calorie_dict).fillna(0)
            else:
                merged_data['消費カロリー'] = 0
            
            display_df = merged_data[['date_str', 'weight', 'ジム', '消費カロリー']].copy()
            display_df.columns = ['日付', '体重 (kg)', 'ジム', '消費カロリー (kcal)']
            display_df = display_df.sort_values('日付', ascending=False)
            
            st.dataframe(display_df, use_container_width=True, hide_index=True)
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.info("📝 データがまだありません。データ入力画面から記録を始めましょう!")
        st.markdown('</div>', unsafe_allow_html=True)

# データ入力画面
def input_page():
    st.markdown("""
    <div class="hero-section">
        <div class="main-title">📝 データ入力</div>
        <div class="subtitle">Daily Health Recording</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="glass-card input-section">', unsafe_allow_html=True)
    
    today = datetime.now().date()
    selected_date = st.date_input(
        "日付",
        value=today,
        max_value=today,
        min_value=datetime(2026, 1, 1).date()
    )
    
    # 今日以外は編集不可
    if selected_date != today:
        st.warning("⚠️ 過去の日付は編集できません(翌0時以降)")
        st.info("💡 今日のデータのみ入力・編集が可能です")
        st.markdown('</div>', unsafe_allow_html=True)
        return
    
    # 既存データの読み込み
    weight_df = fb.get_weight_data()
    gym_df = fb.get_gym_data()
    calorie_df = fb.get_calorie_data()
    
    # 今日のデータがあれば表示
    today_weight = weight_df[weight_df['date'] == pd.Timestamp(today)]
    today_gym = gym_df[gym_df['date'] == pd.Timestamp(today)]
    today_calorie = calorie_df[calorie_df['date'] == pd.Timestamp(today)]
    
    default_weight = today_weight.iloc[0]['weight'] if not today_weight.empty else 0.0
    default_gym = today_gym.iloc[0]['went_to_gym'] if not today_gym.empty else False
    default_calorie = int(today_calorie.iloc[0]['calories']) if not today_calorie.empty else 0
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="input-label">体重 (kg)</div>', unsafe_allow_html=True)
        weight = st.number_input(
            "体重 (kg)",
            min_value=0.0,
            max_value=300.0,
            value=float(default_weight),
            step=0.1,
            help="今日の体重を入力してください",
            label_visibility="collapsed"
        )
    
    with col2:
        st.markdown('<div class="input-label">ジム</div>', unsafe_allow_html=True)
        went_to_gym = st.checkbox(
            "ジムに行った",
            value=default_gym,
            help="今日ジムに行った場合はチェック"
        )
    
    st.markdown('<div class="input-label">消費カロリー (kcal)</div>', unsafe_allow_html=True)
    calories = st.number_input(
        "消費カロリー (kcal)",
        min_value=0,
        max_value=10000,
        value=default_calorie,
        step=50,
        help="今日の総消費カロリーを入力",
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col2:
        if st.button("💾 保存", type="primary", use_container_width=True):
            if weight > 0:
                try:
                    fb.save_weight(today, weight)
                    fb.save_gym_record(today, went_to_gym)
                    fb.save_calorie_record(today, calories)
                    st.success("✅ データを保存しました!")
                    st.balloons()
                except Exception as e:
                    st.error(f"❌ エラーが発生しました: {str(e)}")
            else:
                st.warning("⚠️ 体重を入力してください")
    
    st.markdown('</div>', unsafe_allow_html=True)

# 設定画面
def settings_page():
    st.markdown("""
    <div class="hero-section">
        <div class="main-title">⚙️ 設定</div>
        <div class="subtitle">Personalize Your Experience</div>
    </div>
    """, unsafe_allow_html=True)
    
    settings = fb.get_user_settings()
    
    st.markdown('<div class="glass-card settings-section">', unsafe_allow_html=True)
    
    st.markdown('<div class="settings-group">', unsafe_allow_html=True)
    st.markdown('<div class="settings-group-title">🎯 目標設定</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="input-label">目標体重 (kg)</div>', unsafe_allow_html=True)
        weight_goal = st.number_input(
            "目標体重 (kg)",
            min_value=0.0,
            max_value=300.0,
            value=float(settings.get('weight_goal', 70.0)),
            step=0.1,
            label_visibility="collapsed"
        )
    
    with col2:
        st.markdown('<div class="input-label">目標消費カロリー (kcal)</div>', unsafe_allow_html=True)
        calorie_goal = st.number_input(
            "目標消費カロリー (kcal)",
            min_value=0,
            max_value=10000,
            value=int(settings.get('calorie_goal', 2000)),
            step=100,
            label_visibility="collapsed"
        )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="settings-group">', unsafe_allow_html=True)
    st.markdown('<div class="settings-group-title">🔐 パスワード変更</div>', unsafe_allow_html=True)
    
    new_password = st.text_input(
        "新しいパスワード",
        type="password",
        help="パスワードを変更する場合は入力してください"
    )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col2:
        if st.button("💾 設定を保存", type="primary", use_container_width=True):
            try:
                new_settings = {
                    'weight_goal': weight_goal,
                    'calorie_goal': calorie_goal,
                    'password': new_password if new_password else settings.get('password', 'yasu0122')
                }
                fb.update_user_settings(new_settings)
                st.success("✅ 設定を保存しました!")
            except Exception as e:
                st.error(f"❌ エラーが発生しました: {str(e)}")
    
    st.markdown('</div>', unsafe_allow_html=True)

# メイン処理
def main():
    # サイドバーでページ選択
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 2rem 0;">
            <div style="font-family: 'Playfair Display', serif; font-size: 1.8rem; font-weight: 700; 
                        background: linear-gradient(135deg, #818CF8, #34D399); 
                        -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                YASU Health
            <div style="font-family: 'Inter', sans-serif; font-size: 0.8rem; color: rgba(255,255,255,0.5); 
                        letter-spacing: 0.1em; margin-top: 0.5rem;">
                WELLNESS DASHBOARD
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div style="margin: 2rem 0;">', unsafe_allow_html=True)
        page = st.radio(
            "ページを選択",
            ["メイン画面", "データ入力", "設定"],
            label_visibility="collapsed"
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        if st.button("🚪 ログアウト", use_container_width=True):
            logout()
        
        st.markdown("""
        <div style="position: absolute; bottom: 2rem; left: 0; right: 0; text-align: center;">
            <div style="font-family: 'Inter', sans-serif; font-size: 0.7rem; color: rgba(255,255,255,0.3);">
                © 2026 YASU Health<br>Powered by AI
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    if page == "メイン画面":
        main_page()
    elif page == "データ入力":
        input_page()
    elif page == "設定":
        settings_page()

if __name__ == "__main__":
    main()

            

