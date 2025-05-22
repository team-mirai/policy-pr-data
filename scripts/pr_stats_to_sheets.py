#!/usr/bin/env python3
"""
PRデータを分析して日次のPR作成数とマージ数を抽出し、Google Sheetsに書き込むスクリプト

このスクリプトは以下の機能を持ちます:
1. all_pr_data.jsonからPRデータを読み込む
2. 日次のPR作成数とマージ数を計算する
3. Google Sheetsに結果を書き込む

このスクリプトはGitHub Actionsワークフローから定期的に実行されます。
"""

import json
import os
import datetime
from collections import defaultdict
import sys
from pathlib import Path

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SPREADSHEET_ID = "1g5grA476vtsWO4M-Vb6oWibFeGlNXuwT13M4I3VSE5E"
SHEET_NAME = "PR統計"  # スプレッドシートのタブ名

def load_pr_data(json_path):
    """PRデータをJSONファイルから読み込む"""
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            return json.load(f)
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

def get_sheets_service():
    """Google Sheets APIのサービスを取得する"""
    try:
        credentials_path = os.environ.get("GOOGLE_SHEETS_CREDENTIALS_PATH", "service_account_credentials.json")
        
        SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
        
        credentials = service_account.Credentials.from_service_account_file(
            credentials_path, scopes=SCOPES
        )
        
        service = build("sheets", "v4", credentials=credentials)
        
        return service
    except Exception as e:
        print(f"Sheets APIサービスの取得中にエラーが発生しました: {e}")
        return None

def write_to_sheets(stats):
    """統計データをGoogle Sheetsに書き込む"""
    try:
        service = get_sheets_service()
        if not service:
            return False
            
        rows = [["日付", "PR作成数", "PRマージ数"]]  # ヘッダー行
        for stat in stats:
            rows.append([stat["date"], stat["created"], stat["merged"]])
        
        sheet_metadata = service.spreadsheets().get(spreadsheetId=SPREADSHEET_ID).execute()
        sheets = sheet_metadata.get("sheets", [])
        sheet_exists = False
        
        for sheet in sheets:
            if sheet.get("properties", {}).get("title") == SHEET_NAME:
                sheet_exists = True
                break
        
        if not sheet_exists:
            body = {
                "requests": [{
                    "addSheet": {
                        "properties": {
                            "title": SHEET_NAME
                        }
                    }
                }]
            }
            service.spreadsheets().batchUpdate(
                spreadsheetId=SPREADSHEET_ID, body=body
            ).execute()
        
        body = {
            "values": rows
        }
        
        result = service.spreadsheets().values().update(
            spreadsheetId=SPREADSHEET_ID,
            range=f"{SHEET_NAME}!A1",
            valueInputOption="RAW",
            body=body
        ).execute()
        
        print(f"{result.get('updatedCells')}セルを更新しました")
        return True
    except HttpError as error:
        print(f"Google Sheets APIエラー: {error}")
        return False
    except Exception as e:
        print(f"スプレッドシートへの書き込み中にエラーが発生しました: {e}")
        return False

def main():
    """メイン処理"""
    pr_data_path = "all_pr_data.json"
    
    print(f"PRデータを {pr_data_path} から読み込んでいます...")
    pr_data = load_pr_data(pr_data_path)
    
    if not pr_data:
        print("PRデータが読み込めませんでした。終了します。")
        sys.exit(1)
    
    print(f"{len(pr_data)}件のPRデータを読み込みました")
    
    print("日次のPR統計を計算しています...")
    stats = extract_daily_pr_stats(pr_data)
    
    print(f"{len(stats)}日分の統計データを生成しました")
    
    if stats:
        recent_stats = stats[-min(5, len(stats)):]
        print("\n最近の統計データ:")
        for stat in recent_stats:
            print(f"{stat['date']}: 作成 {stat['created']}件, マージ {stat['merged']}件")
    
    print("\nGoogle Sheetsに書き込んでいます...")
    success = write_to_sheets(stats)
    
    if success:
        print("Google Sheetsへの書き込みが完了しました")
    else:
        print("Google Sheetsへの書き込みに失敗しました")
        sys.exit(1)

if __name__ == "__main__":
    main()
