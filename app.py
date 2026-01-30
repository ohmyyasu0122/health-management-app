import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

# utilsディレクトリから実際のモジュールをインポート
from utils.firebase_handler import FirebaseHandler
from utils.auth import check_password, logout
from utils.ml_predictor import HealthPredictor

# ページ設定
st.set_page_config(
    page_title="MANA Health Matrix",
    page_icon="🧬", # ファビコンもサイバーパンク風に
    layout="wide",
    initial_sidebar_state="expanded"
)

# カスタムCSSとGoogle Fontsの読み込み
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Roboto+Mono:wght@400;700&display=swap" rel="stylesheet">
    <style>
        /* Global Styles */
        :root {
            --bg-dark: #0A0A0A;
            --text-light: #E0E0E0;
            --accent-cyan: #00FFFF;
            --accent-magenta: #FF00FF;
            --accent-green: #00FF00;
            --border-glow: rgba(0, 255, 255, 0.5);
            --button-hover: rgba(0, 255, 255, 0.2);
            --card-bg: #1A1A1A;
            --card-border: #333333;
        }

        body {
            font-family: 'Roboto Mono', monospace;
            background-color: var(--bg-dark);
            color: var(--text-light);
            margin: 0;
            padding: 0;
            font-size: 16px;
            line-height: 1.6;
        }

        /* Streamlit specific overrides */
        .stApp {
            background-color: var(--bg-dark);
            color: var(--text-light);
            font-family: 'Roboto Mono', monospace;
        }

        /* Sidebar */
        [data-testid="stSidebar"] {
            background-color: #111;
            padding: 20px;
            box-shadow: 2px 0 10px rgba(0, 255, 255, 0.3);
            border-right: 1px solid var(--accent-cyan);
        }

        /* Streamlitのタイトル要素をターゲット */
        [data-testid="stSidebar"] .st-emotion-cache-vk32gh { /* Sidebar title */
            font-family: 'Orbitron', sans-serif;
            font-size: 1.8rem;
            color: var(--accent-green);
            text-align: center;
            margin-bottom: 30px;
            text-shadow: 0 0 8px var(--accent-green);
        }

        /* Streamlitのナビゲーションリンクをターゲット */
        [data-testid="stSidebarNav"] ul {
            list-style: none;
            padding: 0;
            margin: 0;
        }

        [data-testid="stSidebarNav"] li {
            margin-bottom: 15px;
        }

        [data-testid="stSidebarNav"] a {
            display: block;
            padding: 12px 15px;
            color: var(--text-light);
            text-decoration: none;
            border: 1px solid transparent;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
            font-family: 'Roboto Mono', monospace;
        }

        [data-testid="stSidebarNav"] a::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, var(--accent-cyan), transparent);
            transition: all 0.5s ease;
            opacity: 0.3;
        }

        [data-testid="stSidebarNav"] a:hover {
            color: var(--accent-cyan);
            border-color: var(--accent-cyan);
            box-shadow: 0 0 10px var(--accent-cyan);
            transform: translateX(5px);
        }

        [data-testid="stSidebarNav"] a:hover::before {
            left: 100%;
        }

        /* Streamlitの選択中のナビゲーションリンクをターゲット */
        [data-testid="stSidebarNav"] a.st-emotion-cache-10trblm.st-emotion-cache-10trblm.st-emotion-cache-10trblm.st-emotion-cache-10trblm { /* Active link */
            color: var(--accent-cyan);
            border-color: var(--accent-cyan);
            box-shadow: 0 0 15px var(--accent-cyan);
            background-color: rgba(0, 255, 255, 0.1);
        }
        
        /* Logout button in sidebar */
        [data-testid="stSidebar"] .stButton > button {
            background-color: #333;
            color: var(--text-light);
            border: 1px solid var(--accent-magenta);
            padding: 10px 15px;
            text-align: center;
            cursor: pointer;
            font-family: 'Roboto Mono', monospace;
            font-size: 1rem;
            transition: all 0.3s ease;
            margin-top: 30px;
            box-shadow: 0 0 5px var(--accent-magenta);
            width: 100%;
        }

        [data-testid="stSidebar"] .stButton > button:hover {
            background-color: var(--accent-magenta);
            color: var(--bg-dark);
            box-shadow: 0 0 15px var(--accent-magenta);
        }

        /* Utility Classes */
        .neon-text {
            color: var(--accent-cyan);
            text-shadow: 0 0 5px var(--accent-cyan), 0 0 10px var(--accent-cyan);
        }

        .glitch {
            animation: glitch-effect 2s infinite alternate;
        }

        @keyframes glitch-effect {
            0% { text-shadow: 0 0 5px var(--accent-cyan); }
            20% { text-shadow: 2px 2px 0 var(--accent-magenta), -2px -2px 0 var(--accent-green); }
            40% { text-shadow: -2px 2px 0 var(--accent-cyan), 2px -2px 0 var(--accent-magenta); }
            60% { text-shadow: 0 0 5px var(--accent-green); }
            80% { text-shadow: 2px -2px 0 var(--accent-magenta), -2px 2px 0 var(--accent-cyan); }
            100% { text-shadow: 0 0 5px var(--accent-cyan); }
        }

        /* Header */
        .app-header {
            text-align: center;
            margin-bottom: 40px;
        }

        .app-title {
            font-family: 'Orbitron', sans-serif;
            font-size: 3.5rem;
            color: var(--accent-cyan);
            text-shadow: 0 0 15px var(--accent-cyan), 0 0 25px rgba(0, 255, 255, 0.7);
            margin: 0;
            letter-spacing: 2px;
        }

        .app-subtitle {
            font-size: 1.2rem;
            color: var(--text-light);
            margin-top: 10px;
            opacity: 0.7;
        }

        /* Gym Title */
        .gym-status-card {
            background-color: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: 8px;
            padding: 20px;
            text-align: center;
            box-shadow: 0 0 15px rgba(0, 255, 0, 0.3);
            margin-bottom: 30px;
        }

        .gym-title-cyber {
            font-family: 'Orbitron', sans-serif;
            font-size: 2rem;
            color: var(--accent-green);
            text-shadow: 0 0 10px var(--accent-green);
            margin: 0;
        }

        .gym-consecutive-days {
            font-size: 1.2rem;
            color: var(--text-light);
            opacity: 0.8;
            margin-top: 10px;
        }

        /* AI Advice */
        .ai-advice-section {
            background-color: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: 8px;
            padding: 25px;
            box-shadow: 0 0 15px rgba(255, 0, 255, 0.3);
        }

        .ai-advice-header {
            font-family: 'Orbitron', sans-serif;
            font-size: 1.5rem;
            color: var(--accent-magenta);
            text-shadow: 0 0 8px var(--accent-magenta);
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .ai-advice-content {
            font-size: 1.1rem;
            margin-bottom: 20px;
        }

        .recipe-section {
            border-top: 1px dashed var(--card-border);
            padding-top: 20px;
        }

        .recipe-header {
            font-family: 'Orbitron', sans-serif;
            font-size: 1.3rem;
            color: var(--accent-cyan);
            text-shadow: 0 0 5px var(--accent-cyan);
            margin-bottom: 15px;
        }

        .recipe-item {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            padding: 10px 0;
            border-bottom: 1px dotted #333;
        }

        .recipe-item:last-child {
            border-bottom: none;
        }

        .recipe-title a {
            color: var(--accent-cyan);
            text-decoration: none;
            font-weight: bold;
            font-size: 1.1rem;
        }

        .recipe-title a:hover {
            text-decoration: underline;
            text-shadow: 0 0 5px var(--accent-cyan);
        }

        .recipe-snippet {
            font-size: 0.9rem;
            color: #AAA;
            margin-top: 5px;
        }

        .recipe-source {
            font-size: 0.8rem;
            color: #888;
            white-space: nowrap;
        }

        .info-message-custom { /* Renamed to avoid conflict with st.info */
            background-color: rgba(0, 255, 255, 0.1);
            border: 1px solid var(--accent-cyan);
            padding: 15px;
            border-radius: 5px;
            text-align: center;
            font-size: 1.1rem;
            color: var(--accent-cyan);
            box-shadow: 0 0 10px rgba(0, 255, 255, 0.5);
        }

        /* Period Selection */
        .period-selection-container {
            display: flex;
            justify-content: flex-end;
            margin-bottom: 20px;
        }

        .custom-select-wrapper {
            position: relative;
            display: inline-block;
            width: 150px;
        }

        /* Streamlitのselectboxをターゲット */
        .stSelectbox [data-testid="stSelectbox"] > div > div {
            width: 100%;
            padding: 10px 15px;
            background-color: var(--card-bg);
            color: var(--text-light);
            border: 1px solid var(--accent-cyan);
            border-radius: 5px;
            appearance: none; /* Remove default arrow */
            -webkit-appearance: none;
            -moz-appearance: none;
            font-family: 'Roboto Mono', monospace;
            font-size: 1rem;
            cursor: pointer;
            box-shadow: 0 0 5px rgba(0, 255, 255, 0.3);
        }

        .stSelectbox [data-testid="stSelectbox"] > div > div:focus {
            outline: none;
            border-color: var(--accent-magenta);
            box-shadow: 0 0 10px var(--accent-magenta);
        }
        /* Streamlitのselectboxのドロップダウン矢印をカスタム */
        .stSelectbox [data-testid="stSelectbox"] > div > div::after {
            content: '▼';
            position: absolute;
            top: 50%;
            right: 10px;
            transform: translateY(-50%);
            color: var(--accent-cyan);
            pointer-events: none;
        }


        /* Metrics Display */
        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }

        .metric-card-wrapper {
            background-color: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: 8px;
            padding: 20px;
            text-align: center;
            box-shadow: 0 0 10px rgba(0, 255, 255, 0.2);
            position: relative;
            overflow: hidden;
        }

        .metric-card-wrapper::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(0,255,255,0.1) 0%, transparent 70%);
            animation: rotate-glow 10s linear infinite;
            opacity: 0.3;
        }

        @keyframes rotate-glow {
            from { transform: rotate(0deg); }
            to { transform: rotate(360deg); }
        }

        .metric-label-custom {
            font-size: 1rem;
            color: #AAA;
            margin-bottom: 10px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        .metric-value-custom {
            font-family: 'Orbitron', sans-serif;
            font-size: 2.5rem;
            font-weight: bold;
            color: var(--accent-cyan);
            text-shadow: 0 0 10px var(--accent-cyan);
            margin-bottom: 5px;
        }

        .metric-change-custom, .metric-goal-custom {
            font-size: 0.9rem;
            color: var(--text-light);
            opacity: 0.7;
        }

        .metric-change-custom.positive { color: var(--accent-green); }
        .metric-change-custom.negative { color: var(--accent-magenta); }

        /* Graph Display */
        .graph-container {
            background-color: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 0 15px rgba(0, 255, 255, 0.3);
            min-height: 400px; /* Placeholder height */
            position: relative;
            overflow: hidden;
        }

        .graph-title-custom {
            font-family: 'Orbitron', sans-serif;
            font-size: 1.8rem;
            color: var(--accent-cyan);
            text-shadow: 0 0 8px var(--accent-cyan);
            text-align: center;
            margin-bottom: 20px;
        }

        /* Data Table */
        .data-table-section {
            background-color: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 0 15px rgba(0, 255, 0, 0.3);
        }

        /* Streamlit expander headerをターゲット */
        [data-testid="stExpander"] .st-emotion-cache-p5m90l { /* Expander header */
            font-family: 'Orbitron', sans-serif;
            font-size: 1.5rem;
            color: var(--accent-green);
            text-shadow: 0 0 8px var(--accent-green);
            margin-bottom: 0;
            padding: 0; /* Remove default padding */
        }
        [data-testid="stExpander"] .st-emotion-cache-p5m90l:hover {
            color: var(--accent-cyan);
            text-shadow: 0 0 8px var(--accent-cyan);
        }
        [data-testid="stExpander"] .st-emotion-cache-1m6g9o3 { /* Expander content area */
            padding: 0; /* Remove default padding */
        }

        /* Streamlit Dataframe styling */
        [data-testid="stDataFrame"] {
            border: 1px solid #444;
            border-radius: 5px;
        }
        [data-testid="stDataFrame"] table {
            width: 100%;
            border-collapse: collapse;
            font-size: 0.95rem;
        }
        [data-testid="stDataFrame"] th, [data-testid="stDataFrame"] td {
            padding: 12px 15px;
            text-align: left;
            border-bottom: 1px solid #222;
        }
        [data-testid="stDataFrame"] th {
            background-color: #2A2A2A;
            color: var(--accent-cyan);
            font-family: 'Orbitron', sans-serif;
            text-transform: uppercase;
            letter-spacing: 1px;
            position: sticky;
            top: 0;
            z-index: 1;
        }
        [data-testid="stDataFrame"] tr:nth-child(even) {
            background-color: #1F1F1F;
        }
        [data-testid="stDataFrame"] tr:hover {
            background-color: #282828;
            box-shadow: inset 0 0 5px rgba(0, 255, 255, 0.2);
        }
        /* 特定の列のテキストアラインメントを調整 */
        [data-testid="stDataFrame"] .col-ジム {
            text-align: center;
        }

        /* Input/Settings Page elements */
        .page-title-custom {
            font-family: 'Orbitron', sans-serif;
            font-size: 2.5rem;
            color: var(--accent-magenta);
            text-shadow: 0 0 10px var(--accent-magenta);
            margin-bottom: 30px;
            text-align: center;
        }

        .form-group-label {
            display: block;
            font-size: 1.1rem;
            color: var(--accent-cyan);
            margin-bottom: 8px;
            text-shadow: 0 0 3px rgba(0, 255, 255, 0.5);
            font-family: 'Roboto Mono', monospace;
        }

        /* Streamlit input widgets */
        .stNumberInput input, .stTextInput input, .stDateInput input {
            background-color: #1A1A1A;
            border: 1px solid var(--accent-cyan);
            border-radius: 5px;
            color: var(--text-light);
            font-family: 'Roboto Mono', monospace;
            font-size: 1rem;
            box-shadow: 0 0 5px rgba(0, 255, 255, 0.3);
            transition: all 0.3s ease;
        }
        .stNumberInput input:focus, .stTextInput input:focus, .stDateInput input:focus {
            outline: none;
            border-color: var(--accent-magenta);
            box-shadow: 0 0 10px var(--accent-magenta);
        }

        .stCheckbox span { /* Checkbox label */
            color: var(--text-light);
            font-family: 'Roboto Mono', monospace;
            font-size: 1.1rem;
        }
        .stCheckbox [data-testid="stCheckbox"] input[type="checkbox"] {
            transform: scale(1.5);
            accent-color: var(--accent-green);
        }

        /* Streamlitのボタンをターゲット */
        .stButton.action-button-custom > button {
            background-color: var(--accent-cyan);
            color: var(--bg-dark);
            border: none;
            padding: 15px 30px;
            border-radius: 5px;
            font-family: 'Orbitron', sans-serif;
            font-size: 1.2rem;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 0 15px var(--accent-cyan);
            text-transform: uppercase;
            letter-spacing: 1px;
            width: 100%;
        }

        .stButton.action-button-custom > button:hover {
            background-color: var(--accent-green);
            box-shadow: 0 0 20px var(--accent-green);
            transform: translateY(-3px);
        }

        .warning-message-custom {
            background-color: rgba(255, 165, 0, 0.1);
            border: 1px solid orange;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
            font-size: 1rem;
            text-align: center;
            color: orange;
            box-shadow: 0 0 10px rgba(255, 165, 0, 0.5);
        }

        .info-message-form-custom {
            background-color: rgba(0, 255, 255, 0.1);
            border: 1px solid var(--accent-cyan);
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
            font-size: 1rem;
            text-align: center;
            color: var(--accent-cyan);
            box-shadow: 0 0 10px rgba(0, 255, 255, 0.5);
        }

        .settings-section-title-custom {
            font-family: 'Orbitron', sans-serif;
            font-size: 1.8rem;
            color: var(--accent-green);
            text-shadow: 0 0 8px var(--accent-green);
            margin-bottom: 20px;
            border-bottom: 1px dashed #333;
            padding-bottom: 10px;
        }

        /* Streamlit expander styling */
        [data-testid="stExpander"] {
            background-color: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: 8px;
            padding: 0px; /* Adjust padding as needed */
            box-shadow: 0 0 15px rgba(255, 0, 255, 0.3);
        }
        [data-testid="stExpander"] .st-emotion-cache-p5m90l { /* Expander header */
            font-family: 'Orbitron', sans-serif;
            font-size: 1.5rem;
            color: var(--accent-magenta);
            text-shadow: 0 0 8px var(--accent-magenta);
            padding: 25px;
            margin-bottom: 0;
        }
        [data-testid="stExpander"] .st-emotion-cache-p5m90l:hover {
            color: var(--accent-cyan);
            text-shadow: 0 0 8px var(--accent-cyan);
        }
        [data-testid="stExpander"] .st-emotion-cache-1m6g9o3 { /* Expander content area */
            padding: 0 25px 25px 25px;
        }

        /* Responsive adjustments */
        @media (max-width: 1024px) {
            .app-title {
                font-size: 2.8rem;
            }
            .gym-title-cyber {
                font-size: 1.8rem;
            }
            .metric-value-custom {
                font-size: 2rem;
            }
        }

        @media (max-width: 768px) {
            [data-testid="stSidebar"] {
                width: 100%;
                height: auto;
                padding: 15px;
                border-right: none;
                border-bottom: 1px solid var(--accent-cyan);
                box-shadow: 0 2px 10px rgba(0, 255, 255, 0.3);
            }
            [data-testid="stSidebarNav"] ul {
                display: flex;
                justify-content: space-around;
                flex-wrap: wrap;
            }
            [data-testid="stSidebarNav"] li {
                margin: 0 5px 10px 5px;
            }
            [data-testid="stSidebar"] .st-emotion-cache-vk32gh, /* Sidebar title */
            [data-testid="stSidebar"] .stButton > button { /* Logout button */
                display: none; /* Hide for smaller screens to save space */
            }
            .app-title {
                font-size: 2.2rem;
            }
            .gym-title-cyber {
                font-size: 1.5rem;
            }
            .metrics-grid {
                grid-template-columns: 1fr;
            }
            .ai-advice-header, .recipe-header, .data-table-header-custom {
                font-size: 1.3rem;
            }
            .stButton.action-button-custom > button {
                width: 100%;
            }
        }

        @media (max-width: 480px) {
            .app-title {
                font-size: 1.8rem;
            }
            .gym-title-cyber {
                font-size: 1.2rem;
            }
            .metric-value-custom {
                font-size: 1.8rem;
            }
        }
    </style>
""", unsafe_allow_html=True)

# 認証チェック
if not check_password():
    st.stop()

# Firebase初期化
@st.cache_resource
def init_firebase():
    return FirebaseHandler()

fb = init_firebase()

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

# メイン画面
def main_page():
    st.markdown('<div class="app-header"><h1 class="app-title">💪 健康管理アプリ <span class="glitch">MATRIX</span></h1><p class="app-subtitle">サイバーウェルネスを最適化</p></div>', unsafe_allow_html=True)
    
    # データ読み込み
    weight_df = fb.get_weight_data()
    gym_df = fb.get_gym_data()
    calorie_df = fb.get_calorie_data()
    settings = fb.get_user_settings()
    
    # 連続日数と称号
    consecutive_days = fb.calculate_consecutive_gym_days()
    title = get_gym_title(consecutive_days)
    
    st.markdown(
        f'<div class="gym-status-card"><div class="gym-title-cyber">🏆 あなたは<span class="neon-text">{title}</span>です</div><div class="gym-consecutive-days">(連続{consecutive_days}日)</div></div>',
        unsafe_allow_html=True
    )
    
    # AI提案
    predictor = HealthPredictor(weight_df, gym_df, calorie_df)
    if predictor.can_predict():
        with st.expander("🤖 今日のAIアドバイス", expanded=True):
            result = predictor.get_daily_advice()
            
            st.markdown(f'<div class="ai-advice-content">{result["advice"]}</div>', unsafe_allow_html=True)
            
            if result['recipes'] and result['recipes']['recipes']:
                st.markdown('<div class="recipe-section">', unsafe_allow_html=True)
                st.markdown(f'<div class="recipe-header">🍽️ おすすめレシピ ({result["recipes"]["category"]})</div>', unsafe_allow_html=True)
                
                for recipe in result['recipes']['recipes']:
                    st.markdown(f"""
                        <div class="recipe-item">
                            <div>
                                <div class="recipe-title"><a href="{recipe['url']}" target="_blank">{recipe['title']}</a></div>
                                <div class="recipe-snippet">{recipe['snippet']}</div>
                            </div>
                            <div class="recipe-source">📍 {recipe['source']}</div>
                        </div>
                    """, unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True) # Close recipe-section
    else:
        days_left = 30 - len(weight_df)
        st.markdown(f'<div class="info-message-custom">📊 AIアドバイスまであと**{days_left}日**です。毎日記録を続けましょう!</div>', unsafe_allow_html=True)
    
    # 期間選択
    st.markdown('<div class="period-selection-container">', unsafe_allow_html=True)
    period = st.selectbox("表示期間", ["週", "月", "年"], key="period_select", label_visibility="collapsed")
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
    st.markdown('<div class="metrics-grid">', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="metric-card-wrapper">', unsafe_allow_html=True)
        st.markdown('<div class="metric-label-custom">現在の体重</div>', unsafe_allow_html=True)
        if not filtered_weight.empty:
            current_weight = filtered_weight.iloc[-1]['weight']
            weight_change = current_weight - filtered_weight.iloc[0]['weight']
            change_class = "positive" if weight_change < 0 else "negative" # 体重は減るとポジティブ
            st.markdown(f'<div class="metric-value-custom">{current_weight:.1f} <small>kg</small></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-change-custom {change_class}">{weight_change:+.1f} kg</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="metric-value-custom">-- <small>kg</small></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-card-wrapper">', unsafe_allow_html=True)
        st.markdown('<div class="metric-label-custom">目標体重</div>', unsafe_allow_html=True)
        weight_goal = settings.get('weight_goal', 70.0)
        if not filtered_weight.empty:
            diff = current_weight - weight_goal
            change_class = "positive" if diff < 0 else "negative" # 目標より低いとポジティブ
            st.markdown(f'<div class="metric-value-custom">{weight_goal:.1f} <small>kg</small></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-goal-custom {change_class}">{diff:+.1f} kg</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="metric-value-custom">{weight_goal:.1f} <small>kg</small></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-card-wrapper">', unsafe_allow_html=True)
        st.markdown('<div class="metric-label-custom">ジム回数</div>', unsafe_allow_html=True)
        gym_count = filtered_gym['went_to_gym'].sum() if not filtered_gym.empty else 0
        st.markdown(f'<div class="metric-value-custom">{gym_count} <small>回</small></div>', unsafe_allow_html=True)
        # ジム回数の変化は元のコードにロジックがないため、ダミー値を表示
        st.markdown('<div class="metric-change-custom positive">+3 回 (今月)</div>', unsafe_allow_html=True) 
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="metric-card-wrapper">', unsafe_allow_html=True)
        st.markdown('<div class="metric-label-custom">平均消費カロリー</div>', unsafe_allow_html=True)
        avg_calories = filtered_calorie['calories'].mean() if not filtered_calorie.empty else 0
        calorie_goal = settings.get('calorie_goal', 2000)
        change_class = "positive" if avg_calories > calorie_goal else "negative" # 目標より高いとポジティブ
        st.markdown(f'<div class="metric-value-custom">{avg_calories:.0f} <small>kcal</small></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-goal-custom {change_class}">目標: {calorie_goal} kcal</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True) # Close metrics-grid
    
    # グラフ表示
    st.markdown('<div class="graph-container">', unsafe_allow_html=True)
    st.markdown('<div class="graph-title-custom">体重推移グラフ</div>', unsafe_allow_html=True)
    if not filtered_weight.empty:
        fig = go.Figure()
        
        # 体重ライン
        fig.add_trace(go.Scatter(
            x=filtered_weight['date'],
            y=filtered_weight['weight'],
            mode='lines+markers',
            name='体重',
            line=dict(color=var_to_hex('--accent-cyan'), width=3),
            marker=dict(size=8, color=var_to_hex('--accent-cyan')),
            hovertemplate='<b>日付</b>: %{x|%Y-%m-%d}<br><b>体重</b>: %{y:.1f} kg<extra></extra>'
        ))
        
        # 目標体重ライン
        fig.add_trace(go.Scatter(
            x=filtered_weight['date'],
            y=[weight_goal] * len(filtered_weight),
            mode='lines',
            name='目標体重',
            line=dict(color=var_to_hex('--accent-magenta'), width=2, dash='dash'),
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
                    size=15,
                    color=var_to_hex('--accent-green'),
                    symbol='star',
                    line=dict(color='darkgreen', width=2)
                ),
                hovertemplate='<b>ジムに行った日</b><br>%{x|%Y-%m-%d}<extra></extra>'
            ))
        
        fig.update_layout(
            title=dict(
                text="体重推移グラフ",
                font=dict(size=24, color=var_to_hex('--accent-cyan'), family='Orbitron')
            ),
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
                font=dict(color=var_to_hex('--text-light'), family='Roboto Mono')
            ),
            plot_bgcolor=var_to_hex('--card-bg'), # グラフの背景色
            paper_bgcolor=var_to_hex('--card-bg'), # 全体の背景色
            font=dict(color=var_to_hex('--text-light'), family='Roboto Mono'),
            xaxis=dict(gridcolor='#222', linecolor='#444'),
            yaxis=dict(gridcolor='#222', linecolor='#444')
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # データテーブル
        with st.expander("📊 詳細データログ"): # Expander header will be styled by CSS
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
    else:
        st.markdown('<div class="info-message-custom">📝 データがまだありません。データ入力画面から記録を始めましょう!</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True) # Close graph-container

# カラー変数をPythonで利用するためのヘルパー関数
def var_to_hex(var_name):
    # CSS変数から直接値を取得することはできないため、ハードコード
    colors = {
        '--accent-cyan': '#00FFFF',
        '--accent-magenta': '#FF00FF',
        '--accent-green': '#00FF00',
        '--text-light': '#E0E0E0',
        '--card-bg': '#1A1A1A'
    }
    return colors.get(var_name, '#FFFFFF') # デフォルトは白

# データ入力画面
def input_page():
    st.markdown('<h2 class="page-title-custom">📝 データ入力インターフェース</h2>', unsafe_allow_html=True)
    
    today = datetime.now().date()
    
    # 既存データの読み込み
    weight_df = fb.get_weight_data()
    gym_df = fb.get_gym_data()
    calorie_df = fb.get_calorie_data()

    # 今日のデータがあれば表示
    today_weight_record = weight_df[weight_df['date'] == pd.Timestamp(today)]
    today_gym_record = gym_df[gym_df['date'] == pd.Timestamp(today)]
    today_calorie_record = calorie_df[calorie_df['date'] == pd.Timestamp(today)]
    
    default_weight = today_weight_record.iloc[0]['weight'] if not today_weight_record.empty else 0.0
    default_gym = today_gym_record.iloc[0]['went_to_gym'] if not today_gym_record.empty else False
    default_calorie = int(today_calorie_record.iloc[0]['calories']) if not today_calorie_record.empty else 0
    
    # 日付選択 (過去の日付は編集不可)
    selected_date = st.date_input(
        "日付",
        value=today,
        max_value=today,
        min_value=datetime(2026, 1, 1).date(), # 最小日付は元のコードに合わせる
        key="input_date_picker",
        label_visibility="collapsed",
        disabled=True # 常に今日の日付のみ入力可能にするためdisabled
    )
    
    # 今日以外は編集不可のメッセージ
    if selected_date != today:
        st.markdown('<div class="warning-message-custom">⚠️ 過去の日付は編集できません(翌0時以降)</div>', unsafe_allow_html=True)
        st.markdown('<div class="info-message-form-custom">💡 今日のデータのみ入力・編集が可能です</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<label class="form-group-label">体重 (kg)</label>', unsafe_allow_html=True)
        weight = st.number_input(
            "体重 (kg)",
            min_value=0.0,
            max_value=300.0,
            value=float(default_weight),
            step=0.1,
            help="今日の体重を入力してください",
            key="input_weight",
            label_visibility="collapsed"
        )
    
    with col2:
        st.markdown('<label class="form-group-label" style="margin-top: 20px;">ジムに行った</label>', unsafe_allow_html=True) # Adjust margin-top for alignment
        went_to_gym = st.checkbox(
            "ジムに行った",
            value=default_gym,
            help="今日ジムに行った場合はチェック",
            key="input_gym",
            label_visibility="collapsed"
        )
    
    st.markdown('<label class="form-group-label">消費カロリー (kcal)</label>', unsafe_allow_html=True)
    calories = st.number_input(
        "消費カロリー (kcal)",
        min_value=0,
        max_value=10000,
        value=default_calorie,
        step=50,
        help="今日の総消費カロリーを入力",
        key="input_calories",
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col2:
        if st.button("💾 データ保存", type="primary", use_container_width=True, key="save_data_button"):
            if weight > 0:
                try:
                    fb.save_weight(selected_date, weight)
                    fb.save_gym_record(selected_date, went_to_gym)
                    fb.save_calorie_record(selected_date, calories)
                    st.success("✅ データを保存しました!")
                    st.balloons()
                except Exception as e:
                    st.error(f"❌ エラーが発生しました: {str(e)}")
            else:
                st.warning("⚠️ 体重を入力してください")

# 設定画面
def settings_page():
    st.markdown('<h2 class="page-title-custom">⚙️ システム設定</h2>', unsafe_allow_html=True)
    
    settings = fb.get_user_settings()
    
    st.markdown('<div class="settings-section-title-custom">🎯 目標設定</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<label class="form-group-label">目標体重 (kg)</label>', unsafe_allow_html=True)
        weight_goal = st.number_input(
            "目標体重 (kg)",
            min_value=0.0,
            max_value=300.0,
            value=float(settings.get('weight_goal', 70.0)),
            step=0.1,
            key="setting_weight_goal",
            label_visibility="collapsed"
        )
    
    with col2:
        st.markdown('<label class="form-group-label">目標消費カロリー (kcal)</label>', unsafe_allow_html=True)
        calorie_goal = st.number_input(
            "目標消費カロリー (kcal)",
            min_value=0,
            max_value=10000,
            value=int(settings.get('calorie_goal', 2000)),
            step=100,
            key="setting_calorie_goal",
            label_visibility="collapsed"
        )
    
    st.markdown("---")
    st.markdown('<div class="settings-section-title-custom">🔐 パスワード変更</div>', unsafe_allow_html=True)
    
    st.markdown('<label class="form-group-label">新しいパスワード</label>', unsafe_allow_html=True)
    new_password = st.text_input(
        "新しいパスワード",
        type="password",
        help="パスワードを変更する場合は入力してください",
        key="setting_new_password",
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col2:
        if st.button("💾 設定を保存", type="primary", use_container_width=True, key="save_settings_button"):
            try:
                new_settings = {
                    'weight_goal': weight_goal,
                    'calorie_goal': calorie_goal,
                    # 新しいパスワードが入力されていればそれを使用、なければ既存のパスワードを維持
                    'password': new_password if new_password else settings.get('password', 'yasu0122')
                }
                fb.update_user_settings(new_settings)
                st.success("✅ 設定を保存しました!")
            except Exception as e:
                st.error(f"❌ エラーが発生しました: {str(e)}")

# メイン処理
def main():
    # サイドバーでページ選択
    with st.sidebar:
        st.markdown('<div class="sidebar-title">MANA HEALTH OS</div>', unsafe_allow_html=True)
        page = st.radio(
            "ページを選択",
            ["メイン画面", "データ入力", "設定"],
            label_visibility="collapsed",
            key="sidebar_navigation"
        )
        
        st.markdown("---")
        
        if st.button("🚪 ログアウト", use_container_width=True, key="logout_button"):
            logout()
    
    if page == "メイン画面":
        main_page()
    elif page == "データ入力":
        input_page()
    elif page == "設定":
        settings_page()

if __name__ == "__main__":
    main()

