"""
バッチ処理モジュール
複数の書類を一括処理する機能を提供
"""

import os
import json
from typing import List, Dict, Any
from datetime import datetime
import streamlit as st
from pathlib import Path

from document_processor.extractor import extract_text
from services.document_service import process_and_store_document
from ai_agent.rag import rewrite_document_with_rag
from diff_generator.generator import generate_diff_report
from utils.logger import app_logger, log_file_operation, log_ai_operation

class BatchProcessor:
    """バッチ処理を管理するクラス"""
    
    def __init__(self):
        self.batch_id = None
        self.batch_results = []
        self.batch_config = {}
    
    def start_batch(self, batch_name: str = None) -> str:
        """バッチ処理を開始"""
        from datetime import datetime
        import uuid
        
        self.batch_id = f"batch_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{str(uuid.uuid4())[:8]}"
        self.batch_results = []
        self.batch_config = {
            'batch_id': self.batch_id,
            'batch_name': batch_name or f"バッチ処理_{datetime.now().strftime('%Y-%m-%d %H:%M')}",
            'start_time': datetime.now().isoformat(),
            'status': 'running'
        }
        
        app_logger.log_info(f"バッチ処理を開始: {self.batch_id}")
        return self.batch_id
    
    def process_document_batch(self, documents: List[Dict[str, Any]], new_standard_text: str) -> Dict[str, Any]:
        """複数の書類を一括処理"""
        
        if not self.batch_id:
            self.start_batch()
        
        results = {
            'batch_id': self.batch_id,
            'total_documents': len(documents),
            'processed_documents': 0,
            'successful_documents': 0,
            'failed_documents': 0,
            'results': []
        }
        
        for i, doc in enumerate(documents):
            try:
                app_logger.log_info(f"書類処理開始: {doc.get('name', f'Document_{i+1}')}")
                
                # 書類の処理
                doc_result = self._process_single_document(doc, new_standard_text, i+1)
                results['results'].append(doc_result)
                results['processed_documents'] += 1
                
                if doc_result['status'] == 'success':
                    results['successful_documents'] += 1
                else:
                    results['failed_documents'] += 1
                    
            except Exception as e:
                app_logger.log_error(f"書類処理中にエラー: {doc.get('name', f'Document_{i+1}')}", e)
                results['results'].append({
                    'document_name': doc.get('name', f'Document_{i+1}'),
                    'status': 'error',
                    'error': str(e)
                })
                results['failed_documents'] += 1
        
        # バッチ処理の完了
        self.batch_config['end_time'] = datetime.now().isoformat()
        self.batch_config['status'] = 'completed'
        self.batch_config['results'] = results
        
        app_logger.log_info(f"バッチ処理完了: {self.batch_id}", {
            'total': results['total_documents'],
            'successful': results['successful_documents'],
            'failed': results['failed_documents']
        })
        
        return results
    
    def _process_single_document(self, document: Dict[str, Any], new_standard_text: str, doc_index: int) -> Dict[str, Any]:
        """単一書類の処理"""
        
        result = {
            'document_name': document.get('name', f'Document_{doc_index}'),
            'status': 'processing',
            'start_time': datetime.now().isoformat(),
            'processing_steps': []
        }
        
        try:
            # ステップ1: テキスト抽出
            result['processing_steps'].append({
                'step': 'text_extraction',
                'status': 'started',
                'timestamp': datetime.now().isoformat()
            })
            
            existing_doc_text = extract_text(document['content'], document['type'])
            
            result['processing_steps'][-1]['status'] = 'completed'
            result['processing_steps'][-1]['end_timestamp'] = datetime.now().isoformat()
            
            # ステップ2: ベクトル化
            result['processing_steps'].append({
                'step': 'vectorization',
                'status': 'started',
                'timestamp': datetime.now().isoformat()
            })
            
            doc_id, num_chunks = process_and_store_document(
                file_content=document['content'],
                file_type=document['type'],
                document_name=document['name']
            )
            
            result['processing_steps'][-1]['status'] = 'completed'
            result['processing_steps'][-1]['end_timestamp'] = datetime.now().isoformat()
            result['processing_steps'][-1]['details'] = {'doc_id': doc_id, 'num_chunks': num_chunks}
            
            # ステップ3: AI書き換え
            result['processing_steps'].append({
                'step': 'ai_rewrite',
                'status': 'started',
                'timestamp': datetime.now().isoformat()
            })
            
            rewritten_doc = rewrite_document_with_rag(
                existing_doc_id=doc_id,
                new_standard_text=new_standard_text
            )
            
            result['processing_steps'][-1]['status'] = 'completed'
            result['processing_steps'][-1]['end_timestamp'] = datetime.now().isoformat()
            
            # ステップ4: 差分生成
            result['processing_steps'].append({
                'step': 'diff_generation',
                'status': 'started',
                'timestamp': datetime.now().isoformat()
            })
            
            diff_report = generate_diff_report(existing_doc_text, rewritten_doc, format='markdown')
            
            result['processing_steps'][-1]['status'] = 'completed'
            result['processing_steps'][-1]['end_timestamp'] = datetime.now().isoformat()
            
            # 結果の保存
            result['status'] = 'success'
            result['end_time'] = datetime.now().isoformat()
            result['rewritten_document'] = rewritten_doc
            result['diff_report'] = diff_report
            result['original_text'] = existing_doc_text
            
        except Exception as e:
            result['status'] = 'error'
            result['error'] = str(e)
            result['end_time'] = datetime.now().isoformat()
            app_logger.log_error(f"書類処理エラー: {document.get('name', f'Document_{doc_index}')}", e)
        
        return result
    
    def save_batch_results(self, output_dir: str = "./batch_results"):
        """バッチ処理結果を保存"""
        
        if not self.batch_config:
            raise ValueError("バッチ処理が開始されていません")
        
        # 出力ディレクトリの作成
        os.makedirs(output_dir, exist_ok=True)
        
        # 結果ファイルの保存
        batch_file = os.path.join(output_dir, f"{self.batch_id}.json")
        with open(batch_file, 'w', encoding='utf-8') as f:
            json.dump(self.batch_config, f, ensure_ascii=False, indent=2)
        
        # 各書類の結果を個別ファイルとして保存
        for result in self.batch_config.get('results', {}).get('results', []):
            if result['status'] == 'success':
                doc_name = result['document_name'].replace('/', '_').replace('\\', '_')
                
                # 書き換えられた書類を保存
                rewritten_file = os.path.join(output_dir, f"{self.batch_id}_{doc_name}_rewritten.md")
                with open(rewritten_file, 'w', encoding='utf-8') as f:
                    f.write(result['rewritten_document'])
                
                # 差分レポートを保存
                diff_file = os.path.join(output_dir, f"{self.batch_id}_{doc_name}_diff.md")
                with open(diff_file, 'w', encoding='utf-8') as f:
                    f.write(result['diff_report'])
        
        app_logger.log_info(f"バッチ処理結果を保存: {batch_file}")
        return batch_file
    
    def get_batch_summary(self) -> Dict[str, Any]:
        """バッチ処理の概要を取得"""
        
        if not self.batch_config:
            return {}
        
        results = self.batch_config.get('results', {})
        
        return {
            'batch_id': self.batch_id,
            'batch_name': self.batch_config.get('batch_name'),
            'start_time': self.batch_config.get('start_time'),
            'end_time': self.batch_config.get('end_time'),
            'status': self.batch_config.get('status'),
            'total_documents': results.get('total_documents', 0),
            'successful_documents': results.get('successful_documents', 0),
            'failed_documents': results.get('failed_documents', 0),
            'success_rate': (results.get('successful_documents', 0) / max(results.get('total_documents', 1), 1)) * 100
        }

def create_batch_interface():
    """バッチ処理インターフェースを作成"""
    
    st.subheader("📦 バッチ処理")
    
    # バッチ処理の設定
    with st.expander("バッチ処理設定"):
        batch_name = st.text_input("バッチ処理名", value=f"バッチ処理_{datetime.now().strftime('%Y-%m-%d %H:%M')}")
        
        # ファイルアップロード（複数）
        uploaded_files = st.file_uploader(
            "処理する書類をアップロード（複数選択可能）",
            type=['pdf', 'docx', 'txt'],
            accept_multiple_files=True
        )
        
        new_standard_file = st.file_uploader(
            "新規格内容をアップロード",
            type=['pdf', 'txt']
        )
    
    # バッチ処理の実行
    if uploaded_files and new_standard_file and st.button("🚀 バッチ処理を開始", type="primary"):
        
        try:
            # バッチ処理の初期化
            processor = BatchProcessor()
            processor.start_batch(batch_name)
            
            # 新規格内容の読み込み
            new_standard_content = new_standard_file.getvalue()
            new_standard_text = extract_text(new_standard_content, new_standard_file.type)
            
            # 書類リストの作成
            documents = []
            for file in uploaded_files:
                documents.append({
                    'name': file.name,
                    'content': file.getvalue(),
                    'type': file.type,
                    'size': file.size
                })
            
            # バッチ処理の実行
            with st.spinner("バッチ処理を実行中..."):
                results = processor.process_document_batch(documents, new_standard_text)
            
            # 結果の表示
            st.success(f"バッチ処理が完了しました！")
            
            # 結果サマリー
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("総書類数", results['total_documents'])
            with col2:
                st.metric("成功", results['successful_documents'])
            with col3:
                st.metric("失敗", results['failed_documents'])
            with col4:
                success_rate = (results['successful_documents'] / max(results['total_documents'], 1)) * 100
                st.metric("成功率", f"{success_rate:.1f}%")
            
            # 詳細結果の表示
            with st.expander("詳細結果"):
                for i, result in enumerate(results['results']):
                    st.write(f"**{result['document_name']}**: {result['status']}")
                    if result['status'] == 'error':
                        st.error(f"エラー: {result.get('error', 'Unknown error')}")
            
            # 結果の保存
            if st.button("💾 結果を保存"):
                output_file = processor.save_batch_results()
                st.success(f"結果を保存しました: {output_file}")
                
        except Exception as e:
            st.error(f"バッチ処理中にエラーが発生しました: {e}")
            app_logger.log_error("バッチ処理エラー", e)
