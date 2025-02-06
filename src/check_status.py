from datetime import datetime
import os

def check_status_main():
    # 現在の日時を取得
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # `main.py` があるディレクトリに `health.txt` を配置
    base_dir = os.path.dirname(os.path.abspath(__file__))  # `check_status.py` があるディレクトリ
    parent_dir = os.path.dirname(base_dir)  # `src` の親ディレクトリを取得
    file_path = os.path.join(parent_dir, "health.txt")  # `health.txt` を `src` の外に保存

    # ファイルに書き込む
    with open(file_path, "w") as file:
        file.write(f"Running dayo : {current_date}")
