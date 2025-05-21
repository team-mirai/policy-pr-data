# policy-pr-data

このリポジトリには、team-mirai/policyリポジトリのプルリクエスト（PR）データがJSON形式でエクスポートされています。

## データ構造

`all_pr_data.json`ファイルには、GitHub APIからエクスポートされたPRデータが含まれています。各PRは以下の構造を持っています：

- `basic_info`: PR基本情報（番号、タイトル、URL、状態など）
  - `number`: PR番号
  - `state`: PRの状態（"open"または"closed"）
  - `title`: PRのタイトル
  - `html_url`: PRへのリンク
- `labels`: PRに付けられたラベルの配列
  - 各ラベルは`name`フィールドを持ち、ラベル名が格納されています（例：`教育`）

## 使用例

### 特定条件のPRをCSVに抽出する例

以下のPythonスクリプトは、教育ラベルが付いていて、ステータスがオープンのPRをCSVファイルに抽出する例です：

```python
import json
import csv
import os

# JSONデータの読み込み
with open('all_pr_data.json', 'r', encoding='utf-8') as f:
    pr_data = json.load(f)

# 条件に合うPRをフィルタリング
filtered_prs = []
for pr in pr_data:
    pr_number = pr.get('basic_info', {}).get('number', 0)
    pr_state = pr.get('basic_info', {}).get('state', '')
    
    # 教育ラベルの有無をチェック
    has_education_label = False
    for label in pr.get('labels', []):
        if label.get('name') == '教育':
            has_education_label = True
            break
    
    # 条件に合致するPRを追加
    if pr_state.lower() == 'open' and has_education_label:
        filtered_prs.append({
            'number': pr_number,
            'title': pr.get('basic_info', {}).get('title', ''),
            'url': pr.get('basic_info', {}).get('html_url', '')
        })

# PR番号でソート
filtered_prs.sort(key=lambda x: x['number'])

# CSVファイルに出力
csv_file_path = 'filtered_prs.csv'
with open(csv_file_path, 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['PR番号', 'PR件名', 'PRリンク'])
    for pr in filtered_prs:
        writer.writerow([pr['number'], pr['title'], pr['url']])

print(f"CSVファイルが作成されました: {os.path.abspath(csv_file_path)}")
```

このスクリプトは必要に応じて条件を変更することで、様々な条件のPRを抽出できます。
