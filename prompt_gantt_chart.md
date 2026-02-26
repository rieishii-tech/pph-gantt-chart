# PPH商談ガントチャート生成プロンプト

## 概要
SalesforceのPPH（太陽光発電関連）商談データからインタラクティブなガントチャートHTMLを自動生成するPythonスクリプト `generate_gantt.py` を作成・保守してください。

---

## データソース

### Salesforceクエリ条件
- **オブジェクト**: Opportunity（商談）
- **フィルタ条件**:
  - `PPH__c = true`
  - `CloseDate >= 2025-01-01`
  - **除外ステータス**: `完工`, `失注`, `ペンディング`（StageName NOT IN）
- **取得フィールド**:
  - 基本: `Id`, `Name`, `StageName`, `ConstractType__c`（事業区分）
  - 日付: `Naijibi__c`（内示日）, `TempSurveyDate__c`（仮現調日）, `SurveyDate__c`（本現調日）, `Field27__c`（納品日）, `KojiSekouyoteibi__c`（着工施工予定日）, `ScheduleOfBlackoutDates__c`（停電日）, `KojiKankobi__c`（完工検査日）, `Kankobi__c`（完工日/開通予定日）, `StartDate__c`（稼働開始日）
  - フラグ: `KojiSekouKakuteibi__c`（施工確定フラグ boolean）
  - リレーション: `Location__r.State__c`（都道府県 → `Prefecture`として保存）, `InvestigationUser__r.Name`（現調者 → `InvestigationUserName`）, `ConstUser__r.Name`（施工担当 → `ConstUserName`）
- **レコード数**: 約445件（ページネーション対応、offset 0/200/400で3回クエリ）
- **データ形式**: JSON（`pph_data_v4_full.json`）、日付は `YYYY-MM-DD` 文字列またはnull

---

## 生成するHTML/JavaScript仕様

### 全体構成（上から順に）
1. **ヘッダー**（sticky top:0, z-index:200）
   - タイトル「PPH商談 ガントチャート（進行中案件）」
   - 最終更新日時、全データ件数
2. **本日のスケジュール ダッシュボード**（sticky top:48px, z-index:190）
3. **コントロールバー**（フィルタ・検索・期間選択）（sticky, z-index:180）
4. **凡例**
5. **ガントチャートテーブル**

### 本日のスケジュール ダッシュボード
カードベースのレイアウトで本日および明日の予定を表示。

#### 表示カード（displayOrder順）

| カード名 | アイコン | 条件 |
|---------|--------|------|
| 開通予定（本日） | ★ | `Kankobi__c === todayStr` かつ ステータス `08_` or `09_` |
| 開通予定（明日） | ☆ | `Kankobi__c === tmrStr` かつ ステータス `08_` or `09_`。枠線は緑の点線 |
| 着工予定（本日） | 工 | `KojiSekouyoteibi__c === todayStr` かつ ステータス `08_` |
| 本現調 | 現 | `SurveyDate__c === todayStr` |
| 仮現調 | 仮 | `TempSurveyDate__c === todayStr` |
| 施工中 | 中 | `todayStr > KojiSekouyoteibi__c` かつ `todayStr < Kankobi__c` かつ ステータス `08_` or `09_` |
| 停電 | 停 | `ScheduleOfBlackoutDates__c === todayStr` |
| 完工検査 | 検 | `KojiKankobi__c === todayStr` |
| 納品 | 納 | `Field27__c === todayStr` |
| 内示 | 示 | `Naijibi__c === todayStr` |

#### 重要な実装ルール
- **日付比較は必ず文字列ベース（`YYYY-MM-DD`）で行う**。`new Date().getTime()` によるタイムスタンプ比較はタイムゾーン/DSTの問題で誤判定するため禁止。
- 各カードに都道府県タグ、商談名、関連日付（施工中→完工日、着工→完工日、開通→着工日）、ステータスタグを表示
- 折りたたみトグル機能あり
- 合計件数バッジ表示

### ガントチャートテーブル

#### 固定列（7列、position:sticky + left）

| 列 | width | left | 内容 |
|----|-------|------|------|
| 商談名 | 200px | 0 | overflow:ellipsis |
| 県 | 56px | 200px | 都道府県（center） |
| 区分 | 56px | 256px | 事業区分（center） |
| 現調者 | 56px | 312px | InvestigationUserName |
| 施工担当 | 56px | 368px | ConstUserName |
| ステータス | 110px | 424px | StageName |
| 次の予定 | 120px | 534px | 「○○待ち M/D」形式。右端に2px紺ボーダー |

#### z-index階層（重要）
```
ヘッダー corner cells（top+left）: z-index: 40
ヘッダー sticky列（top+left）    : z-index: 30
ヘッダー日付セル（topのみ）      : z-index: 20
ボディ sticky列（leftのみ）      : z-index: 5
```

#### CSS必須設定
```css
table { border-collapse: separate; border-spacing: 0; }
```
※ `border-collapse: collapse` だとstickyが正しく機能しないため `separate` を使用

#### 日付セル（横軸）
- 2段ヘッダー: 1行目=年/月（colspan）、2行目=日
- 各セル幅: 24px
- **土曜日**: 背景 `#e3f2fd`、ヘッダー `#bbdefb`（青系）
- **日曜日・祝日**: 背景 `#ffebee`、ヘッダー `#ffcdd2`（赤系）
- **本日**: `border-left/right: 2px solid #f44336` + 背景 `rgba(255,0,0,0.15)`
- **祝日**: 2025〜2027年の日本の祝日をSetでハードコード

#### ガントバーの色
| イベント | 色 | 備考 |
|---------|-----|------|
| 内示日 | `#607d8b` | |
| 仮現調 | `#b3e5fc` + `border:2px solid #4fc3f7` | |
| 本現調 | `#4fc3f7` | |
| 納品 | `#795548` | |
| 着工〜完工期間 | 確定: `#ff9800` / 予定: `#ffe0b2` | KojiSekouKakuteibi__cで判定 |
| 停電 | `#f44336` | |
| 完工検査 | `#ab47bc` | |
| 稼働開始 | `#4caf50` | |

### フィルタ機能
- **ステータス**: 全て / 施工以降（08-09）/ 各個別ステータス
- **都道府県**: データから自動生成
- **事業区分**: データから自動生成
- **現調者**: 全て / 設定あり / 未設定
- **施工担当**: 全て / 設定あり / 未設定
- **検索**: 商談名の部分一致
- **期間**: 3ヶ月 / 6ヶ月（デフォルト）/ 12ヶ月 / 全期間
  - 期間の開始月: **当月1日から**

### ソート機能
- 全7固定列にクリックソート（asc/desc切替）
- デフォルトソート: 着工予定日 → 完工日（昇順、nullは最後）
- 次の予定列: 日付の早い順

### その他
- 初期表示時、本日列にスクロール（`scrollIntoView({inline:'center'})`）
- 偶数行の背景: `#fafafa`（sticky列含む）
- ホバー: `#e8eaf6`（sticky列含む）
- 現調者/施工担当: 設定あり=青字太字（`.has-user`）、未設定=グレー（`.no-user`）

---

## Python側の実装

### データ読み込み
```python
import json, os, sys
sys.stdout.reconfigure(encoding='utf-8')

data_dir = os.path.join(os.path.expanduser('~'), '.claude', 'projects',
    'C--Users------Desktop-Claude-Code-Demo',
    '370f5140-6c9c-4df8-88af-62792628b142', 'tool-results')
with open(os.path.join(data_dir, 'pph_data_v4_full.json'), 'r', encoding='utf-8') as f:
    data = json.load(f)
```

### HTML生成
- `html_template` 内の `__DATA_PLACEHOLDER__` をJSON文字列で置換
- 出力先: `~/Desktop/Claude_Code_Demo/pph_gantt_chart.html`

---

## 過去に発生したバグと教訓

### 1. 施工中にステータス不一致レコードが表示される
- **原因**: 施工中の判定が日付範囲のみでステータスを確認していなかった
- **対策**: 必ず `StageName.startsWith('08')` or `startsWith('09')` をチェック

### 2. 開通予定（本日）に今日以外のレコードが表示される
- **原因**: `new Date(s+'T00:00:00').getTime()` でのタイムスタンプ比較がタイムゾーンの影響で不正確
- **対策**: ダッシュボードの日付比較はすべて `YYYY-MM-DD` 文字列の直接比較に変更

### 3. スクロール時に固定列が消える
- **原因**: `border-collapse: collapse` ではstickyが正しく動作しない。z-indexの階層が不適切
- **対策**: `border-collapse: separate; border-spacing: 0` を使用。z-indexを4段階（40/30/20/5）に設定

---

## ファイル構成
```
~/Desktop/Claude_Code_Demo/
  ├── generate_gantt.py        # メイン生成スクリプト
  ├── pph_gantt_chart.html     # 生成されるHTML出力
  └── prompt_gantt_chart.md    # このプロンプト
~/.claude/projects/.../tool-results/
  └── pph_data_v4_full.json    # Salesforceデータ（445件）
```
