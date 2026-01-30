import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from datetime import datetime, timedelta
from utils.recipe_searcher import RecipeSearcher

class HealthPredictor:
    def __init__(self, weight_df, gym_df, calorie_df):
        self.weight_df = weight_df
        self.gym_df = gym_df
        self.calorie_df = calorie_df
        self.recipe_searcher = RecipeSearcher()
    
    def can_predict(self):
        """30日以上のデータがあるか確認"""
        return len(self.weight_df) >= 30
    
    def get_daily_advice(self):
        """毎日のアドバイスを生成"""
        if not self.can_predict():
            return {
                'advice': "📊 30日分のデータが溜まると、AIがあなたに最適なアドバイスを提供します!",
                'recipes': None
            }
        
        # 最近7日間の傾向分析
        recent_data = self.weight_df.tail(7)
        weight_trend = recent_data['weight'].diff().mean()
        
        # ジム頻度
        recent_gym = self.gym_df.tail(7)
        gym_rate = recent_gym['went_to_gym'].sum() / 7 if not recent_gym.empty else 0
        
        # カロリー平均
        recent_calories = self.calorie_df.tail(7)
        avg_calories = recent_calories['calories'].mean() if not recent_calories.empty else 0
        
        # アドバイス生成
        advice = self._generate_advice(weight_trend, gym_rate, avg_calories)
        
        # レシピ推奨
        recipe_recommendations = self.recipe_searcher.get_recipe_recommendations(
            weight_trend, gym_rate, avg_calories
        )
        
        return {
            'advice': advice,
            'recipes': recipe_recommendations
        }
    
    def _generate_advice(self, weight_trend, gym_rate, avg_calories):
        """アドバイス生成ロジック"""
        advice_parts = []
        
        # 体重トレンド
        if weight_trend > 0.2:
            advice_parts.append("⚠️ **体重が増加傾向です**\n- 食事量を見直しましょう\n- 低カロリー・高タンパクの食事を意識")
        elif weight_trend < -0.2:
            advice_parts.append("📉 **体重が減少傾向です**\n- 良いペースです!この調子で続けましょう\n- 栄養バランスも忘れずに")
        else:
            advice_parts.append("✅ **体重は安定しています**\n- 現在の生活習慣を維持しましょう")
        
        # ジム頻度
        if gym_rate < 0.3:
            advice_parts.append("💪 **ジムの頻度を増やしましょう**\n- 週3回以上を目標に!\n- 筋肉をつけて基礎代謝アップ")
        elif gym_rate >= 0.7:
            advice_parts.append("🏆 **素晴らしいジム習慣です!**\n- 継続は力なり!\n- タンパク質をしっかり摂取しましょう")
        
        # カロリー
        if avg_calories > 800:
            advice_parts.append("🍽️ **消費カロリーが高めです**\n- このまま頑張りましょう！\n- プロテインもしっかり摂取する")
        elif avg_calories < 200:
            advice_parts.append("⚡ **消費カロリーが少なめです**\n- 適度な運動で代謝を上げましょう\n- 筋トレで筋肉量を増やす")
        
        return "\n\n".join(advice_parts)
    
    def predict_future_weight(self, days=7):
        """将来の体重予測"""
        if not self.can_predict():
            return None
        
        # 日付を数値に変換
        self.weight_df['days_since_start'] = (
            self.weight_df['date'] - self.weight_df['date'].min()
        ).dt.days
        
        X = self.weight_df['days_since_start'].values.reshape(-1, 1)
        y = self.weight_df['weight'].values
        
        # 線形回帰モデル
        model = LinearRegression()
        model.fit(X, y)
        
        # 未来の予測
        last_day = self.weight_df['days_since_start'].max()
        future_days = np.array([last_day + i for i in range(1, days + 1)]).reshape(-1, 1)
        predictions = model.predict(future_days)
        
        return predictions
