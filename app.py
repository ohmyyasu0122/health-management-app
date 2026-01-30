import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
from utils.firebase_handler import FirebaseHandler
from utils.auth import check_password, logout
from utils.ml_predictor import HealthPredictor

# ページ設定
st.set_page_config(
    page_title="やすの健康アプリ",
    page_icon="favicon.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

# カスタムCSS - モダンデザイン
st.markdown("""
<style>
    /* 全体の背景 */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* メインコンテンツエリア */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        backdrop-filter: blur(10px);
    }
    
    /* タイトル */
    .main-title {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    /* ジム称号カード */
    .gym-title {
        font-size: 1.8rem;
        color: #ffffff;
        text-align: center;
        padding: 1.5rem;
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(245, 87, 108, 0.4);
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.02); }
    }
    
    /* メトリクスカード */
    .stMetric {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .stMetric:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
    }
    
    .stMetric label {
        font-size: 1rem !important;
        font-weight: 600 !important;
        color: #667eea !important;
    }
    
    .stMetric [data-testid="stMetricValue"] {
        font-size: 2rem !important;
        font-weight: 700 !important;
        color: #2d3748 !important;
    }
    
    /* ボタンスタイル */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }
    
    /* 入力フィールド */
    .stNumberInput > div > div > input,
    .stDateInput > div > div > input {
        border-radius: 10px;
        border: 2px solid #e2e8f0;
        padding: 0.75rem;
        transition: border-color 0.3s ease;
    }
    
    .stNumberInput > div > div > input:focus,
    .stDateInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* チェックボックス */
    .stCheckbox {
        background: #f7fafc;
        padding: 1rem;
        border-radius: 10px;
        border: 2px solid #e2e8f0;
    }
    
    /* エキスパンダー */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
        border-radius: 10px;
        font-weight: 600;
        padding: 1rem;
    }
    
    /* サイドバー */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    [data-testid="stSidebar"] .stRadio > label {
        color: white !important;
        font-weight: 600;
    }
    
    [data-testid="stSidebar"] .stRadio > div {
        background: rgba(255, 255, 255, 0.1);
        padding: 0.5rem;
        border-radius: 10px;
    }
    
    /* データテーブル */
    .dataframe {
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
    }
    
    /* セレクトボックス */
    .stSelectbox > div > div {
        border-radius: 10px;
        border: 2px solid #e2e8f0;
    }
    
    /* 情報ボックス */
    .stAlert {
        border-radius: 10px;
        border-left: 4px solid #667eea;
    }
    
    /* 成功メッセージ */
    .stSuccess {
        background: linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%);
        border-radius: 10px;
        padding: 1rem;
        color: #065f46;
    }
    
    /* 警告メッセージ */
    .stWarning {
        background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
        border-radius: 10px;
        padding: 1rem;
    }
    
    /* カードコンテナ */
    .card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
        margin-bottom: 1rem;
        transition: transform 0.3s ease;
    }
    
    .card:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.12);
    }
    
    /* セクションヘッダー */
    .section-header {
        font-size: 1.5rem;
        font-weight: 700;
        color: #667eea;
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 3px solid #667eea;
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
        30: "🏆 ジム神",
        15: "🧙 ジム仙人",
        10: "🥋 ジム師範代",
        7: "💪 ジムマスター",
        5: "⭐ ジムの常連さん",
        3: "🌟 ジム慣れ",
        2: "🔰 ジム初心者",
        1: "🌱 ジム練習生"
    }
    
    for days in sorted(titles.keys(), reverse=True):
        if consecutive_days >= days:
            return titles[days]
    return "❓ ジム未経験者"

# メイン画面
def main_page():
    st.markdown('<div class="main-title">💪 健康管理ダッシュボード</div>', unsafe_allow_html=True)
    
    # データ読み込み
    weight_df = fb.get_weight_data()
    gym_df = fb.get_gym_data()
    calorie_df = fb.get_calorie_data()
    settings = fb.get_user_settings()
    
    # 連続日数と称号
    consecutive_days = fb.calculate_consecutive_gym_days()
    title = get_gym_title(consecutive_days)
    
    st.markdown(
        f'<div class="gym-title">あなたは <strong>{title}</strong> です！<br>連続 {consecutive_days} 日達成 🎉</div>',
        unsafe_allow_html=True
    )
    
    # AI提案
    if len(weight_df) >= 30:
        with st.expander("🤖 今日のAIパーソナルアドバイス", expanded=True):
            predictor = HealthPredictor(weight_df, gym_df, calorie_df)
            result = predictor.get_daily_advice()
            
            st.markdown(f'<div class="card">{result["advice"]}</div>', unsafe_allow_html=True)
            
            if result['recipes']:
                st.markdown("---")
                st.markdown(f"### 🍽️ おすすめレシピ ({result['recipes']['category']})")
                
                for recipe in result['recipes']['recipes']:
                    with st.container():
                        st.markdown(f'<div class="card">', unsafe_allow_html=True)
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            st.markdown(f"**[{recipe['title']}]({recipe['url']})**")
                            st.caption(recipe['snippet'])
                        with col2:
                            st.caption(f"📍 {recipe['source']}")
                        st.markdown('</div>', unsafe_allow_html=True)
    else:
        days_left = 30 - len(weight_df)
        st.info(f"📊 AIアドバイス機能まであと **{days_left}日** です。毎日記録を続けて、パーソナライズされたアドバイスを受け取りましょう！")
    
    # 期間選択
    st.markdown('<div class="section-header">📈 データ分析</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        period = st.selectbox("📅 表示期間", ["週", "月", "年"], key="period_select")
    
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
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if not filtered_weight.empty:
            current_weight = filtered_weight.iloc[-1]['weight']
            weight_change = current_weight - filtered_weight.iloc[0]['weight']
            st.metric("⚖️ 現在の体重", f"{current_weight:.1f} kg", f"{weight_change:+.1f} kg")
        else:
            st.metric("⚖️ 現在の体重", "-- kg")
    
    with col2:
        weight_goal = settings.get('weight_goal', 70.0)
        if not filtered_weight.empty:
            diff = current_weight - weight_goal
            st.metric("🎯 目標体重", f"{weight_goal:.1f} kg", f"{diff:+.1f} kg")
        else:
            st.metric("🎯 目標体重", f"{weight_goal:.1f} kg")
    
    with col3:
        gym_count = filtered_gym['went_to_gym'].sum() if not filtered_gym.empty else 0
        st.metric("🏋️ ジム回数", f"{gym_count}回")
    
    with col4:
        avg_calories = filtered_calorie['calories'].mean() if not filtered_calorie.empty else 0
        calorie_goal = settings.get('calorie_goal', 2000)
        diff_cal = avg_calories - calorie_goal
        st.metric("🔥 平均消費カロリー", f"{avg_calories:.0f} kcal", f"{diff_cal:+.0f} kcal")
    
    # グラフ表示
    if not filtered_weight.empty:
        fig = go.Figure()
        
        # 体重ライン
        fig.add_trace(go.Scatter(
            x=filtered_weight['date'],
            y=filtered_weight['weight'],
            mode='lines+markers',
            name='体重',
            line=dict(color='#667eea', width=4),
            marker=dict(size=10, color='#667eea', line=dict(color='white', width=2)),
            hovertemplate='<b>日付</b>: %{x|%Y-%m-%d}<br><b>体重</b>: %{y:.1f} kg<extra></extra>',
            fill='tozeroy',
            fillcolor='rgba(102, 126, 234, 0.1)'
        ))
        
        # 目標体重ライン
        fig.add_trace(go.Scatter(
            x=filtered_weight['date'],
            y=[weight_goal] * len(filtered_weight),
            mode='lines',
            name='目標体重',
            line=dict(color='#f5576c', width=3, dash='dash'),
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
                    color='#4ade80',
                    symbol='star',
                    line=dict(color='#22c55e', width=2)
                ),
                hovertemplate='<b>🏋️ ジムに行った日</b><br>%{x|%Y-%m-%d}<extra></extra>'
            ))
        
        fig.update_layout(
            title=dict(
                text="📊 体重推移グラフ",
                font=dict(size=26, color='#667eea', family='Arial Black')
            ),
            xaxis_title="日付",
            yaxis_title="体重 (kg)",
            hovermode="x unified",
            height=550,
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                bgcolor='rgba(255, 255, 255, 0.8)',
                bordercolor='#667eea',
                borderwidth=2
            ),
            plot_bgcolor='rgba(248, 249, 250, 0.5)',
            paper_bgcolor='white',
            font=dict(family='Arial', size=12),
            xaxis=dict(
                showgrid=True,
                gridcolor='rgba(102, 126, 234, 0.1)',
                zeroline=False
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor='rgba(102, 126, 234, 0.1)',
                zeroline=False
            )
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
            display_df.columns = ['📅 日付', '⚖️ 体重 (kg)', '🏋️ ジム', '🔥 消費カロリー (kcal)']
            display_df = display_df.sort_values('📅 日付', ascending=False)
            
            st.dataframe(display_df, use_container_width=True, hide_index=True)
    else:
        st.info("📝 データがまだありません。データ入力画面から記録を始めましょう！")

# データ入力画面
def input_page():
    st.markdown('<div class="main-title">📝 データ入力</div>', unsafe_allow_html=True)
    
    today = datetime.now().date()
    
    st.markdown('<div class="card">', unsafe_allow_html=True)
    selected_date = st.date_input(
        "📅 日付を選択",
        value=today,
        max_value=today,
        min_value=datetime(2026, 1, 1).date()
    )
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 今日以外は編集不可
    if selected_date != today:
        st.warning("⚠️ 過去の日付は編集できません（翌0時以降）")
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
    
    st.markdown("---")
    st.markdown('<div class="section-header">📊 今日の記録</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        weight = st.number_input(
            "⚖️ 体重 (kg)",
            min_value=0.0,
            max_value=300.0,
            value=float(default_weight),
            step=0.1,
            help="今日の体重を入力してください"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        went_to_gym = st.checkbox(
            "🏋️ ジムに行った",
            value=default_gym,
            help="今日ジムに行った場合はチェック"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="card">', unsafe_allow_html=True)
    calories = st.number_input(
        "🔥 消費カロリー (kcal)",
        min_value=0,
        max_value=10000,
        value=default_calorie,
        step=50,
        help="今日の総消費カロリーを入力"
    )
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col2:
        if st.button("💾 保存する", type="primary", use_container_width=True):
            if weight > 0:
                try:
                    fb.save_weight(today, weight)
                    fb.save_gym_record(today, went_to_gym)
                    fb.save_calorie_record(today, calories)
                    st.success("✅ データを保存しました！")
                    st.balloons()
                except Exception as e:
                    st.error(f"❌ エラーが発生しました: {str(e)}")
            else:
                st.warning("⚠️ 体重を入力してください")

# 設定画面
def settings_page():
    st.markdown('<div class="main-title">⚙️ 設定</div>', unsafe_allow_html=True)
    
    settings = fb.get_user_settings()
    
    st.markdown('<div class="section-header">🎯 目標設定</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        weight_goal = st.number_input(
            "⚖️ 目標体重 (kg)",
            min_value=0.0,
            max_value=300.0,
            value=float(settings.get('weight_goal', 70.0)),
            step=0.1,
            help="達成したい目標体重を設定してください"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        calorie_goal = st.number_input(
            "🔥 目標消費カロリー (kcal)",
            min_value=0,
            max_value=10000,
            value=int(settings.get('calorie_goal', 2000)),
            step=100,
            help="1日の目標消費カロリーを設定してください"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown('<div class="section-header">🔐 セキュリティ設定</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="card">', unsafe_allow_html=True)
    new_password = st.text_input(
        "🔑 新しいパスワード",
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
                st.success("✅ 設定を保存しました！")
                st.balloons()
            except Exception as e:
                st.error(f"❌ エラーが発生しました: {str(e)}")

# メイン処理
def main():
    # サイドバーでページ選択
    with st.sidebar:
        st.markdown('<h1 style="color: white; text-align: center; margin-bottom: 2rem;">📱 メニュー</h1>', unsafe_allow_html=True)
        
        page = st.radio(
            "ページを選択",
            ["🏠 メイン画面", "📝 データ入力", "⚙️ 設定"],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        # ユーザー情報表示
        st.markdown("""
        <div style="background: rgba(255, 255, 255, 0.1); padding: 1rem; border-radius: 10px; margin-bottom: 1rem;">
            <p style="color: white; text-align: center; margin: 0;">👤 ユーザー</p>
            <p style="color: white; text-align: center; font-weight: bold; margin: 0;">やす</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🚪 ログアウト", use_container_width=True):
            logout()
        
        # フッター
        st.markdown("---")
        st.markdown("""
        <div style="color: rgba(255, 255, 255, 0.7); text-align: center; font-size: 0.8rem;">
            <p>💪 健康管理アプリ v2.0</p>
            <p>© 2026 Health Tracker</p>
        </div>
        """, unsafe_allow_html=True)
    
    if page == "🏠 メイン画面":
        main_page()
    elif page == "📝 データ入力":
        input_page()
    elif page == "⚙️ 設定":
        settings_page()

if __name__ == "__main__":
    main()

