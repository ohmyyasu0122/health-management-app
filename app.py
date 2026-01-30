import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

# NOTE: 以下のインポートは、ユーザーの元のコードに合わせていますが、
# 実行可能にするために一時的にモッククラスに置き換えています。
# 実際のアプリケーションでは、元のインポートを使用してください。
# from utils.firebase_handler import FirebaseHandler
# from utils.auth import check_password, logout
# from utils.ml_predictor import HealthPredictor

# --- モッククラス (実際のアプリケーションでは元のインポートを使用) ---
class FirebaseHandler:
    def get_weight_data(self):
        dates = [datetime.now().date() - timedelta(days=i) for i in range(40, 0, -1)]
        weights = [75.0 - i * 0.1 + (i % 5) * 0.2 for i in range(40)]
        return pd.DataFrame({'date': pd.to_datetime(dates), 'weight': weights})

    def get_gym_data(self):
        dates = [datetime.now().date() - timedelta(days=i) for i in range(40, 0, -1)]
        gym_status = [True if i % 3 == 0 else False for i in range(40)]
        return pd.DataFrame({'date': pd.to_datetime(dates), 'went_to_gym': gym_status})

    def get_calorie_data(self):
        dates = [datetime.now().date() - timedelta(days=i) for i in range(40, 0, -1)]
        calories = [2000 + (i % 7) * 50 - (i % 3) * 20 for i in range(40)]
        return pd.DataFrame({'date': pd.to_datetime(dates), 'calories': calories})

    def get_user_settings(self):
        return {'weight_goal': 70.0, 'calorie_goal': 2000, 'password': 'yasu0122'}

    def calculate_consecutive_gym_days(self):
        return 10 # モック値

    def save_weight(self, date, weight):
        st.success(f"Mock: Weight {weight} saved for {date}")

    def save_gym_record(self, date, went_to_gym):
        st.success(f"Mock: Gym status {went_to_gym} saved for {date}")

    def save_calorie_record(self, date, calories):
        st.success(f"Mock: Calories {calories} saved for {date}")

    def update_user_settings(self, settings):
        st.success(f"Mock: Settings updated: {settings}")

class HealthPredictor:
    def __init__(self, weight_df, gym_df, calorie_df):
        pass # モックなので実際のロジックは不要

    def get_daily_advice(self):
        return {
            'advice': "今日のAIアドバイス: 体重は順調に減少傾向です！この調子で運動と食事のバランスを保ちましょう。特に、週末の活動量を少し増やすと、さらに効果的かもしれません。",
            'recipes': {
                'category': '低カロリー',
                'recipes': [
                    {'title': '鶏むね肉と野菜のヘルシー蒸し', 'url': 'https://example.com/recipe1', 'snippet': '高タンパク低脂質で満足感のある一品。'},
                    {'title': '豆腐とわかめの中華スープ', 'url': 'https://example.com/recipe2', 'snippet': '体を温め、代謝アップをサポート。'}
                ]
            }
        }

def check_password():
    return True # モックなので常に認証済み

def logout():
    st.info("Mock: Logged out.")
# --- モッククラスここまで ---


# ページ設定
st.set_page_config(
    page_title="サイバー健康管理システム", # タイトルをテーマに合わせて変更
    page_icon="favicon.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- カスタムCSS (サイバーパンク/近未来風に大幅変更) ---
st.markdown("""
<style>
    /* Google FontsからRoboto Monoをインポート */
    @import url('https://fonts.googleapis.com/css2?family=Roboto+Mono:wght@400;700&display=swap');

    /* 全体的なフォントと背景 */
    body {
        font-family: 'Roboto Mono', monospace, 'Segoe UI', sans-serif; /* モノスペース系フォントを優先 */
        background-color: #0a0a0a; /* 非常に暗い背景 */
        color: #e0e0e0; /* 基本の文字色を明るいグレー */
    }
    
    /* Streamlitのメインコンテナのパディング調整 */
    .main .block-container {
        padding-top: 2rem;
        padding-right: 2rem;
        padding-left: 2rem;
        padding-bottom: 2rem;
    }

    /* メインタイトル */
    .main-title {
        font-size: 3rem; /* より大きく */
        font-weight: 700; /* 極太 */
        color: #ff00ff; /* ネオンマゼンタ */
        text-align: center;
        margin-bottom: 2.5rem;
        padding-bottom: 0.8rem;
        border-bottom: 2px solid #00ffff; /* ネオンシアンの下線 */
        text-shadow: 0 0 10px #ff00ff, 0 0 20px #ff00ff, 0 0 30px #ff00ff; /* ネオンの光 */
        letter-spacing: 2px; /* 文字間隔 */
    }

    /* ジムの称号 */
    .gym-title {
        font-size: 1.8rem;
        font-weight: 700;
        color: #00ff00; /* ネオンライムグリーン */
        text-align: center;
        padding: 1.5rem;
        background: linear-gradient(90deg, #1a1a1a, #0a0a0a); /* 暗いグラデーション */
        border-radius: 5px; /* シャープな角 */
        margin-bottom: 3rem;
        box-shadow: 0 0 15px rgba(0, 255, 255, 0.5), 0 0 25px rgba(255, 0, 255, 0.3); /* シアンとマゼンタの複合ネオン影 */
        text-shadow: 0 0 5px #00ff00; /* 軽いネオン光 */
        border: 1px solid #00ffff; /* ネオンシアンのボーダー */
    }
    .gym-title strong {
        color: #ff00ff; /* 強調文字はネオンマゼンタ */
        text-shadow: 0 0 8px #ff00ff;
    }

    /* カードスタイルのコンテナ */
    .stContainer {
        background-color: #1a1a1a; /* 暗い背景 */
        border-radius: 8px; /* 少し丸み */
        box-shadow: 0 0 10px rgba(0, 255, 255, 0.3); /* シアンのネオン影 */
        padding: 1.8rem;
        margin-bottom: 2rem;
        border: 1px solid #00ffff; /* ネオンシアンのボーダー */
    }
    .stContainer h3 { /* コンテナ内のサブヘッダー */
        color: #00ffff; /* ネオンシアン */
        text-shadow: 0 0 5px #00ffff;
        border-bottom: 1px dashed #00ffff;
        padding-bottom: 0.5rem;
        margin-bottom: 1.5rem;
    }

    /* メトリクス */
    .stMetric {
        background-color: #1a1a1a;
        border-radius: 5px;
        padding: 1.2rem;
        box-shadow: 0 0 8px rgba(255, 0, 255, 0.3); /* マゼンタのネオン影 */
        border: 1px solid #ff00ff; /* マゼンタのボーダー */
        text-align: center;
    }
    .stMetric > div:first-child { /* ラベル */
        font-size: 0.9rem;
        color: #e0e0e0; /* 明るいグレー */
        margin-bottom: 0.5rem;
    }
    .stMetric > div:nth-child(2) { /* 値 */
        font-size: 2rem;
        font-weight: 700;
        color: #00ff00; /* ネオンライムグリーン */
        text-shadow: 0 0 5px #00ff00;
    }
    .stMetric > div:nth-child(3) { /* 変化量/目標 */
        font-size: 1rem;
        color: #00ffff; /* ネオンシアン */
    }

    /* ボタン */
    .stButton > button {
        background-color: #00ffff; /* ネオンシアン */
        color: #0a0a0a; /* 暗い文字色 */
        border-radius: 5px; /* シャープな角 */
        border: none;
        padding: 0.8rem 1.5rem;
        font-size: 1.1rem;
        font-weight: 700;
        transition: all 0.2s ease-in-out;
        box-shadow: 0 0 5px #00ffff;
    }
    .stButton > button:hover {
        background-color: #ff00ff; /* ホバー時はマゼンタ */
        color: #0a0a0a;
        box-shadow: 0 0 15px #ff00ff, 0 0 25px #ff00ff; /* より強いネオン光 */
        transform: scale(1.02); /* 少し拡大 */
    }
    .stButton > button:active {
        transform: scale(0.98);
    }

    /* Expander */
    .stExpander {
        border: 1px solid #ff00ff; /* マゼンタのボーダー */
        border-radius: 8px;
        box-shadow: 0 0 10px rgba(255, 0, 255, 0.3);
        margin-bottom: 1.5rem;
    }
    .stExpander > div:first-child { /* Expander header */
        background-color: #1a1a1a; /* 暗い背景色 */
        border-radius: 8px 8px 0 0;
        padding: 1rem 1.5rem;
        font-weight: 700;
        color: #00ffff; /* ネオンシアン */
        text-shadow: 0 0 5px #00ffff;
    }
    .stExpander > div:nth-child(2) { /* Expander content */
        padding: 1.5rem;
        background-color: #0a0a0a; /* コンテンツ背景も暗く */
        color: #e0e0e0; /* 読みやすい明るいグレー */
    }
    .stExpander > div:nth-child(2) h3 { /* レシピタイトル */
        color: #00ff00; /* ライムグリーン */
        text-shadow: none;
        border-bottom: 1px dotted #00ff00;
    }
    .stExpander > div:nth-child(2) strong {
        color: #ff00ff; /* マゼンタ */
    }
    .stExpander > div:nth-child(2) a {
        color: #00ffff; /* リンクはシアン */
        text-decoration: none;
    }
    .stExpander > div:nth-child(2) a:hover {
        text-decoration: underline;
    }


    /* Sidebar */
    .css-1d391kg { /* Streamlit sidebar class */
        background-color: #0a0a0a; /* サイドバーの背景も暗く */
        box-shadow: 2px 0 15px rgba(0, 255, 255, 0.5); /* シアンのネオン影 */
        border-right: 1px solid #00ffff;
    }
    .sidebar .stRadio > label {
        font-size: 1.1rem;
        padding: 0.8rem 0;
        color: #e0e0e0; /* 明るいグレー */
    }
    .sidebar .stRadio > label > div:first-child {
        color: #e0e0e0;
    }
    .sidebar .stRadio > label > div:first-child:hover {
        color: #00ffff; /* ホバーでネオンシアン */
        text-shadow: 0 0 5px #00ffff;
    }
    .sidebar .stRadio > label > div:first-child > input:checked + div { /* 選択されたラジオボタン */
        color: #ff00ff !important; /* マゼンタ */
        text-shadow: 0 0 8px #ff00ff !important;
    }
    .sidebar .stButton > button {
        background-color: #ff00ff; /* ログアウトボタンはマゼンタ */
        box-shadow: 0 0 5px #ff00ff;
    }
    .sidebar .stButton > button:hover {
        background-color: #00ffff; /* ホバーでシアン */
        box-shadow: 0 0 15px #00ffff;
    }
    .sidebar .stTitle { /* サイドバータイトル */
        color: #00ff00; /* ライムグリーン */
        text-shadow: 0 0 5px #00ff00;
    }

    /* Info/Warning messages */
    .stAlert {
        border-radius: 5px;
        font-weight: 600;
        text-shadow: 0 0 2px;
    }
    .stAlert.info {
        background-color: #002222; /* 暗いシアン背景 */
        color: #00ffff;
        border-left: 5px solid #00ffff;
        box-shadow: 0 0 8px rgba(0, 255, 255, 0.5);
    }
    .stAlert.warning {
        background-color: #222200; /* 暗い黄色背景 */
        color: #ffff00;
        border-left: 5px solid #ffff00;
        box-shadow: 0 0 8px rgba(255, 255, 0, 0.5);
    }
    .stAlert.success {
        background-color: #002200; /* 暗い緑背景 */
        color: #00ff00;
        border-left: 5px solid #00ff00;
        box-shadow: 0 0 8px rgba(0, 255, 0, 0.5);
    }

    /* Dataframe */
    .stDataFrame {
        border-radius: 8px;
        overflow: hidden;
        border: 1px solid #00ffff; /* シアンのボーダー */
        box-shadow: 0 0 10px rgba(0, 255, 255, 0.3);
    }
    .stDataFrame table {
        border-collapse: collapse;
    }
    .stDataFrame th {
        background-color: #1a1a1a; /* 暗いヘッダー背景 */
        color: #00ffff; /* ネオンシアン */
        font-weight: 700;
        text-shadow: 0 0 3px #00ffff;
        border-bottom: 1px solid #00ffff;
    }
    .stDataFrame td {
        background-color: #0a0a0a; /* 暗いセル背景 */
        color: #e0e0e0; /* 明るいグレー */
        border-bottom: 1px dotted #333333;
    }
    .stDataFrame tr:nth-child(even) td {
        background-color: #101010; /* 縞模様を少し明るく */
    }

    /* Input fields */
    .stNumberInput, .stTextInput, .stDateInput, .stSelectbox {
        margin-bottom: 1.2rem;
    }
    .stNumberInput > div > div > input,
    .stTextInput > div > div > input,
    .stDateInput > div > div > input,
    .stSelectbox > div > div > div > div {
        border-radius: 5px;
        border: 1px solid #00ffff; /* ネオンシアンのボーダー */
        padding: 0.6rem 0.8rem;
        background-color: #1a1a1a; /* 暗い入力フィールド背景 */
        color: #00ff00; /* 入力文字はライムグリーン */
        box-shadow: 0 0 5px rgba(0, 255, 255, 0.2);
    }
    .stNumberInput > div > div > input:focus,
    .stTextInput > div > div > input:focus,
    .stDateInput > div > div > input:focus,
    .stSelectbox > div > div > div > div:focus {
        border-color: #ff00ff; /* フォーカスでマゼンタ */
        box-shadow: 0 0 10px rgba(255, 0, 255, 0.5);
        outline: none; /* デフォルトのアウトラインを消す */
    }
    .stSelectbox > div > div > div > div { /* Selectboxの矢印 */
        color: #00ffff;
    }
    .stSelectbox > div > div > div > div > div > div { /* Selectboxの選択肢 */
        background-color: #1a1a1a;
        color: #00ffff;
    }
    .stSelectbox > div > div > div > div > div > div:hover {
        background-color: #00ffff;
        color: #0a0a0a;
    }
    
    /* Checkbox */
    .stCheckbox > label > div:first-child {
        border: 1px solid #00ffff;
        background-color: #1a1a1a;
    }
    .stCheckbox > label > div:first-child:hover {
        border-color: #ff00ff;
    }
    .stCheckbox > label > div:first-child > div { /* チェックマーク */
        color: #00ff00;
    }
    .stCheckbox > label {
        color: #e0e0e0;
    }

    /* Help text */
    .stHelp {
        color: #888888;
        font-size: 0.85rem;
    }

    /* Subheader */
    h2 {
        color: #00ffff;
        text-shadow: 0 0 5px #00ffff;
        border-bottom: 1px dashed #00ffff;
        padding-bottom: 0.5rem;
        margin-bottom: 1.5rem;
    }
    h3 {
        color: #ff00ff;
        text-shadow: 0 0 3px #ff00ff;
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
        30: "サイバー神", # 称号も少し変更
        15: "ネオン仙人",
        10: "グリッド師範代",
        7: "データマスター",
        5: "システム常連",
        3: "プロトコル慣れ",
        2: "ニュービー",
        1: "トレーニングモジュール"
    }
    
    for days in sorted(titles.keys(), reverse=True):
        if consecutive_days >= days:
            return titles[days]
    return "未接続ユーザー"

# メイン画面
def main_page():
    st.markdown('<div class="main-title">💪 サイバー健康管理システム</div>', unsafe_allow_html=True)
    
    # データ読み込み
    weight_df = fb.get_weight_data()
    gym_df = fb.get_gym_data()
    calorie_df = fb.get_calorie_data()
    settings = fb.get_user_settings()
    
    # 連続日数と称号
    consecutive_days = fb.calculate_consecutive_gym_days()
    title = get_gym_title(consecutive_days)
    
    st.markdown(
        f'<div class="gym-title">🏆 あなたは<strong>{title}</strong>です (連続{consecutive_days}日)</div>',
        unsafe_allow_html=True
    )
    
    # AI提案
    # AIアドバイスセクションをカードで囲む
    st.markdown('<div class="stContainer">', unsafe_allow_html=True)
    if len(weight_df) >= 30:
        with st.expander("🤖 AIアドバイスモジュール", expanded=True): # Expanderタイトルも変更
            predictor = HealthPredictor(weight_df, gym_df, calorie_df)
            result = predictor.get_daily_advice()
            
            st.markdown(result['advice'])
            
            if result['recipes']:
                st.markdown("---")
                st.markdown(f"### 🍽️ 推奨データ ({result['recipes']['category']})") # レシピタイトルも変更
                
                for recipe in result['recipes']['recipes']:
                    with st.container(): # 各レシピもコンテナで囲むことで、将来的なスタイリングが容易になります
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            st.markdown(f"**[{recipe['title']}]({recipe['url']})**")
                            st.caption(recipe['snippet'])
                        with col2:
                            st.caption(f"📍 {recipe['source']}")
                        st.markdown("---")
    else:
        days_left = 30 - len(weight_df)
        st.info(f"📊 AIアドバイスまであと**{days_left}日**です。毎日記録を続けましょう!")
    st.markdown('</div>', unsafe_allow_html=True) # AIアドバイスセクションの終わり
    
    # 期間選択
    st.markdown('<div class="stContainer">', unsafe_allow_html=True)
    st.subheader("📅 データ表示期間") # サブヘッダーも変更
    col1, col2, col3 = st.columns(3)
    with col1:
        period = st.selectbox("表示期間", ["週", "月", "年"], key="period_select", label_visibility="collapsed")
    
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
    st.markdown('</div>', unsafe_allow_html=True) # 期間選択セクションの終わり

    # メトリクス表示
    st.markdown('<div class="stContainer">', unsafe_allow_html=True)
    st.subheader("📈 現在のシステムステータス") # サブヘッダーも変更
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if not filtered_weight.empty:
            current_weight = filtered_weight.iloc[-1]['weight']
            weight_change = current_weight - filtered_weight.iloc[0]['weight']
            st.metric("現在の体重", f"{current_weight:.1f} kg", f"{weight_change:+.1f} kg")
        else:
            st.metric("現在の体重", "-- kg")
    
    with col2:
        weight_goal = settings.get('weight_goal', 70.0)
        if not filtered_weight.empty:
            diff = current_weight - weight_goal
            st.metric("目標体重", f"{weight_goal:.1f} kg", f"{diff:+.1f} kg")
        else:
            st.metric("目標体重", f"{weight_goal:.1f} kg")
    
    with col3:
        gym_count = filtered_gym['went_to_gym'].sum() if not filtered_gym.empty else 0
        st.metric("ジム回数", f"{gym_count}回")
    
    with col4:
        avg_calories = filtered_calorie['calories'].mean() if not filtered_calorie.empty else 0
        calorie_goal = settings.get('calorie_goal', 2000)
        st.metric("平均消費カロリー", f"{avg_calories:.0f} kcal", f"目標: {calorie_goal} kcal")
    st.markdown('</div>', unsafe_allow_html=True) # メトリクスセクションの終わり

    # グラフ表示
    st.markdown('<div class="stContainer">', unsafe_allow_html=True)
    if not filtered_weight.empty:
        fig = go.Figure()
        
        # 体重ライン (色を新しいテーマに合わせる)
        fig.add_trace(go.Scatter(
            x=filtered_weight['date'],
            y=filtered_weight['weight'],
            mode='lines+markers',
            name='体重データ', # 凡例も変更
            line=dict(color='#00ffff', width=3), # ネオンシアン
            marker=dict(size=8, color='#00ffff'),
            hovertemplate='<b>日付</b>: %{x|%Y-%m-%d}<br><b>体重</b>: %{y:.1f} kg<extra></extra>'
        ))
        
        # 目標体重ライン
        fig.add_trace(go.Scatter(
            x=filtered_weight['date'],
            y=[weight_goal] * len(filtered_weight),
            mode='lines',
            name='目標プロトコル', # 凡例も変更
            line=dict(color='#ff00ff', width=2, dash='dash'), # ネオンマゼンタ
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
                name='ジムアクセス', # 凡例も変更
                marker=dict(
                    size=15,
                    color='#00ff00', # ネオンライムグリーン
                    symbol='star',
                    line=dict(color='#00cc00', width=2)
                ),
                hovertemplate='<b>ジムアクセス日</b><br>%{x|%Y-%m-%d}<extra></extra>'
            ))
        
        fig.update_layout(
            title=dict(
                text="体重データログ", # グラフタイトルも変更
                font=dict(size=24, color='#ff00ff') # タイトル色をマゼンタに
            ),
            xaxis_title="タイムスタンプ", # 軸ラベルも変更
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
                font=dict(color='#e0e0e0') # 凡例の文字色
            ),
            plot_bgcolor='#0a0a0a', # グラフの背景色を暗く
            paper_bgcolor='#0a0a0a', # 全体の背景色を暗く
            font=dict(family='Roboto Mono', color='#e0e0e0'), # グラフ内のフォントと色
            xaxis=dict(
                gridcolor='#333333', # グリッド線
                zerolinecolor='#333333',
                tickfont=dict(color='#00ffff') # 軸の目盛り文字色
            ),
            yaxis=dict(
                gridcolor='#333333', # グリッド線
                zerolinecolor='#333333',
                tickfont=dict(color='#00ffff') # 軸の目盛り文字色
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # データテーブル
        with st.expander("📊 詳細データログ"): # Expanderタイトルも変更
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
        st.info("📝 データがまだありません。データ入力画面から記録を始めましょう!")
    st.markdown('</div>', unsafe_allow_html=True) # グラフセクションの終わり

# データ入力画面
def input_page():
    st.title("📝 データ入力モジュール") # タイトルも変更
    
    today = datetime.now().date()
    selected_date = st.date_input(
        "日付",
        value=today,
        max_value=today,
        min_value=datetime(2026, 1, 1).date()
    )
    
    # 今日以外は編集不可
    if selected_date != today:
        st.warning("⚠️ 過去のデータは編集できません(翌0時以降)") # 文言を少し変更
        st.info("💡 今日のデータのみ入力・編集が可能です")
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
    
    st.markdown('<div class="stContainer">', unsafe_allow_html=True) # 入力フォームをカードで囲む
    st.markdown("### 記録するデータ")
    
    col1, col2 = st.columns(2)
    
    with col1:
        weight = st.number_input(
            "体重 (kg)",
            min_value=0.0,
            max_value=300.0,
            value=float(default_weight),
            step=0.1,
            help="今日の体重を入力してください"
        )
    
    with col2:
        went_to_gym = st.checkbox(
            "ジムにアクセス", # 文言を少し変更
            value=default_gym,
            help="今日ジムに行った場合はチェック"
        )
    
    calories = st.number_input(
        "消費カロリー (kcal)",
        min_value=0,
        max_value=10000,
        value=default_calorie,
        step=50,
        help="今日の総消費カロリーを入力"
    )
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col2:
        if st.button("💾 データ保存", type="primary", use_container_width=True): # 文言を少し変更
            if weight > 0:
                try:
                    fb.save_weight(today, weight)
                    fb.save_gym_record(today, went_to_gym)
                    fb.save_calorie_record(today, calories)
                    st.success("✅ データ保存完了!") # 文言を少し変更
                    st.balloons()
                except Exception as e:
                    st.error(f"❌ エラーが発生しました: {str(e)}")
            else:
                st.warning("⚠️ 体重を入力してください")
    st.markdown('</div>', unsafe_allow_html=True) # 入力フォームのカードの終わり

# 設定画面
def settings_page():
    st.title("⚙️ システム設定") # タイトルも変更
    
    settings = fb.get_user_settings()
    
    st.markdown('<div class="stContainer">', unsafe_allow_html=True) # 目標設定をカードで囲む
    st.markdown("### 🎯 目標プロトコル設定") # サブヘッダーも変更
    
    col1, col2 = st.columns(2)
    
    with col1:
        weight_goal = st.number_input(
            "目標体重 (kg)",
            min_value=0.0,
            max_value=300.0,
            value=float(settings.get('weight_goal', 70.0)),
            step=0.1
        )
    
    with col2:
        calorie_goal = st.number_input(
            "目標消費カロリー (kcal)",
            min_value=0,
            max_value=10000,
            value=int(settings.get('calorie_goal', 2000)),
            step=100
        )
    st.markdown('</div>', unsafe_allow_html=True) # 目標設定のカードの終わり

    st.markdown('<div class="stContainer">', unsafe_allow_html=True) # パスワード変更をカードで囲む
    st.markdown("### 🔐 アクセスキー変更") # サブヘッダーも変更
    
    new_password = st.text_input(
        "新しいパスワード",
        type="password",
        help="パスワードを変更する場合は入力してください"
    )
    st.markdown('</div>', unsafe_allow_html=True) # パスワード変更のカードの終わり
    
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

# メイン処理
def main():
    # サイドバーでページ選択
    with st.sidebar:
        st.title("📱 メニュー")
        page = st.radio(
            "ページを選択",
            ["メイン画面", "データ入力", "設定"],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        if st.button("🚪 ログアウト", use_container_width=True):
            logout()
    
    if page == "メイン画面":
        main_page()
    elif page == "データ入力":
        input_page()
    elif page == "設定":
        settings_page()

if __name__ == "__main__":
    main()
