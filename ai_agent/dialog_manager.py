"""
AI対話管理モジュール
ユーザーとの対話を管理し、AIからの質問とユーザーの回答を処理する
"""

import streamlit as st
from typing import Dict, List, Optional, Tuple
import json
import uuid
from datetime import datetime

class DialogManager:
    """AI対話を管理するクラス"""
    
    def __init__(self):
        self.dialogs = {}
        self.current_dialog_id = None
    
    def start_new_dialog(self, context: str = "") -> str:
        """新しい対話を開始する"""
        dialog_id = str(uuid.uuid4())
        self.dialogs[dialog_id] = {
            'id': dialog_id,
            'context': context,
            'messages': [],
            'status': 'active',
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }
        self.current_dialog_id = dialog_id
        return dialog_id
    
    def add_ai_message(self, dialog_id: str, message: str, question_type: str = "general") -> None:
        """AIからのメッセージを追加する"""
        if dialog_id not in self.dialogs:
            raise ValueError(f"Dialog {dialog_id} not found")
        
        message_obj = {
            'id': str(uuid.uuid4()),
            'sender': 'ai',
            'message': message,
            'question_type': question_type,
            'timestamp': datetime.now().isoformat(),
            'requires_response': True
        }
        
        self.dialogs[dialog_id]['messages'].append(message_obj)
        self.dialogs[dialog_id]['updated_at'] = datetime.now().isoformat()
    
    def add_user_message(self, dialog_id: str, message: str) -> None:
        """ユーザーからのメッセージを追加する"""
        if dialog_id not in self.dialogs:
            raise ValueError(f"Dialog {dialog_id} not found")
        
        message_obj = {
            'id': str(uuid.uuid4()),
            'sender': 'user',
            'message': message,
            'timestamp': datetime.now().isoformat()
        }
        
        self.dialogs[dialog_id]['messages'].append(message_obj)
        self.dialogs[dialog_id]['updated_at'] = datetime.now().isoformat()
    
    def get_latest_ai_question(self, dialog_id: str) -> Optional[Dict]:
        """最新のAI質問を取得する"""
        if dialog_id not in self.dialogs:
            return None
        
        messages = self.dialogs[dialog_id]['messages']
        for message in reversed(messages):
            if message['sender'] == 'ai' and message.get('requires_response', False):
                return message
        
        return None
    
    def get_dialog_history(self, dialog_id: str) -> List[Dict]:
        """対話履歴を取得する"""
        if dialog_id not in self.dialogs:
            return []
        
        return self.dialogs[dialog_id]['messages']
    
    def close_dialog(self, dialog_id: str) -> None:
        """対話を終了する"""
        if dialog_id in self.dialogs:
            self.dialogs[dialog_id]['status'] = 'closed'
            self.dialogs[dialog_id]['updated_at'] = datetime.now().isoformat()

def create_dialog_interface(dialog_manager: DialogManager, dialog_id: str):
    """Streamlitで対話インターフェースを作成する"""
    
    # 対話履歴の表示
    st.subheader("💬 AI対話")
    
    # 対話履歴を表示
    messages = dialog_manager.get_dialog_history(dialog_id)
    
    if messages:
        st.markdown("### 対話履歴")
        for message in messages:
            if message['sender'] == 'ai':
                st.info(f"🤖 AI: {message['message']}")
            else:
                st.success(f"👤 ユーザー: {message['message']}")
    
    # 最新のAI質問を取得
    latest_question = dialog_manager.get_latest_ai_question(dialog_id)
    
    if latest_question:
        st.markdown("### 現在の質問")
        st.warning(f"🤖 AI: {latest_question['message']}")
        
        # ユーザー回答フォーム
        with st.form("user_response_form"):
            user_response = st.text_area("回答を入力してください", height=100)
            submitted = st.form_submit_button("回答を送信")
            
            if submitted and user_response.strip():
                dialog_manager.add_user_message(dialog_id, user_response)
                st.success("回答が送信されました")
                st.rerun()
    else:
        st.info("現在、AIからの質問はありません。")

def generate_ai_questions_for_document_update(existing_doc_text: str, new_standard_text: str) -> List[str]:
    """書類更新に必要なAI質問を生成する"""
    
    questions = [
        "新しい規格で追加された主要な要件は何ですか？",
        "既存の書類で削除または変更が必要な部分はありますか？",
        "組織の特定の業務プロセスに関連する変更はありますか？",
        "新しい規格で要求される追加の手順や手続きはありますか？",
        "既存の責任者や担当者の役割に変更はありますか？",
        "新しい規格で要求される追加の文書や記録はありますか？",
        "組織の規模や特性に応じた除外事項はありますか？",
        "新しい規格で要求される追加の監査や評価はありますか？"
    ]
    
    return questions

def create_question_interface(questions: List[str], dialog_manager: DialogManager, dialog_id: str):
    """質問インターフェースを作成する"""
    
    st.subheader("❓ AIからの質問")
    
    # 質問の選択
    selected_question = st.selectbox(
        "回答したい質問を選択してください",
        questions,
        format_func=lambda x: x[:50] + "..." if len(x) > 50 else x
    )
    
    if selected_question:
        st.markdown(f"**質問**: {selected_question}")
        
        # 回答フォーム
        with st.form("question_response_form"):
            response = st.text_area("回答を入力してください", height=150)
            submitted = st.form_submit_button("回答を送信")
            
            if submitted and response.strip():
                # AI質問を追加
                dialog_manager.add_ai_message(dialog_id, selected_question, "document_update")
                # ユーザー回答を追加
                dialog_manager.add_user_message(dialog_id, response)
                st.success("回答が記録されました")
                st.rerun()

def save_dialog_to_session(dialog_manager: DialogManager, dialog_id: str):
    """対話をセッションに保存する"""
    if dialog_id in dialog_manager.dialogs:
        st.session_state['current_dialog'] = dialog_manager.dialogs[dialog_id]

def load_dialog_from_session(dialog_manager: DialogManager) -> Optional[str]:
    """セッションから対話を読み込む"""
    if 'current_dialog' in st.session_state:
        dialog_data = st.session_state['current_dialog']
        dialog_id = dialog_data['id']
        dialog_manager.dialogs[dialog_id] = dialog_data
        return dialog_id
    return None
