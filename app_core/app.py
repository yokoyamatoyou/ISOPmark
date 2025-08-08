import streamlit as st
import os
from pathlib import Path
from datetime import datetime

from document_processor.extractor import extract_text
from utils.helpers import validate_file_type

# ページ設定
st.set_page_config(
    page_title="ISOP - 規格対応書類更新AIエージェント",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    # サイドバーの設定
    with st.sidebar:
        st.title("📋 ISOP")
        st.markdown("---")
        
        # ナビゲーションメニュー
        page = st.selectbox(
            "メニュー",
            ["🏠 ホーム", "📄 書類アップロード", "🤖 AI処理", "📊 差分レポート", "📦 バッチ処理", "📋 テンプレート", "⚙️ 設定"]
        )
        
        st.markdown("---")
        
        # 処理状況の表示
        if 'processing_status' in st.session_state:
            st.info(f"処理状況: {st.session_state['processing_status']}")
        
        # 環境変数の確認
        if not os.getenv('OPENAI_API_KEY'):
            st.error("⚠️ OpenAI APIキーが設定されていません")
        else:
            st.success("✅ OpenAI APIキーが設定されています")
            
        if not os.getenv('CHROMA_DB_PATH'):
            st.warning("⚠️ ChromaDBパスが設定されていません（デフォルト使用）")

    # メインページの内容
    if page == "🏠 ホーム":
        show_home_page()
    elif page == "📄 書類アップロード":
        show_upload_page()
    elif page == "🤖 AI処理":
        show_ai_processing_page()
    elif page == "📊 差分レポート":
        show_diff_report_page()
    elif page == "📦 バッチ処理":
        show_batch_processing_page()
    elif page == "📋 テンプレート":
        show_template_page()
    elif page == "⚙️ 設定":
        show_settings_page()

def show_home_page():
    """ホームページの表示"""
    st.title("🏠 ISOP - 規格対応書類更新AIエージェント")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ## ようこそ！
        
        このアプリケーションは、ISOやプライバシーマークなどの規格文書の更新を支援するAIエージェントです。
        
        ### 主な機能
        - 📄 **書類アップロード**: 既存の規格関連書類と新規格内容をアップロード
        - 🤖 **AI処理**: AIによる自動書類書き換えと対話型修正
        - 📊 **差分レポート**: 変更前後の差分を可視化
        - ⚙️ **設定**: システム設定の管理
        
        ### 対応規格
        - ISO 27001（情報セキュリティマネジメント）
        - ISO 9001（品質マネジメント）
        - プライバシーマーク
        - その他の規格対応も可能
        """)
    
    with col2:
        st.info("""
        **🚀 クイックスタート**
        
        1. 「📄 書類アップロード」で既存書類をアップロード
        2. 新規格内容をアップロード
        3. 「🤖 AI処理」で自動更新を実行
        4. 「📊 差分レポート」で変更内容を確認
        5. 「📦 バッチ処理」で複数書類を一括処理
        6. 「📋 テンプレート」で規格別テンプレートを使用
        """)
        
        if st.button("📄 書類アップロードを開始", type="primary"):
            st.switch_page("📄 書類アップロード")

def show_upload_page():
    """書類アップロードページの表示"""
    st.title("📄 書類アップロード")
    
    # タブ分け
    tab1, tab2, tab3 = st.tabs(["📋 既存書類", "🆕 新規格内容", "📁 アップロード履歴"])
    
    with tab1:
        st.header("既存の規格関連書類")
        st.markdown("更新対象となる既存の規格関連書類をアップロードしてください。")
        
        existing_doc = st.file_uploader(
            "既存書類をアップロード (PDF, DOCX, TXT)",
            type=['pdf', 'docx', 'txt'],
            key="existing_doc"
        )
        
        if existing_doc:
            st.success(f"✅ {existing_doc.name} がアップロードされました")
            
            # ファイル情報の表示
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("ファイルサイズ", f"{existing_doc.size / 1024:.1f} KB")
            with col2:
                st.metric("ファイル形式", existing_doc.type.upper())
            with col3:
                st.metric("アップロード時刻", "現在")
            
            # プレビュー機能
            if st.checkbox("📄 ファイル内容をプレビュー"):
                try:
                    content = existing_doc.getvalue()
                    text = extract_text(content, existing_doc.type)
                    st.text_area("ファイル内容", text, height=200)
                except Exception as e:
                    st.error(f"プレビューの生成に失敗しました: {e}")
    
    with tab2:
        st.header("新規格内容")
        st.markdown("更新された規格内容の書類をアップロードしてください。")
        
        new_standard_doc = st.file_uploader(
            "新規格内容をアップロード (PDF, TXT)",
            type=['pdf', 'txt'],
            key="new_standard_doc"
        )
        
        if new_standard_doc:
            st.success(f"✅ {new_standard_doc.name} がアップロードされました")
            
            # ファイル情報の表示
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("ファイルサイズ", f"{new_standard_doc.size / 1024:.1f} KB")
            with col2:
                st.metric("ファイル形式", new_standard_doc.type.upper())
            with col3:
                st.metric("アップロード時刻", "現在")
            
            # プレビュー機能
            if st.checkbox("📄 新規格内容をプレビュー", key="preview_new"):
                try:
                    content = new_standard_doc.getvalue()
                    text = extract_text(content, new_standard_doc.type)
                    st.text_area("新規格内容", text, height=200)
                except Exception as e:
                    st.error(f"プレビューの生成に失敗しました: {e}")
    
    with tab3:
        st.header("アップロード履歴")
        st.info("アップロード履歴機能は開発中です。")
    
    # 処理開始ボタン
    if 'existing_doc' in st.session_state and 'new_standard_doc' in st.session_state:
        if st.session_state.existing_doc and st.session_state.new_standard_doc:
            st.markdown("---")
            if st.button("🚀 AI処理を開始", type="primary", use_container_width=True):
                st.session_state['processing_status'] = "書類解析中..."
                st.switch_page("🤖 AI処理")

def show_ai_processing_page():
    """AI処理ページの表示"""
    st.title("🤖 AI処理")
    
    # 処理ステップの表示
    steps = ["📄 書類解析", "🔍 ベクトル化", "🤖 AI書き換え", "📊 差分生成"]
    current_step = st.session_state.get('current_step', 0)
    
    # プログレスバー
    progress = st.progress(current_step / len(steps))
    
    # ステップ表示
    cols = st.columns(len(steps))
    for i, (col, step) in enumerate(zip(cols, steps)):
        if i <= current_step:
            col.success(step)
        else:
            col.info(step)
    
    st.markdown("---")
    
    # タブ分け
    tab1, tab2, tab3 = st.tabs(["🔄 処理実行", "💬 AI対話", "📋 処理ログ"])
    
    with tab1:
        st.header("処理実行")
        
        if st.button("🚀 処理を開始", type="primary"):
            try:
                # ステップ1: 書類解析
                st.session_state['current_step'] = 0
                st.session_state['processing_status'] = "書類解析中..."
                
                with st.spinner("書類からテキストを抽出しています..."):
                    # 既存書類の処理
                    existing_doc = st.session_state.get('existing_doc')
                    new_standard_doc = st.session_state.get('new_standard_doc')
                    
                    if existing_doc and new_standard_doc:
                        try:
                            from utils.logger import app_logger, log_file_operation
                            
                            existing_doc_content = existing_doc.getvalue()
                            new_standard_doc_content = new_standard_doc.getvalue()
                            
                            # ログ記録
                            log_file_operation("upload", existing_doc.name, existing_doc.size)
                            log_file_operation("upload", new_standard_doc.name, new_standard_doc.size)
                            
                            existing_doc_text = extract_text(existing_doc_content, existing_doc.type)
                            new_standard_doc_text = extract_text(new_standard_doc_content, new_standard_doc.type)
                            
                            st.session_state['existing_doc_text'] = existing_doc_text
                            st.session_state['new_standard_doc_text'] = new_standard_doc_text
                            
                            app_logger.log_processing_step("テキスト抽出", "完了", {
                                'existing_doc_size': len(existing_doc_text),
                                'new_standard_doc_size': len(new_standard_doc_text)
                            })
                            
                            st.success("✅ テキスト抽出が完了しました")
                            
                        except Exception as e:
                            app_logger.log_error("テキスト抽出中にエラーが発生", e)
                            st.error(f"テキスト抽出中にエラーが発生しました: {e}")
                            return
                
                # ステップ2: ベクトル化
                st.session_state['current_step'] = 1
                st.session_state['processing_status'] = "ベクトル化中..."
                
                with st.spinner("既存書類のベクトル化とデータベースへの保存を実行中..."):
                    try:
                        from services.document_service import process_and_store_document
                        
                        doc_id, num_chunks = process_and_store_document(
                            file_content=existing_doc_content,
                            file_type=existing_doc.type,
                            document_name=existing_doc.name
                        )
                        
                        if doc_id:
                            st.session_state['existing_doc_id'] = doc_id
                            app_logger.log_processing_step("ベクトル化", "完了", {
                                'doc_id': doc_id,
                                'num_chunks': num_chunks
                            })
                            st.success(f"✅ ベクトル化が完了しました（{num_chunks}個のチャンク）")
                        else:
                            app_logger.log_error("ベクトル化処理に失敗", context={'doc_name': existing_doc.name})
                            st.error("ベクトル化処理に失敗しました")
                            return
                            
                    except Exception as e:
                        app_logger.log_error("ベクトル化処理中にエラーが発生", e)
                        st.error(f"ベクトル化処理中にエラーが発生しました: {e}")
                        return
                
                # ステップ3: AI書き換え
                st.session_state['current_step'] = 2
                st.session_state['processing_status'] = "AI書き換え中..."
                
                with st.spinner("AIが書類を書き換えています...（数分かかることがあります）"):
                    try:
                        from ai_agent.rag import rewrite_document_with_rag
                        from utils.logger import log_ai_operation
                        
                        rewritten_doc = rewrite_document_with_rag(
                            existing_doc_id=st.session_state['existing_doc_id'],
                            new_standard_text=st.session_state['new_standard_doc_text']
                        )
                        
                        st.session_state['rewritten_doc'] = rewritten_doc
                        log_ai_operation("書類書き換え", "gpt-4o-mini", success=True)
                        app_logger.log_processing_step("AI書き換え", "完了", {
                            'rewritten_doc_size': len(rewritten_doc)
                        })
                        st.success("✅ AI書き換えが完了しました")
                        
                    except Exception as e:
                        log_ai_operation("書類書き換え", "gpt-4o-mini", success=False, error=e)
                        app_logger.log_error("AI書き換え中にエラーが発生", e)
                        st.error(f"AI書き換え中にエラーが発生しました: {e}")
                        return
                
                # ステップ4: 差分生成
                st.session_state['current_step'] = 3
                st.session_state['processing_status'] = "差分生成中..."
                
                with st.spinner("差分レポートを生成中..."):
                    try:
                        from diff_generator.generator import generate_diff_report
                        
                        original_text = st.session_state.get('existing_doc_text', '')
                        diff_report_md = generate_diff_report(original_text, rewritten_doc, format='markdown')
                        
                        st.session_state['diff_report_md'] = diff_report_md
                        app_logger.log_processing_step("差分生成", "完了", {
                            'original_size': len(original_text),
                            'rewritten_size': len(rewritten_doc),
                            'diff_report_size': len(diff_report_md)
                        })
                        st.success("✅ 差分レポートの生成が完了しました")
                        
                    except Exception as e:
                        app_logger.log_error("差分生成中にエラーが発生", e)
                        st.error(f"差分生成中にエラーが発生しました: {e}")
                        return
                
                st.session_state['processing_status'] = "完了"
                st.balloons()
                
            except Exception as e:
                st.error(f"処理中にエラーが発生しました: {e}")
                st.session_state['processing_status'] = "エラー"
    
    with tab2:
        st.header("AI対話")
        
        # 対話管理の初期化
        from ai_agent.dialog_manager import DialogManager, create_dialog_interface, generate_ai_questions_for_document_update, create_question_interface
        
        if 'dialog_manager' not in st.session_state:
            st.session_state['dialog_manager'] = DialogManager()
        
        dialog_manager = st.session_state['dialog_manager']
        
        # 新しい対話を開始するかチェック
        if st.button("🆕 新しい対話を開始", type="primary"):
            dialog_id = dialog_manager.start_new_dialog("書類更新プロセス")
            st.session_state['current_dialog_id'] = dialog_id
            st.success("新しい対話が開始されました")
            st.rerun()
        
        # 現在の対話IDを取得
        current_dialog_id = st.session_state.get('current_dialog_id')
        
        if current_dialog_id:
            # 対話インターフェースを表示
            create_dialog_interface(dialog_manager, current_dialog_id)
            
            st.markdown("---")
            
            # 書類更新に関する質問を生成
            if 'existing_doc_text' in st.session_state and 'new_standard_doc_text' in st.session_state:
                questions = generate_ai_questions_for_document_update(
                    st.session_state['existing_doc_text'],
                    st.session_state['new_standard_doc_text']
                )
                
                create_question_interface(questions, dialog_manager, current_dialog_id)
        else:
            st.info("対話を開始するには「新しい対話を開始」ボタンをクリックしてください。")
    
    with tab3:
        st.header("処理ログ")
        
        # ログ表示機能を統合
        from utils.logger import create_log_display
        
        create_log_display()

def show_diff_report_page():
    """差分レポートページの表示"""
    st.title("📊 差分レポート")
    
    if 'diff_report_md' in st.session_state:
        st.markdown("## 差分レポート")
        st.markdown(st.session_state['diff_report_md'])
        
        # ダウンロードボタン
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📄 差分レポートをダウンロード", type="primary"):
                st.download_button(
                    label="📄 差分レポートをダウンロード",
                    data=st.session_state['diff_report_md'],
                    file_name="diff_report.md",
                    mime="text/markdown"
                )
        
        with col2:
            if 'rewritten_doc' in st.session_state:
                st.download_button(
                    label="📄 新書類をダウンロード",
                    data=st.session_state['rewritten_doc'],
                    file_name="updated_document.md",
                    mime="text/markdown"
                )
    else:
        st.info("差分レポートがありません。AI処理を実行してください。")

def show_settings_page():
    """設定ページの表示"""
    st.title("⚙️ 設定")
    
    # タブ分け
    tab1, tab2, tab3 = st.tabs(["🔑 API設定", "🗄️ データベース設定", "📊 システム情報"])
    
    with tab1:
        st.header("API設定")
        
        # OpenAI API設定
        st.subheader("OpenAI API設定")
        api_key = st.text_input("OpenAI API Key", type="password", value=os.getenv('OPENAI_API_KEY', ''))
        if st.button("API Keyを設定"):
            os.environ['OPENAI_API_KEY'] = api_key
            st.success("API Keyが設定されました")
        
        # モデル設定
        st.subheader("AIモデル設定")
        model = st.selectbox("使用するモデル", ["gpt-5-mini-2025-08-07", "gpt-4o-mini", "gpt-4", "gpt-3.5-turbo"])
        temperature = st.slider("Temperature", 0.0, 1.0, 0.7, 0.1)
        
        st.info(f"選択されたモデル: {model}, Temperature: {temperature}")
    
    with tab2:
        st.header("データベース設定")
        
        # ChromaDB設定
        st.subheader("ChromaDB設定")
        db_path = st.text_input("ChromaDB Path", value=os.getenv('CHROMA_DB_PATH', './chroma_db'))
        if st.button("DB Pathを設定"):
            os.environ['CHROMA_DB_PATH'] = db_path
            st.success("DB Pathが設定されました")
        
        # データベース情報
        if os.path.exists(db_path):
            st.success(f"✅ データベースが存在します: {db_path}")
        else:
            st.warning(f"⚠️ データベースが存在しません: {db_path}")
    
    with tab3:
        st.header("システム情報")
        
        # システム情報の表示
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Python バージョン", "3.11")
            st.metric("Streamlit バージョン", "1.28.0")
            st.metric("OpenAI バージョン", "1.0.0")
        
        with col2:
            st.metric("ChromaDB バージョン", "0.4.0")
            st.metric("LangChain バージョン", "0.1.0")
            st.metric("システム状態", "正常")
        
        st.markdown("---")
        
        # ログエクスポート機能
        st.subheader("📋 ログ管理")
        
        from utils.logger import app_logger
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📄 ログをエクスポート (JSON)"):
                try:
                    log_data = app_logger.export_logs('json')
                    st.download_button(
                        label="📄 JSONログをダウンロード",
                        data=log_data,
                        file_name=f"isop_logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                        mime="application/json"
                    )
                except Exception as e:
                    st.error(f"ログエクスポート中にエラーが発生: {e}")
        
        with col2:
            if st.button("📄 ログをエクスポート (TXT)"):
                try:
                    log_data = app_logger.export_logs('text')
                    st.download_button(
                        label="📄 テキストログをダウンロード",
                        data=log_data,
                        file_name=f"isop_logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                        mime="text/plain"
                    )
                except Exception as e:
                    st.error(f"ログエクスポート中にエラーが発生: {e}")

def show_batch_processing_page():
    """バッチ処理ページの表示"""
    st.title("📦 バッチ処理")
    
    from services.batch_processor import create_batch_interface
    
    create_batch_interface()

def show_template_page():
    """テンプレートページの表示"""
    st.title("📋 テンプレート管理")
    
    from services.template_manager import create_template_interface
    
    create_template_interface()

if __name__ == "__main__":
    main()
