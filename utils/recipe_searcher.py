import streamlit as st
from googleapiclient.discovery import build
from typing import List, Dict

class RecipeSearcher:
    def __init__(self):
        if 'google_search' in st.secrets:
            self.api_key = st.secrets['google_search']['api_key']
            self.search_engine_id = st.secrets['google_search']['search_engine_id']
            try:
                self.service = build("customsearch", "v1", developerKey=self.api_key)
            except Exception as e:
                st.warning(f"Google Search API初期化エラー: {str(e)}")
                self.service = None
        else:
            self.api_key = None
            self.service = None
    
    def search_recipes(self, query: str, num_results: int = 5) -> List[Dict]:
        """
        レシピを検索
        
        Args:
            query: 検索クエリ (例: "高タンパク 低カロリー レシピ")
            num_results: 取得する結果数
        
        Returns:
            レシピ情報のリスト
        """
        if not self.service:
            return self._get_fallback_recipes(query)
        
        try:
            # Google Custom Search実行
            result = self.service.cse().list(
                q=query,
                cx=self.search_engine_id,
                num=num_results,
                lr='lang_ja',
                safe='active'
            ).execute()
            
            recipes = []
            
            if 'items' in result:
                for item in result['items']:
                    recipe = {
                        'title': item.get('title', ''),
                        'url': item.get('link', ''),
                        'snippet': item.get('snippet', ''),
                        'source': self._extract_source(item.get('link', ''))
                    }
                    
                    # サムネイル画像があれば追加
                    if 'pagemap' in item and 'cse_image' in item['pagemap']:
                        recipe['image'] = item['pagemap']['cse_image'][0].get('src', '')
                    
                    recipes.append(recipe)
            
            return recipes
        
        except Exception as e:
            st.warning(f"検索エラー: {str(e)}")
            return self._get_fallback_recipes(query)
    
    def _extract_source(self, url: str) -> str:
        """URLからサイト名を抽出"""
        if 'cookpad.com' in url:
            return 'クックパッド'
        elif 'kurashiru.com' in url:
            return 'クラシル'
        elif 'delishkitchen.tv' in url:
            return 'デリッシュキッチン'
        elif 'erecipe.woman.excite.co.jp' in url:
            return 'E・レシピ'
        else:
            return 'その他'
    
    def _get_fallback_recipes(self, query: str) -> List[Dict]:
        """API利用不可時のフォールバック"""
        fallback_recipes = {
            '高タンパク': [
                {
                    'title': '鶏胸肉のグリル - クックパッド',
                    'url': 'https://cookpad.com/search/%E9%B6%8F%E8%83%B8%E8%82%89%20%E3%82%B0%E3%83%AA%E3%83%AB',
                    'snippet': '高タンパク・低脂質の鶏胸肉を使った簡単レシピ',
                    'source': 'クックパッド'
                },
                {
                    'title': 'サーモンのソテー - クラシル',
                    'url': 'https://www.kurashiru.com/search?query=%E3%82%B5%E3%83%BC%E3%83%A2%E3%83%B3%20%E3%82%BD%E3%83%86%E3%83%BC',
                    'snippet': 'オメガ3脂肪酸豊富なサーモンレシピ',
                    'source': 'クラシル'
                }
            ],
            '低カロリー': [
                {
                    'title': '豆腐ハンバーグ - デリッシュキッチン',
                    'url': 'https://delishkitchen.tv/search?q=%E8%B1%86%E8%85%90%E3%83%8F%E3%83%B3%E3%83%90%E3%83%BC%E3%82%B0',
                    'snippet': 'ヘルシーで満足感のある豆腐ハンバーグ',
                    'source': 'デリッシュキッチン'
                },
                {
                    'title': '野菜たっぷりスープ - E・レシピ',
                    'url': 'https://erecipe.woman.excite.co.jp/search/?keyword=%E9%87%8E%E8%8F%9C%E3%82%B9%E3%83%BC%E3%83%97',
                    'snippet': '栄養満点の野菜スープレシピ',
                    'source': 'E・レシピ'
                }
            ]
        }
        
        # クエリに応じてレシピを返す
        for key in fallback_recipes:
            if key in query:
                return fallback_recipes[key]
        
        return fallback_recipes['高タンパク']
    
    def get_recipe_recommendations(self, weight_trend: float, gym_rate: float, 
                                   avg_calories: float) -> Dict:
        """
        ユーザーの状態に基づいてレシピを推奨
        
        Args:
            weight_trend: 体重の変化傾向
            gym_rate: ジムに行く頻度 (0-1)
            avg_calories: 平均消費カロリー
        
        Returns:
            推奨レシピ情報
        """
        # 検索クエリの生成
        if weight_trend > 0.2:
            query = "低カロリー 高タンパク ダイエット レシピ"
            category = "体重管理"
        elif gym_rate >= 0.5:
            query = "高タンパク 筋トレ 食事 レシピ"
            category = "筋肉増強"
        elif avg_calories < 200:
            query = "代謝アップ バランス 栄養 レシピ"
            category = "代謝改善"
        else:
            query = "バランス 健康 簡単 レシピ"
            category = "健康維持"
        
        recipes = self.search_recipes(query, num_results=5)
        
        return {
            'category': category,
            'query': query,
            'recipes': recipes
        }
