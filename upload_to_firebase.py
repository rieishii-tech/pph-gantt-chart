"""
PPH商談データを Firebase Realtime Database にアップロードするスクリプト。
Usage: python upload_to_firebase.py
"""
import json, os, sys
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

import firebase_admin
from firebase_admin import credentials, db

# --- 設定 ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SERVICE_ACCOUNT_KEY = os.path.join(SCRIPT_DIR, 'serviceAccountKey.json')
DATABASE_URL = 'https://pph-gantt-chart-default-rtdb.asia-southeast1.firebasedatabase.app'
DATA_FILE = os.path.join(SCRIPT_DIR, 'pph_data_v5.json')

def main():
    # データ読み込み
    if not os.path.exists(DATA_FILE):
        print(f'エラー: データファイルが見つかりません: {DATA_FILE}')
        sys.exit(1)

    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    print(f'読み込みレコード数: {len(data)}')

    # Firebase 初期化
    if not os.path.exists(SERVICE_ACCOUNT_KEY):
        print(f'エラー: サービスアカウントキーが見つかりません: {SERVICE_ACCOUNT_KEY}')
        sys.exit(1)

    cred = credentials.Certificate(SERVICE_ACCOUNT_KEY)
    firebase_admin.initialize_app(cred, {'databaseURL': DATABASE_URL})

    # データアップロード
    print('Firebase にアップロード中...')
    ref = db.reference('/')
    ref.set({
        'pph_data': data,
        'metadata': {
            'lastUpdated': datetime.now().strftime('%Y/%m/%d %H:%M:%S'),
            'recordCount': len(data)
        }
    })

    print(f'アップロード完了! ({len(data)}件)')
    print(f'更新日時: {datetime.now().strftime("%Y/%m/%d %H:%M:%S")}')
    print(f'Database URL: {DATABASE_URL}')

if __name__ == '__main__':
    main()
