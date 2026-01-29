import streamlit as st
from utils.firebase_handler import FirebaseHandler

def check_password():
    """パスワード認証"""
    
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    
    if st.session_state.authenticated:
        return True
    
    # Firebase設定取得
    fb = FirebaseHandler()
    settings = fb.get_user_settings()
    correct_password = settings.get('password', 'yasu0122')
    
    st.title("🔐 ログイン")
    
    password = st.text_input("パスワードを入力してください", type="password", key="password_input")
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col2:
        if st.button("ログイン", type="primary", use_container_width=True):
            if password == correct_password:
                st.session_state.authenticated = True
                st.success("✅ ログイン成功!")
                st.rerun()
            else:
                st.error("❌ パスワードが間違っています")
    
    return False

def logout():
    """ログアウト"""
    st.session_state.authenticated = False
    st.rerun()
