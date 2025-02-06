import os
import json
import feedparser

base_dir = os.path.dirname(os.path.abspath(__file__))  # `src` ディレクトリ
parent_dir = os.path.dirname(base_dir)  # `src` の親ディレクトリを取得

# ファイルパスを親ディレクトリに変更
feed_json_path = os.path.join(parent_dir, 'feeds.json')  # フィードの履歴json
setting_json_path = os.path.join(parent_dir, 'setting.json')  # 設定json


def load_config(filename=setting_json_path):
    #設定ファイル読み込み
    with open(filename, 'r', encoding='utf-8') as file:
        config = json.load(file)
    return config

raw_channel_list = load_config()['channels']

channel_list = [(channel["name"], channel["url"]) for channel in raw_channel_list]


def load_json(file_path):
    #feeds.json読み込み
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return []


def save_json(file_path, data):
    #JSON保存
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def fetch_rss_feed(url):
    #RSSフィード取得
    return feedparser.parse(url)


def update_json_with_new_entries(archived_feed, rss_data, channel_name):
    #新しいエントリを比較してJSONに追加
    new_entries = []
    #空のリスト宣言

    for entry in rss_data.entries:
        #ここでのentryはrssフィード内の<entry>だよ
        if not any(existing_entry['link'] == entry.link for existing_entry in archived_feed):
            #取得したエントリのlink見て同じじゃないならnew_entryに入れる
            new_entry = {
                'channel': channel_name,
                'title': entry.title,
                'link': entry.link,
                'published': entry.published,
            }
            new_entries.append(new_entry)
            #空のリストにnew_entryを追加

    archived_feed.extend(new_entries)
    #new_entriesをarchived_feed(mainで宣言、既存のjson)に追記拡張

    return new_entries
    #追加分を返す


'''def print_new_entries(entries):
    #新しいエントリをテキストとして出力
    for entry in entries:
        print(f"新しい配信が見つかりました")
        print(f"チャンネル名: {entry['channel']}")
        print(f"配信タイトル: {entry['title']}")
        print(f"URL: {entry['link']}")
        print(f"公開日: {entry['published']}")
        print("-" * 40)
'''


def rssfeeds_handler_main():
    #メイン
    archived_feed = load_json(feed_json_path)
    all_new_entries = []
    #JSON読み込み

    for channel_name, rss_url in channel_list:
        #チャンネルリストの内容で各関数をfor
        rss_data = fetch_rss_feed(rss_url)
        new_entries = update_json_with_new_entries(archived_feed, rss_data, channel_name)
        all_new_entries.extend(new_entries)

    save_json(feed_json_path, archived_feed)
    #更新したデータをJSONファイルに保存

    #print_new_entries(all_new_entries)
    #新しいエントリをテキストとして出力

    return all_new_entries
    #返す