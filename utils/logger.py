"""
ログ管理モジュール
アプリケーション全体のログ記録とエラーハンドリングを管理する
"""

import logging
import streamlit as st
from datetime import datetime
from typing import Dict, Any, Optional
import traceback
import json
import os

class StreamlitLogger:
    """Streamlit用のログ管理クラス"""
    
    def __init__(self, name: str = "ISOP"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        
        # ハンドラーの設定
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
        
        # セッションログの初期化
        if 'app_logs' not in st.session_state:
            st.session_state['app_logs'] = []
    
    def log_info(self, message: str, context: Dict[str, Any] = None):
        """情報ログを記録"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'level': 'INFO',
            'message': message,
            'context': context or {}
        }
        
        self.logger.info(message)
        st.session_state['app_logs'].append(log_entry)
    
    def log_warning(self, message: str, context: Dict[str, Any] = None):
        """警告ログを記録"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'level': 'WARNING',
            'message': message,
            'context': context or {}
        }
        
        self.logger.warning(message)
        st.session_state['app_logs'].append(log_entry)
    
    def log_error(self, message: str, error: Exception = None, context: Dict[str, Any] = None):
        """エラーログを記録"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'level': 'ERROR',
            'message': message,
            'error_type': type(error).__name__ if error else None,
            'error_message': str(error) if error else None,
            'traceback': traceback.format_exc() if error else None,
            'context': context or {}
        }
        
        self.logger.error(f"{message}: {error}" if error else message)
        st.session_state['app_logs'].append(log_entry)
    
    def log_processing_step(self, step: str, status: str, details: Dict[str, Any] = None):
        """処理ステップのログを記録"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'level': 'INFO',
            'message': f"処理ステップ: {step} - {status}",
            'step': step,
            'status': status,
            'details': details or {}
        }
        
        self.logger.info(f"処理ステップ: {step} - {status}")
        st.session_state['app_logs'].append(log_entry)
    
    def get_logs(self, level: Optional[str] = None, limit: int = 100) -> list:
        """ログを取得"""
        logs = st.session_state.get('app_logs', [])
        
        if level:
            logs = [log for log in logs if log['level'] == level.upper()]
        
        return logs[-limit:] if limit else logs
    
    def clear_logs(self):
        """ログをクリア"""
        st.session_state['app_logs'] = []
    
    def export_logs(self, format: str = 'json') -> str:
        """ログをエクスポート"""
        logs = self.get_logs()
        
        if format == 'json':
            return json.dumps(logs, indent=2, ensure_ascii=False)
        elif format == 'text':
            text_logs = []
            for log in logs:
                text_logs.append(f"[{log['timestamp']}] {log['level']}: {log['message']}")
            return '\n'.join(text_logs)
        else:
            raise ValueError(f"Unsupported format: {format}")

def create_log_display():
    """ログ表示インターフェースを作成"""
    st.subheader("📋 アプリケーションログ")
    
    # ログレベルフィルター
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        log_level = st.selectbox(
            "ログレベル",
            ["ALL", "INFO", "WARNING", "ERROR"],
            index=0
        )
    
    with col2:
        log_limit = st.number_input("表示件数", min_value=10, max_value=500, value=100, step=10)
    
    with col3:
        if st.button("🗑️ ログクリア"):
            if 'app_logs' in st.session_state:
                st.session_state['app_logs'] = []
                st.success("ログがクリアされました")
                st.rerun()
    
    # ログの表示
    logs = st.session_state.get('app_logs', [])
    
    if log_level != "ALL":
        logs = [log for log in logs if log['level'] == log_level]
    
    logs = logs[-log_limit:] if log_limit else logs
    
    if logs:
        # ログテーブルの表示
        log_data = []
        for log in logs:
            log_data.append({
                '時刻': log['timestamp'][:19],  # ISO形式から時刻部分のみ
                'レベル': log['level'],
                'メッセージ': log['message'][:100] + "..." if len(log['message']) > 100 else log['message']
            })
        
        st.dataframe(log_data, use_container_width=True)
        
        # 詳細ログの表示
        if st.checkbox("詳細ログを表示"):
            for log in logs:
                with st.expander(f"{log['timestamp'][:19]} - {log['level']} - {log['message']}"):
                    st.json(log)
    else:
        st.info("ログがありません。")

def log_function_call(func_name: str, args: Dict[str, Any] = None, result: Any = None, error: Exception = None):
    """関数呼び出しをログに記録"""
    logger = StreamlitLogger()
    
    context = {
        'function': func_name,
        'args': args or {},
        'result': str(result) if result else None,
        'success': error is None
    }
    
    if error:
        logger.log_error(f"関数 {func_name} の実行中にエラーが発生", error, context)
    else:
        logger.log_info(f"関数 {func_name} が正常に実行されました", context)

def log_file_operation(operation: str, file_name: str, file_size: int = None, success: bool = True, error: Exception = None):
    """ファイル操作をログに記録"""
    logger = StreamlitLogger()
    
    context = {
        'operation': operation,
        'file_name': file_name,
        'file_size': file_size,
        'success': success
    }
    
    if error:
        logger.log_error(f"ファイル操作 {operation} でエラーが発生: {file_name}", error, context)
    else:
        logger.log_info(f"ファイル操作 {operation} が完了: {file_name}", context)

def log_ai_operation(operation: str, model: str = None, tokens_used: int = None, success: bool = True, error: Exception = None):
    """AI操作をログに記録"""
    logger = StreamlitLogger()
    
    context = {
        'operation': operation,
        'model': model,
        'tokens_used': tokens_used,
        'success': success
    }
    
    if error:
        logger.log_error(f"AI操作 {operation} でエラーが発生", error, context)
    else:
        logger.log_info(f"AI操作 {operation} が完了", context)

# グローバルロガーインスタンス
app_logger = StreamlitLogger("ISOP")
