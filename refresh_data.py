"""
Salesforceから最新PPH商談データを取得し、Firebaseにアップロードするスクリプト。
GitHub Actionsまたはローカルから実行可能。

必要な環境変数:
  SF_USERNAME       - Salesforceユーザー名
  SF_PASSWORD       - Salesforceパスワード
  SF_SECURITY_TOKEN - Salesforceセキュリティトークン
  SF_DOMAIN         - Salesforceドメイン (login / test)
  FIREBASE_SA_KEY   - Firebase サービスアカウントキー (JSONテキスト)

ローカル実行時:
  - serviceAccountKey.json がカレントディレクトリにあれば FIREBASE_SA_KEY は不要
  - .env ファイルから環境変数を読み込み可能
"""
import json, os, sys, tempfile
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_URL = 'https://pph-gantt-chart-default-rtdb.asia-southeast1.firebasedatabase.app'

FIELDS = [
    'Id', 'Name', 'StageName', 'ConstractType__c',
    'Location__r.State__c', 'InvestigationUser__r.Name', 'ConstUser__r.Name',
    'Naijibi__c', 'TempSurveyDate__c', 'SurveyDate__c', 'SurveyKakutei__c',
    'Field27__c', 'KojiSekouyoteibi__c', 'ScheduleOfBlackoutDates__c',
    'KojiKankobi__c', 'Kankobi__c', 'StartDate__c',
    'KojiSekouKakuteibi__c', 'KankoKakuteibi__c', 'StartKakutei__c', 'Jucyubi__c'
]

FIELD_MAP = {
    'Location__r': {'State__c': 'Prefecture'},
    'InvestigationUser__r': {'Name': 'InvestigationUserName'},
    'ConstUser__r': {'Name': 'ConstUserName'},
}

SOQL = (
    "SELECT " + ", ".join(FIELDS) +
    " FROM Opportunity"
    " WHERE RecordType.Name = '改修'"
    " AND StageName != '09_失注/不成立'"
    " ORDER BY CreatedDate ASC"
)

def flatten_record(rec):
    """Salesforceレコードをフラットなdictに変換"""
    flat = {}
    for key, val in rec.items():
        if key == 'attributes':
            continue
        if isinstance(val, dict) and key in FIELD_MAP:
            for sub_key, out_name in FIELD_MAP[key].items():
                flat[out_name] = val.get(sub_key) if val else None
        else:
            flat[key] = val
    return flat

def main():
    # .envファイルがあれば読み込み
    env_path = os.path.join(SCRIPT_DIR, '.env')
    if os.path.exists(env_path):
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    k, v = line.split('=', 1)
                    os.environ.setdefault(k.strip(), v.strip())

    # --- Salesforce接続 ---
    try:
        from simple_salesforce import Salesforce
    except ImportError:
        print('エラー: simple_salesforce がインストールされていません')
        print('  pip install simple-salesforce')
        sys.exit(1)

    sf_user = os.environ.get('SF_USERNAME', '')
    sf_pass = os.environ.get('SF_PASSWORD', '')
    sf_token = os.environ.get('SF_SECURITY_TOKEN', '')
    sf_domain = os.environ.get('SF_DOMAIN', 'login')

    if not sf_user or not sf_pass:
        print('エラー: Salesforce認証情報が設定されていません')
        print('  環境変数 SF_USERNAME, SF_PASSWORD, SF_SECURITY_TOKEN を設定してください')
        print('  または .env ファイルに記載してください')
        sys.exit(1)

    print('Salesforceに接続中...')
    sf = Salesforce(username=sf_user, password=sf_pass,
                    security_token=sf_token, domain=sf_domain)

    print('データ取得中...')
    result = sf.query_all(SOQL)
    records = [flatten_record(r) for r in result['records']]
    print(f'取得件数: {len(records)}')

    # JSONファイル保存
    out_path = os.path.join(SCRIPT_DIR, 'pph_data_v5.json')
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(records, f, ensure_ascii=False, indent=2)
    print(f'JSON保存: {out_path}')

    # --- Firebase接続 ---
    try:
        import firebase_admin
        from firebase_admin import credentials, db
    except ImportError:
        print('エラー: firebase_admin がインストールされていません')
        print('  pip install firebase-admin')
        sys.exit(1)

    # サービスアカウントキーの取得
    sa_key_path = os.path.join(SCRIPT_DIR, 'serviceAccountKey.json')
    sa_key_env = os.environ.get('FIREBASE_SA_KEY', '')

    if sa_key_env:
        # 環境変数からサービスアカウントキー (GitHub Actions用)
        tmp = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
        tmp.write(sa_key_env)
        tmp.close()
        sa_key_path = tmp.name

    if not os.path.exists(sa_key_path):
        print(f'エラー: Firebase サービスアカウントキーが見つかりません')
        sys.exit(1)

    cred = credentials.Certificate(sa_key_path)
    firebase_admin.initialize_app(cred, {'databaseURL': DATABASE_URL})

    print('Firebaseにアップロード中...')
    ref = db.reference('/')
    ref.set({
        'pph_data': records,
        'metadata': {
            'lastUpdated': datetime.now().strftime('%Y/%m/%d %H:%M:%S'),
            'recordCount': len(records)
        }
    })

    # 一時ファイル削除
    if sa_key_env and os.path.exists(tmp.name):
        os.unlink(tmp.name)

    print(f'アップロード完了! ({len(records)}件)')
    print(f'更新日時: {datetime.now().strftime("%Y/%m/%d %H:%M:%S")}')

if __name__ == '__main__':
    main()
