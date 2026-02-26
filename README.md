# PPH商談 ガントチャート

SalesforceのPPH商談データをインタラクティブなガントチャートで表示するWebアプリです。

## 構成

- `index.html` - ガントチャート本体（GitHub Pagesで公開）
- `upload_to_firebase.py` - Salesforceデータ → Firebase アップロード
- `generate_gantt.py` - オフライン用HTML生成スクリプト
- `prompt_gantt_chart.md` - 仕様書

## セットアップ

### 1. 依存パッケージのインストール

```bash
pip install -r requirements.txt
```

### 2. Firebase サービスアカウントキー

`serviceAccountKey.json` をプロジェクトルートに配置してください（`.gitignore` 済み）。

### 3. データアップロード

```bash
python upload_to_firebase.py
```

### 4. 閲覧

GitHub Pages URL または `index.html` をブラウザで開いてください。

## データ更新

Salesforceからデータを再取得した後、`upload_to_firebase.py` を実行するだけでWebが更新されます。
