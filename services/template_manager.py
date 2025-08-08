"""
テンプレート管理モジュール
規格別のテンプレートを管理し、書類作成を支援
"""

import os
import json
from typing import Dict, List, Optional
from pathlib import Path
import streamlit as st

class TemplateManager:
    """テンプレート管理クラス"""
    
    def __init__(self):
        self.templates_dir = Path("templates")
        self.templates = {}
        self.load_templates()
    
    def load_templates(self):
        """テンプレートを読み込み"""
        if not self.templates_dir.exists():
            return
        
        for template_file in self.templates_dir.glob("*.md"):
            try:
                with open(template_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                template_name = template_file.stem
                self.templates[template_name] = {
                    'name': template_name,
                    'filename': template_file.name,
                    'content': content,
                    'path': str(template_file)
                }
            except Exception as e:
                st.error(f"テンプレート読み込みエラー: {template_file.name} - {e}")
    
    def get_available_templates(self) -> List[Dict]:
        """利用可能なテンプレート一覧を取得"""
        return list(self.templates.values())
    
    def get_template(self, template_name: str) -> Optional[Dict]:
        """指定されたテンプレートを取得"""
        return self.templates.get(template_name)
    
    def apply_template(self, template_name: str, custom_data: Dict = None) -> str:
        """テンプレートを適用してカスタマイズされた内容を生成"""
        template = self.get_template(template_name)
        if not template:
            raise ValueError(f"テンプレートが見つかりません: {template_name}")
        
        content = template['content']
        
        # カスタムデータでプレースホルダーを置換
        if custom_data:
            for key, value in custom_data.items():
                placeholder = f"[{key}]"
                content = content.replace(placeholder, str(value))
        
        return content
    
    def create_custom_template(self, name: str, content: str) -> str:
        """カスタムテンプレートを作成"""
        template_file = self.templates_dir / f"{name}.md"
        
        with open(template_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # テンプレートを再読み込み
        self.load_templates()
        
        return str(template_file)

def create_template_interface():
    """テンプレート管理インターフェースを作成"""
    
    st.subheader("📋 テンプレート管理")
    
    template_manager = TemplateManager()
    
    # タブ分け
    tab1, tab2, tab3 = st.tabs(["📄 テンプレート選択", "✏️ カスタムテンプレート", "📚 テンプレート一覧"])
    
    with tab1:
        st.header("テンプレート選択")
        
        # 利用可能なテンプレート一覧
        templates = template_manager.get_available_templates()
        
        if templates:
            template_names = [t['name'] for t in templates]
            selected_template = st.selectbox(
                "テンプレートを選択",
                template_names,
                format_func=lambda x: x.replace('_', ' ').title()
            )
            
            if selected_template:
                template = template_manager.get_template(selected_template)
                
                # テンプレートのプレビュー
                with st.expander("テンプレートプレビュー"):
                    st.markdown(template['content'])
                
                # カスタムデータの入力
                st.subheader("カスタムデータ入力")
                
                # 基本的なカスタムデータ
                custom_data = {}
                
                col1, col2 = st.columns(2)
                with col1:
                    custom_data['組織名'] = st.text_input("組織名", value="[組織名を記入]")
                    custom_data['事業内容'] = st.text_area("事業内容", value="[組織の事業内容、規模、所在地等を記入]")
                    custom_data['適用範囲'] = st.text_area("適用範囲", value="[ISMSの適用範囲を明確に記入]")
                
                with col2:
                    custom_data['作成日'] = st.date_input("作成日")
                    custom_data['作成者'] = st.text_input("作成者", value="[作成者名]")
                    custom_data['バージョン'] = st.text_input("バージョン", value="1.0")
                
                # テンプレートの適用
                if st.button("🚀 テンプレートを適用", type="primary"):
                    try:
                        applied_content = template_manager.apply_template(selected_template, custom_data)
                        
                        st.success("テンプレートが適用されました！")
                        
                        # 適用結果の表示
                        st.subheader("適用結果")
                        st.markdown(applied_content)
                        
                        # ダウンロードボタン
                        st.download_button(
                            label="📄 適用結果をダウンロード",
                            data=applied_content,
                            file_name=f"{selected_template}_{custom_data.get('組織名', 'document')}.md",
                            mime="text/markdown"
                        )
                        
                    except Exception as e:
                        st.error(f"テンプレート適用中にエラーが発生しました: {e}")
        else:
            st.info("利用可能なテンプレートがありません。")
    
    with tab2:
        st.header("カスタムテンプレート作成")
        
        template_name = st.text_input("テンプレート名", placeholder="例: カスタムISO27001")
        template_content = st.text_area(
            "テンプレート内容",
            height=400,
            placeholder="テンプレートの内容を入力してください。\nプレースホルダーは [変数名] の形式で記入してください。"
        )
        
        if st.button("💾 テンプレートを保存", type="primary"):
            if template_name and template_content:
                try:
                    template_file = template_manager.create_custom_template(template_name, template_content)
                    st.success(f"テンプレートが保存されました: {template_file}")
                except Exception as e:
                    st.error(f"テンプレート保存中にエラーが発生しました: {e}")
            else:
                st.warning("テンプレート名と内容を入力してください。")
    
    with tab3:
        st.header("テンプレート一覧")
        
        templates = template_manager.get_available_templates()
        
        if templates:
            for template in templates:
                with st.expander(f"📄 {template['name']}"):
                    st.markdown(f"**ファイル名**: {template['filename']}")
                    st.markdown(f"**パス**: {template['path']}")
                    
                    # テンプレート内容のプレビュー（最初の500文字）
                    preview = template['content'][:500]
                    if len(template['content']) > 500:
                        preview += "..."
                    
                    st.markdown("**内容プレビュー**:")
                    st.code(preview, language="markdown")
        else:
            st.info("テンプレートがありません。")

def get_standard_templates() -> Dict[str, str]:
    """標準テンプレートの説明を取得"""
    return {
        "iso_27001_template": "ISO 27001（情報セキュリティマネジメント）用のテンプレート",
        "iso_9001_template": "ISO 9001（品質マネジメント）用のテンプレート",
        "privacy_mark_template": "プライバシーマーク用のテンプレート",
        "general_template": "汎用規格対応用のテンプレート"
    }
