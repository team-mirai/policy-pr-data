#!/usr/bin/env python3
"""
PRデータの統計抽出処理をテストするスクリプト
"""

import json
import sys
from collections import defaultdict

def load_pr_data_sample(json_path, sample_size=1000):
    """PRデータのサンプルをJSONファイルから読み込む"""
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data_str = f.read(10 * 1024 * 1024)  # 最初の10MBを読み込む
            
            start_idx = data_str.find('[')
            if start_idx == -1:
                print("JSONデータが配列形式ではありません")
                return []
                
            data_str = data_str[start_idx:]
            
            obj_count = 0
            brace_count = 0
            end_idx = 0
            in_string = False
            escape_next = False
            
            for i, char in enumerate(data_str):
                if escape_next:
                    escape_next = False
                    continue
                
                if char == '"' and not escape_next:
                    in_string = not in_string
                elif char == '\\' and in_string:
                    escape_next = True
                elif not in_string:
                    if char == '{':
                        brace_count += 1
                        if brace_count == 1:  # 新しいオブジェクトの開始
                            obj_start = i
                    elif char == '}':
                        brace_count -= 1
                        if brace_count == 0:  # オブジェクトの終了
                            obj_count += 1
                            end_idx = i + 1
                            if obj_count >= sample_size:
                                break
            
            if obj_count > 0:
                sample_data_str = data_str[:end_idx] + "]"
                sample_data_str = sample_data_str.replace(",]", "]")  # 末尾のカンマを削除
                
                try:
                    return json.loads(sample_data_str)
                except json.JSONDecodeError as e:
                    print(f"サンプルデータのJSONパースに失敗しました: {e}")
                    return []
            else:
                print("データの抽出に失敗しました")
                return []
                
    except Exception as e:
        print(f"PRデータの読み込み中にエラーが発生しました: {e}")
        return []

def extract_daily_pr_stats(pr_data):
    """日次のPR作成数とマージ数を計算する"""
    creation_dates = defaultdict(int)
    merge_dates = defaultdict(int)
    
    for pr in pr_data:
        basic_info = pr.get("basic_info", {})
        
        if "created_at" in basic_info:
            created_at = basic_info["created_at"]
            date = created_at.split("T")[0]
            creation_dates[date] += 1
        
        if "merged_at" in basic_info and basic_info["merged_at"]:
            merged_at = basic_info["merged_at"]
            date = merged_at.split("T")[0]
            merge_dates[date] += 1
    
    sorted_creation = sorted(creation_dates.items())
    sorted_merges = sorted(merge_dates.items())
    
    combined_stats = {}
    
    for date, count in sorted_creation:
        if date not in combined_stats:
            combined_stats[date] = {"created": 0, "merged": 0}
        combined_stats[date]["created"] = count
    
    for date, count in sorted_merges:
        if date not in combined_stats:
            combined_stats[date] = {"created": 0, "merged": 0}
        combined_stats[date]["merged"] = count
    
    return [
        {"date": date, "created": stats["created"], "merged": stats["merged"]}
        for date, stats in sorted(combined_stats.items())
    ]

def main():
    """メイン処理"""
    pr_data_path = "/home/ubuntu/repos/policy-pr-data/all_pr_data.json"
    
    print(f"PRデータのサンプルを {pr_data_path} から読み込んでいます...")
    pr_data = load_pr_data_sample(pr_data_path, sample_size=500)
    
    if not pr_data:
        print("PRデータが読み込めませんでした。終了します。")
        sys.exit(1)
    
    print(f"{len(pr_data)}件のPRデータサンプルを読み込みました")
    
    print("日次のPR統計を計算しています...")
    stats = extract_daily_pr_stats(pr_data)
    
    print(f"{len(stats)}日分の統計データを生成しました")
    
    print("\n日次PR統計データ:")
    print("日付, PR作成数, PRマージ数")
    for stat in stats:
        print(f"{stat['date']}, {stat['created']}, {stat['merged']}")

if __name__ == "__main__":
    main()
