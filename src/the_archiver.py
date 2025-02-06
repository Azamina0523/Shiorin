import subprocess
import logging
import json
import re
import os
from .rssfeeds_handler import rssfeeds_handler_main

# 親ディレクトリの絶対パスを取得
base_dir = os.path.dirname(os.path.abspath(__file__))  # `the_archiver.py` があるディレクトリ
parent_dir = os.path.dirname(base_dir)  # `src` の親ディレクトリを取得

# 設定ファイルとログファイルのパスを親ディレクトリに設定
setting_json_path = os.path.join(parent_dir, 'setting.json')
log_file_path = os.path.join(parent_dir, 'log.txt')

# loggingの設定
logging.basicConfig(
    filename=log_file_path,
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    encoding='utf-8'
)

def load_config(filename=setting_json_path):
    # 設定ファイル読み込み
    with open(filename, 'r', encoding='utf-8') as file:
        config = json.load(file)
    return config

keywords_list = load_config()['keywords']

def filter_by_keywords(entries, keywords):
    # keywords_listでエントリをフィルタ
    filtered_entries = []
    
    for entry in entries:
        title = entry['title'].lower()
        # 小文字にして比較
        if any(keyword.lower() in title for keyword in keywords):
            filtered_entries.append(entry)
            # 合致してたらfiltered_entriesに追加
    
    return filtered_entries

def subprocess_run_entries(filtered_entries):
    # フィルタしたエントリytarchive叩く
    for entry in filtered_entries:
        channel = re.sub(r'[<>:"/\\|?*]', '_', entry['channel'])
        title = re.sub(r'[<>:"/\\|?*]', '_', entry['title'])
        # 使えない文字弾く
        link = entry['link']

        command = [
            "ytarchive",
            "--write-thumbnail",
            "--write-description",
            "-w",
            "-r","30",
            "-o",f"{channel}/[%(channel)s]_[%(upload_date)s]_%(title)s_(%(id)s)",
            link,
            "best"
        ]

        subprocess.run(["start", "cmd", "/C"] + command, shell=True)

        logging.info(f"Channel='{channel}', Title='{title}', Link='{link}'")

def the_archiver_main():
    processed_entries = rssfeeds_handler_main()
    filtered_entries = filter_by_keywords(processed_entries, keywords_list)
    subprocess_run_entries(filtered_entries)

if __name__ == "__main__":
    the_archiver_main()