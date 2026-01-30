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
    page_title="やすの健康アプリ",
    page_icon="favicon.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- カスタムCSS (ここを大幅に変更します) ---
st.markdown("""
<style>
    /* 全体的なフォントと背景 */
    body {
        font-family: 'Segoe UI', 'Roboto', 'Helvetica Neue', Arial, sans-serif;
        background-color: #f8f9fa; /* 非常に薄いグレーの背景 */
        color: #333333; /* 基本の文字色 */
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
        font-size: 2.8rem; /* 少し大きく */
        font-weight: 700; /* より太く */
        color: #20c997; /* 新しいメインカラー (ティールグリーン) */
        text-align: center;
        margin-bottom: 2rem; /* 下の余白を増やす */
        padding-bottom: 0.5rem;
        border-bottom: 3px solid #e0f2f7; /* 下線を追加 */
    }

    /* ジムの称号 */
    .gym-title {
        font-size: 1.6rem; /* 少し小さく */
        font-weight: 600;
        color: #ffffff; /* 白文字 */
        text-align: center;
        padding: 1.2rem;
        background: linear-gradient(45deg, #20c997, #00b894); /* グラデーションを調整 */
        border-radius: 12px; /* 角を丸く */
        margin-bottom: 2.5rem; /* 下の余白を増やす */
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1); /* 影を追加 */
    }
    .gym-title strong {
        color: #ffffff; /* 強調文字も白 */
    }

    /* カードスタイルのコンテナ */
    .stContainer {
        background-color: #ffffff; /* 白い背景 */
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08); /* 影を少し強く */
        padding: 1.5rem;
        margin-bottom: 1.5rem; /* 各カードの下に余白 */
    }

    /* メトリクス */
    .stMetric {
        background-color: #ffffff;
        border-radius: 8px;
        padding: 1rem;
        box-shadow: 0 1px 4px rgba(0, 0, 0, 0.05);
        border: 1px solid #e0f2f7; /* 軽いボーダー */
        text-align: center;
    }
    .stMetric > div:first-child { /* ラベル */
        font-size: 0.9rem;
        color: #6c757d;
        margin-bottom: 0.5rem;
    }
    .stMetric > div:nth-child(2) { /* 値 */
        font-size: 1.8rem;
        font-weight: 700;
        color: #333333;
    }
    .stMetric > div:nth-child(3) { /* 変化量/目標 */
        font-size: 1rem;
        color: #6c757d;
    }

    /* ボタン */
    .stButton > button {
        background-color: #20c997; /* メインカラー */
        color: white;
        border-radius: 8px; /* 角を丸く */
        border: none;
        padding: 0.6rem 1.2rem;
        font-size: 1rem;
        font-weight: 600;
        transition: background-color 0.2s, transform 0.2s;
    }
    .stButton > button:hover {
        background-color: #00b894; /* ホバー時の色 */
        transform: translateY(-2px); /* 少し浮き上がる */
    }
    .stButton > button:active {
        transform: translateY(0);
    }

    /* Expander */
    .stExpander {
        border: 1px solid #e0f2f7;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
        margin-bottom: 1.5rem;
    }
    .stExpander > div:first-child { /* Expander header */
        background-color: #f0f4f8; /* 軽い背景色 */
        border-radius: 10px 10px 0 0;
        padding: 0.8rem 1.2rem;
        font-weight: 600;
        color: #333333;
    }
    .stExpander > div:nth-child(2) { /* Expander content */
        padding: 1.2rem;
    }

    /* Sidebar */
    .css-1d391kg { /* Streamlit sidebar class */
        background-color: #ffffff; /* サイドバーの背景を白に */
        box-shadow: 2px 0 8px rgba(0, 0, 0, 0.05);
    }
    .sidebar .stRadio > label {
        font-size: 1.1rem;
        padding: 0.5rem 0;
    }
    .sidebar .stRadio > label > div:first-child {
        color: #333333;
    }
    .sidebar .stRadio > label > div:first-child:hover {
        color: #20c997;
    }
    .sidebar .stButton > button {
        background-color: #dc3545; /* ログアウトボタンは赤系 */
    }
    .sidebar .stButton > button:hover {
        background-color: #c82333;
    }

    /* Info/Warning messages */
    .stAlert {
        border-radius: 8px;
    }
    .stAlert.info {
        background-color: #e0f2f7; /* 薄い青 */
        color: #007bff;
        border-left: 5px solid #007bff;
    }
    .stAlert.warning {
        background-color: #fff3cd; /* 薄い黄色 */
        color: #856404;
        border-left: 5px solid #ffc107;
    }
    .stAlert.success {
        background-color: #d4edda; /* 薄い緑 */
        color: #28a745;
        border-left: 5px solid #28a745;
    }

    /* Dataframe */
    .stDataFrame {
        border-radius: 10px;
        overflow: hidden; /* 角丸を適用 */
    }
    .stDataFrame table {
        border-collapse: collapse;
    }
    .stDataFrame th {
        background-color: #f0f4f8;
        color: #333333;
        font-weight: 600;
    }
    .stDataFrame td {
        background-color: #ffffff;
    }
    .stDataFrame tr:nth-child(even) td {
        background-color: #f8f9fa; /* 縞模様 */
    }

    /* Input fields */
    .stNumberInput, .stTextInput, .stDateInput, .stSelectbox {
        margin-bottom: 1rem;
    }
    .stNumberInput > div > div > input,
    .stTextInput > div > div > input,
    .stDateInput > div > div > input,
    .stSelectbox > div > div > div > div {
        border-radius: 8px;
        border: 1px solid #ced4da;
        padding: 0.5rem 0.75rem;
    }
    .stNumberInput > div > div > input:focus,
    .stTextInput > div > div > input:focus,
    .stDateInput > div > div > input:focus,
    .stSelectbox > div > div > div > div:focus {
        border-color: #20c997;
        box-shadow: 0 0 0 0.2rem rgba(32, 201, 151, 0.25);
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
    st.markdown('<div class="main-title">💪 健康管理アプリ</div>', unsafe_allow_html=True)
    
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
        with st.expander("🤖 今日のAIアドバイス", expanded=True):
            predictor = HealthPredictor(weight_df, gym_df, calorie_df)
            result = predictor.get_daily_advice()
            
            st.markdown(result['advice'])
            
            if result['recipes']:
                st.markdown("---")
                st.markdown(f"### 🍽️ おすすめレシピ ({result['recipes']['category']})")
                
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
    st.subheader("📅 表示期間の選択")
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
    st.subheader("📈 現在の状況")
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
            name='体重',
            line=dict(color='#20c997', width=3), # メインカラー
            marker=dict(size=8, color='#20c997'),
            hovertemplate='<b>日付</b>: %{x|%Y-%m-%d}<br><b>体重</b>: %{y:.1f} kg<extra></extra>'
        ))
        
        # 目標体重ライン
        fig.add_trace(go.Scatter(
            x=filtered_weight['date'],
            y=[weight_goal] * len(filtered_weight),
            mode='lines',
            name='目標体重',
            line=dict(color='#fd7e14', width=2, dash='dash'), # アクセントカラー (オレンジ系)
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
                    color='#17a2b8', # 別のアクセントカラー (水色系)
                    symbol='star',
                    line=dict(color='#138496', width=2)
                ),
                hovertemplate='<b>ジムに行った日</b><br>%{x|%Y-%m-%d}<extra></extra>'
            ))
        
        fig.update_layout(
            title=dict(
                text="体重推移グラフ",
                font=dict(size=24, color='#333333') # タイトル色も調整
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
                x=1
            ),
            plot_bgcolor='#ffffff', # グラフの背景色
            paper_bgcolor='#ffffff', # 全体の背景色
            font=dict(family='Segoe UI', color='#333333') # グラフ内のフォント
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # データテーブル
        with st.expander("📊 詳細データを表示"):
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
    st.title("📝 データ入力")
    
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
            "ジムに行った",
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
    st.markdown('</div>', unsafe_allow_html=True) # 入力フォームのカードの終わり

# 設定画面
def settings_page():
    st.title("⚙️ 設定")
    
    settings = fb.get_user_settings()
    
    st.markdown('<div class="stContainer">', unsafe_allow_html=True) # 目標設定をカードで囲む
    st.markdown("### 🎯 目標設定")
    
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
    st.markdown("### 🔐 パスワード変更")
    
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
