from pystray import Icon, Menu, MenuItem
from PIL import Image
import threading
import time
import importlib
import os
import src
import logging

# ロギングの設定
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(message)s", encoding='utf-8')

# タスクを実行するフラグ（スレッドの制御用）
running_event = threading.Event()
running_event.set()

def background_task():
    while running_event.is_set():
        try:
            logging.debug("Reloading src and calling functions.")
            importlib.reload(src)  # __init__.py にあるモジュールをリロード

            src.check_status_main()  # __init__.py で定義した関数を直接呼び出し
            src.the_archiver_main()

            time.sleep(30)
        except Exception as e:
            logging.error(f"Error in background_task: {e}")
            running_event.clear()  # エラーが発生した場合スレッドを停止

def on_exit(icon, _):
    logging.info("Exiting the application...")
    running_event.clear()  # スレッドのループを停止
    icon.stop()

def run_icon():
    try:
        image_path = os.path.join(os.path.dirname(__file__), 'src', 'icon.ico')
        image = Image.open(image_path)

        menu = Menu(MenuItem("Exit", on_exit))
        icon = Icon("Shiorin", image, "Shiori Novella here, at your service!", menu)

        logging.debug("Running icon...")
        icon.run()  # アイコンを表示
    except Exception as e:
        logging.error(f"Error in run_icon: {e}")

def main():
    try:
        # background_task を動かす
        logging.debug("Starting background task thread...")
        task_thread = threading.Thread(target=background_task, daemon=True)
        task_thread.start()

        # pystray を動かす
        run_icon()
    except Exception as e:
        logging.error(f"Error in main: {e}")

if __name__ == "__main__":
    main()