import firebase_admin
from firebase_admin import credentials, firestore
import streamlit as st
from datetime import datetime, timedelta
import pandas as pd

class FirebaseHandler:
    def __init__(self):
        if not firebase_admin._apps:
            # Streamlit Cloudの場合
            if 'firebase' in st.secrets:
                cred = credentials.Certificate(dict(st.secrets['firebase']))
            else:
                # ローカル開発の場合
                cred = credentials.Certificate('firebase-key.json')
            
            firebase_admin.initialize_app(cred)
        
        self.db = firestore.client()
    
    # ユーザー設定
    def get_user_settings(self):
        doc = self.db.collection('settings').document('user_config').get()
        if doc.exists:
            return doc.to_dict()
        else:
            # デフォルト設定
            default_settings = {
                'password': 'yasu0122',
                'calorie_goal': 2000,
                'weight_goal': 70.0
            }
            self.db.collection('settings').document('user_config').set(default_settings)
            return default_settings
    
    def update_user_settings(self, settings):
        self.db.collection('settings').document('user_config').set(settings)
    
    # 体重データ
    def save_weight(self, date, weight):
        date_str = date.strftime('%Y-%m-%d')
        self.db.collection('weight').document(date_str).set({
            'date': date_str,
            'weight': weight,
            'timestamp': firestore.SERVER_TIMESTAMP
        }, merge=True)
    
    def get_weight_data(self, start_date=None, end_date=None):
        query = self.db.collection('weight').order_by('date')
        
        if start_date:
            query = query.where('date', '>=', start_date.strftime('%Y-%m-%d'))
        if end_date:
            query = query.where('date', '<=', end_date.strftime('%Y-%m-%d'))
        
        docs = query.stream()
        data = [{'date': doc.id, 'weight': doc.to_dict()['weight']} for doc in docs]
        
        if not data:
            return pd.DataFrame(columns=['date', 'weight'])
        
        df = pd.DataFrame(data)
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date')
        
        # 未入力日を前日の値で埋める
        df = self._fill_missing_dates(df)
        
        return df
    
    def _fill_missing_dates(self, df):
        if df.empty:
            return df
        
        # 日付範囲を作成
        date_range = pd.date_range(start=df['date'].min(), end=datetime.now().date(), freq='D')
        full_df = pd.DataFrame({'date': date_range})
        
        # マージして前方埋め
        merged = full_df.merge(df, on='date', how='left')
        merged['weight'] = merged['weight'].ffill()
        
        return merged.dropna()
    
    # ジムデータ
    def save_gym_record(self, date, went_to_gym):
        date_str = date.strftime('%Y-%m-%d')
        self.db.collection('gym').document(date_str).set({
            'date': date_str,
            'went_to_gym': went_to_gym,
            'timestamp': firestore.SERVER_TIMESTAMP
        }, merge=True)
    
    def get_gym_data(self, start_date=None, end_date=None):
        query = self.db.collection('gym').order_by('date')
        
        if start_date:
            query = query.where('date', '>=', start_date.strftime('%Y-%m-%d'))
        if end_date:
            query = query.where('date', '<=', end_date.strftime('%Y-%m-%d'))
        
        docs = query.stream()
        data = [{'date': doc.id, 'went_to_gym': doc.to_dict()['went_to_gym']} for doc in docs]
        
        if not data:
            return pd.DataFrame(columns=['date', 'went_to_gym'])
        
        df = pd.DataFrame(data)
        df['date'] = pd.to_datetime(df['date'])
        return df.sort_values('date')
    
    # カロリーデータ
    def save_calorie_record(self, date, calories):
        date_str = date.strftime('%Y-%m-%d')
        self.db.collection('calories').document(date_str).set({
            'date': date_str,
            'calories': calories,
            'timestamp': firestore.SERVER_TIMESTAMP
        }, merge=True)
    
    def get_calorie_data(self, start_date=None, end_date=None):
        query = self.db.collection('calories').order_by('date')
        
        if start_date:
            query = query.where('date', '>=', start_date.strftime('%Y-%m-%d'))
        if end_date:
            query = query.where('date', '<=', end_date.strftime('%Y-%m-%d'))
        
        docs = query.stream()
        data = [{'date': doc.id, 'calories': doc.to_dict()['calories']} for doc in docs]
        
        if not data:
            return pd.DataFrame(columns=['date', 'calories'])
        
        df = pd.DataFrame(data)
        df['date'] = pd.to_datetime(df['date'])
        return df.sort_values('date')
    
    # 連続ジム日数計算
    def calculate_consecutive_gym_days(self):
        gym_df = self.get_gym_data()
        
        if gym_df.empty:
            return 0
        
        gym_df = gym_df.sort_values('date', ascending=False)
        consecutive = 0
        current_date = datetime.now().date()
        
        for _, row in gym_df.iterrows():
            row_date = row['date'].date()
            
            # 連続性をチェック
            if (current_date - row_date).days == consecutive and row['went_to_gym']:
                consecutive += 1
            else:
                break
        
        return consecutive
