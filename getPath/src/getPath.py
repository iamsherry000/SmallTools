#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Get Path - 從 SharePoint URL 中提取乾淨的路徑
"""

import urllib.parse
import re
from typing import Optional


def extract_path_from_sharepoint_url(url: str, folder_only: bool = False) -> Optional[str]:
    """
    從 SharePoint URL 中提取乾淨的路徑
    
    支援兩種 SharePoint URL 格式：
    1. 帶 'id' 參數的格式：...?id=/sites/xxx/Shared%20Documents/...
    2. 直接路徑格式：.../:u:/r/sites/xxx/Shared%20Documents/...
    
    Args:
        url: SharePoint URL
        folder_only: 如果為 True，只回傳資料夾路徑（不包含檔名）
        
    Returns:
        提取並清理後的路徑，如果無法解析則返回 None
    """
    try:
        # 解析 URL
        parsed_url = urllib.parse.urlparse(url)
        path = None
        
        # 方法 1: 從查詢參數中的 'id' 取得路徑
        query_params = urllib.parse.parse_qs(parsed_url.query)
        if 'id' in query_params:
            path = query_params['id'][0]
        
        # 方法 2: 從 URL 路徑本身提取（適用於 /:u:/r/ 或 /:f:/ 格式）
        if not path:
            url_path = parsed_url.path
            # URL 解碼
            decoded_url_path = urllib.parse.unquote(url_path)
            
            # 檢查是否包含 /sites/ 路徑
            if '/sites/' in decoded_url_path:
                # 找到 /sites/ 的位置
                sites_index = decoded_url_path.find('/sites/')
                path = decoded_url_path[sites_index:]
                
                # 移除查詢參數（如 ?csf=1&web=1 等）
                if '?' in path:
                    path = path.split('?')[0]
        
        if not path:
            return None
        
        # URL 解碼（如果還沒解碼）
        decoded_path = urllib.parse.unquote(path)
        
        # 移除開頭的 /sites/xxx/Shared Documents/ 部分
        # 使用正則表達式匹配常見的 SharePoint 路徑前綴
        pattern = r'^/sites/[^/]+/Shared\s+Documents/'
        cleaned_path = re.sub(pattern, '', decoded_path, flags=re.IGNORECASE)
        
        # 如果路徑以 / 開頭，移除它
        if cleaned_path.startswith('/'):
            cleaned_path = cleaned_path[1:]
        
        # 將反斜線轉換為正斜線（如果有的話）
        cleaned_path = cleaned_path.replace('\\', '/')
        
        # 如果只需要資料夾路徑，移除檔名
        if folder_only and cleaned_path:
            # 找到最後一個 / 的位置
            last_slash = cleaned_path.rfind('/')
            if last_slash != -1:
                cleaned_path = cleaned_path[:last_slash]
        
        return cleaned_path
        
    except Exception as e:
        print(f"解析錯誤: {e}")
        return None


def main():
    """主程式"""
    print("=== SharePoint URL 路徑提取工具 ===\n")
    
    # 測試範例 1: 帶 id 參數的格式
    test_url1 = (
        "https://hp.sharepoint.com/sites/BPSsecurityValidationlab/Shared%20Documents/"
        "Forms/AllItems.aspx?id=%2Fsites%2FBPSsecurityValidationlab%2FShared%20Documents%2F"
        "SVL%20Files%2FTest%20Tools%20and%20Documents%2FIntel%20Tools%2FIntel%20BLDT%2F"
        "bldt%2Dnda%5Fsetup%2D2%2E7%2E0%2Ezip&parent=%2Fsites%2FBPSsecurityValidationlab%2F"
        "Shared%20Documents%2FSVL%20Files%2FTest%20Tools%20and%20Documents%2FIntel%20Tools%2F"
        "Intel%20BLDT"
    )
    
    # 測試範例 2: 直接路徑格式
    test_url2 = (
        "https://hp.sharepoint.com/:u:/r/sites/BPSsecurityValidationlab/"
        "Shared%20Documents/SVL%20Files/Intel%20BLDT%20(Battery%20Life%20Diagnostic%20Tool)/"
        "2024_Masada/24ww52_MasadaN_X90_010106%20RTM/Intel%20Tools%20and%20docs/"
        "Tools%20to%20Go/Browser_Tabs50.bat?csf=1&web=1&e=MFj81M"
    )
    
    print("【測試 1】帶 id 參數的格式:")
    print(test_url1)
    result1 = extract_path_from_sharepoint_url(test_url1)
    print("\n提取的路徑:")
    print(result1 if result1 else "無法提取路徑")
    
    print("\n" + "="*50 + "\n")
    
    print("【測試 2】直接路徑格式:")
    print(test_url2)
    result2 = extract_path_from_sharepoint_url(test_url2)
    print("\n提取的路徑:")
    print(result2 if result2 else "無法提取路徑")
    
    print("\n" + "="*50 + "\n")
    
    # 互動模式
    while True:
        user_input = input("請輸入 SharePoint URL (或輸入 'q' 離開): ").strip()
        
        if user_input.lower() == 'q':
            print("再見！")
            break
            
        if not user_input:
            continue
        
        # 如果 URL 包含換行符號，自動處理
        user_input = user_input.replace('\n', '').replace('\r', '')
        
        result = extract_path_from_sharepoint_url(user_input)
        
        if result:
            print(f"提取的路徑: {result}\n")
        else:
            print("無法提取路徑，請確認 URL 格式是否正確\n")


if __name__ == "__main__":
    main()

