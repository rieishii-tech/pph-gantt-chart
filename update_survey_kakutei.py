"""
FirebaseデータにSurveyKakutei__c（本現調日確定）フィールドを追加するスクリプト
firebase_admin SDKを使用して認証付きで書き込み
"""
import json, os, sys

sys.stdout.reconfigure(encoding='utf-8')

import firebase_admin
from firebase_admin import credentials, db

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SERVICE_ACCOUNT_KEY = os.path.join(SCRIPT_DIR, 'serviceAccountKey.json')
DATABASE_URL = 'https://pph-gantt-chart-default-rtdb.asia-southeast1.firebasedatabase.app'

# Salesforceから取得したSurveyKakutei__c マッピング（Id -> True）
survey_kakutei_map = {
    "0065h00000QBIzcAAH": True, "0065h00000QqngeAAB": True,
    "006J2000002IQE0IAO": True, "006J2000002KIz6IAG": True,
    "006J2000002KIzQIAW": True, "006J2000002LGVtIAO": True,
    "006J2000002LGW8IAO": True, "006J2000003pjrEIAQ": True,
    "006J2000004eT1bIAE": True, "006J2000004eT25IAE": True,
    "006J2000004hktgIAA": True, "006TL00000J8On2YAF": True,
    "006TL00000J8VoTYAV": True, "006TL00000JEK2NYAX": True,
    "006TL00000Jze41YAB": True, "006TL00000LKq04YAD": True,
    "006TL00000RkjFWYAZ": True, "006TL00000RknUPYAZ": True,
    "006TL00000RksqfYAB": True, "006TL00000Th6xaYAB": True,
    "006TL00000ZNsBeYAL": True, "006TL00000c5OAIYA2": True,
    "006TL00000cJJZ0YAO": True, "006TL00000f8K8UYAU": True,
    "006TL00000fPfoNYAS": True, "006TL00000fPwqnYAC": True,
    "006TL00000fQ2szYAC": True, "006TL00000fQ5PRYA0": True,
    "006TL00000fgP8xYAE": True, "006TL00000g7quaYAA": True,
    "006TL00000gYXarYAG": True, "006TL00000i2Ru2YAE": True,
    "006TL00000i2WSIYA2": True, "006TL00000iGxfYYAS": True,
    "006TL00000itMD4YAM": True, "006TL00000jntawYAA": True,
    "006TL00000kFVp0YAG": True, "006TL00000lEtw4YAC": True,
    "006TL00000m4NbuYAE": True, "006TL00000nG3NXYA0": True,
    "006TL00000nGU4OYAW": True, "006TL00000nGcjVYAS": True,
    "006TL00000nHHUrYAO": True, "006TL00000pHcMsYAK": True,
    "006TL00000pjOaIYAU": True, "006TL00000pkAF8YAM": True,
    "006TL00000pkAa6YAE": True, "006TL00000pkEFVYA2": True,
    "006TL00000qIcvKYAS": True, "006TL00000rI4gBYAS": True,
    "006TL00000rqzyYYAQ": True, "006TL00000rs930YAA": True,
    "006TL00000rs9pPYAQ": True, "006TL00000rsDg6YAE": True,
    "006TL00000s1cljYAA": True, "006TL00000s3PyrYAE": True,
    "006TL00000s3cXtYAI": True, "006TL00000s6xKrYAI": True,
    "006TL00000saWYYYA2": True, "006TL00000sac7hYAA": True,
    "006TL00000vpFtwYAE": True, "006TL00000vpxJnYAI": True,
    "006TL00000vqR3JYAU": True, "006TL00000vrvaPYAQ": True,
    "006TL00000xy5xKYAQ": True, "006TL00000xyKmiYAE": True,
    "006TL00000xyuRxYAI": True, "006TL00000xyv1RYAQ": True,
    "006TL00000yTrUbYAK": True, "006TL000010nzZiYAI": True,
    "006TL000010o6jGYAQ": True, "006TL000010oNiVYAU": True,
    "006TL000010oY7dYAE": True, "006TL000010oYyrYAE": True,
    "006TL000011taHuYAI": True, "006TL000012Nwo4YAC": True,
    "006TL000012PcYHYA0": True, "006TL000012wiVGYAY": True,
    "006TL000012xLTNYA2": True, "006TL000013AnV5YAK": True,
    "006TL000013BNWyYAO": True, "006TL000013BXhbYAG": True,
    "006TL000013BdAIYA0": True, "006TL000013BizZYAS": True,
    "006TL000014Q7RGYA0": True, "006TL000014RNFSYA4": True,
    "006TL000014qCn6YAE": True, "006TL000014qjxVYAQ": True,
    "006TL000015rrXSYAY": True, "006TL000015s760YAA": True,
    "006TL000015si3wYAA": True, "006TL000015sx6FYAQ": True,
    "006TL000015sx9SYAQ": True, "006TL000015t8fvYAA": True,
    "006TL000015tC3ZYAU": True, "006TL000015tEoaYAE": True,
    "006TL000015tOKsYAM": True, "006TL000015tWIQYA2": True,
    "006TL000015tZMkYAM": True, "006TL000015tmrpYAA": True,
    "006TL000015to8rYAA": True, "006TL000015trI1YAI": True,
}

def main():
    if not os.path.exists(SERVICE_ACCOUNT_KEY):
        print(f'エラー: サービスアカウントキーが見つかりません: {SERVICE_ACCOUNT_KEY}')
        sys.exit(1)

    # Firebase 初期化
    cred = credentials.Certificate(SERVICE_ACCOUNT_KEY)
    firebase_admin.initialize_app(cred, {'databaseURL': DATABASE_URL})

    # データ取得
    print('Firebaseからデータ取得中...')
    ref = db.reference('/pph_data')
    data = ref.get()

    if data is None:
        print('エラー: データが見つかりません')
        sys.exit(1)

    records = list(data.values()) if isinstance(data, dict) else data
    print(f'取得レコード数: {len(records)}')

    # SurveyKakutei__c を追加
    updated = 0
    for r in records:
        rid = r.get('Id', '')
        r['SurveyKakutei__c'] = survey_kakutei_map.get(rid, False)
        if r['SurveyKakutei__c']:
            updated += 1

    print(f'SurveyKakutei__c=true: {updated}件')

    # アップロード
    print('Firebaseにアップロード中...')
    ref.set(records)

    print(f'アップロード完了! ({len(records)}件)')

if __name__ == '__main__':
    main()
