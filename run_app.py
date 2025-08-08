import os
import subprocess
import sys

# このスクリプト自身の場所を基準にプロジェクトルートを特定
project_root = os.path.dirname(os.path.abspath(__file__))
app_file = os.path.join(project_root, 'app_core', 'app.py')

print(f"Project Root: {project_root}")
print(f"App File: {app_file}")

# Streamlitを実行する前にPYTHONPATHを設定
try:
    env = os.environ.copy()
    module_dirs = [
        'document_processor',
        'utils',
        'services',
        'ai_agent',
        'diff_generator',
        'vector_db_manager',
        'llm_client',
    ]
    env["PYTHONPATH"] = os.pathsep.join(
        [os.path.join(project_root, d) for d in module_dirs] + [env.get("PYTHONPATH", "")]
    )

    # Streamlitをsubprocessで実行
    command = [
        sys.executable,  # 現在のPythonインタプリタを使用
        '-m',
        'streamlit',
        'run',
        'app.py',
        '--server.headless',
        'true'
    ]

    print(f"Executing command: {' '.join(command)}")

    # バックグラウンドで実行するために Popen を使用
    # stdout/stderr をパイプにすると未読出時にバッファが詰まり停止する可能性があるため
    # None を指定して親プロセスと共有し、ブロッキングを回避する
    process = subprocess.Popen(
        command,
        env=env,
        cwd=os.path.join(project_root, 'app_core'),
        stdout=None,
        stderr=None,
    )

    print(f"Streamlit process started with PID: {process.pid}")
    print("Please access the URL provided by Streamlit in your web browser.")
    print("This command will continue to run in the background.")

except FileNotFoundError:
    print(f"Error: Could not find the application file at {app_file}")
except Exception as e:
    print(f"An error occurred: {e}")



