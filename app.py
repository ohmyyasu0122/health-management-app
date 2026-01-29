import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
from utils.firebase_handler import FirebaseHandler
from utils.auth import check_password, logout
from utils.ml_predictor import HealthPredictor

# ページ設定
st.set_page_config(
    page_title="健康管理アプリ",
    page_icon="💪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# カスタムCSS
st.markdown("""
<style>
    .main-title {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .gym-title {
        font-size: 1.8rem;
        color: #ff7f0e;
        text-align: center;
        padding: 1rem;
        background: linear-gradient(90deg, #f0f0f0, #ffffff);
        border-radius: 10px;
        margin-bottom: 2rem;
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
    if len(weight_df) >= 30:
        with st.expander("🤖 今日のAIアドバイス", expanded=True):
            predictor = HealthPredictor(weight_df, gym_df, calorie_df)
            result = predictor.get_daily_advice()
            
            st.markdown(result['advice'])
            
            if result['recipes']:
                st.markdown("---")
                st.markdown(f"### 🍽️ おすすめレシピ ({result['recipes']['category']})")
                
                for recipe in result['recipes']['recipes']:
                    with st.container():
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
    
    # 期間選択
    col1, col2, col3 = st.columns(3)
    with col1:
        period = st.selectbox("表示期間", ["週", "月", "年"], key="period_select")
    
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
    
    # グラフ表示
    if not filtered_weight.empty:
        fig = go.Figure()
        
        # 体重ライン
        fig.add_trace(go.Scatter(
            x=filtered_weight['date'],
            y=filtered_weight['weight'],
            mode='lines+markers',
            name='体重',
            line=dict(color='#1f77b4', width=3),
            marker=dict(size=8),
            hovertemplate='<b>日付</b>: %{x|%Y-%m-%d}<br><b>体重</b>: %{y:.1f} kg<extra></extra>'
        ))
        
        # 目標体重ライン
        fig.add_trace(go.Scatter(
            x=filtered_weight['date'],
            y=[weight_goal] * len(filtered_weight),
            mode='lines',
            name='目標体重',
            line=dict(color='red', width=2, dash='dash'),
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
                    color='green',
                    symbol='star',
                    line=dict(color='darkgreen', width=2)
                ),
                hovertemplate='<b>ジムに行った日</b><br>%{x|%Y-%m-%d}<extra></extra>'
            ))
        
        fig.update_layout(
            title=dict(
                text="体重推移グラフ",
                font=dict(size=24, color='#1f77b4')
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
            display_df.columns = ['日付', '体重 (kg)', 'ジム', '消費カロリー (kcal)']
            display_df = display_df.sort_values('日付', ascending=False)
            
            st.dataframe(display_df, use_container_width=True, hide_index=True)
    else:
        st.info("📝 データがまだありません。データ入力画面から記録を始めましょう!")

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
    
    st.markdown("---")
    
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

# 設定画面
def settings_page():
    st.title("⚙️ 設定")
    
    settings = fb.get_user_settings()
    
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
    
    st.markdown("---")
    st.markdown("### 🔐 パスワード変更")
    
    new_password = st.text_input(
        "新しいパスワード",
        type="password",
        help="パスワードを変更する場合は入力してください"
    )
    
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
