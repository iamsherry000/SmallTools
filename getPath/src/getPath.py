#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Get Path - 從 SharePoint URL 中提取乾淨的路徑
"""

import urllib.parse
import re
from typing import Optional


def extract_path_from_sharepoint_url(url: str) -> Optional[str]:
    """
    從 SharePoint URL 中提取乾淨的路徑
    
    Args:
        url: SharePoint URL
        
    Returns:
        提取並清理後的路徑，如果無法解析則返回 None
    """
    try:
        # 解析 URL
        parsed_url = urllib.parse.urlparse(url)
        
        # 取得查詢參數
        query_params = urllib.parse.parse_qs(parsed_url.query)
        
        # 從 'id' 參數中取得路徑
        if 'id' not in query_params:
            return None
            
        path = query_params['id'][0]
        
        # URL 解碼
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
        
        return cleaned_path
        
    except Exception as e:
        print(f"解析錯誤: {e}")
        return None


def main():
    """主程式"""
    print("=== SharePoint URL 路徑提取工具 ===\n")
    
    # 測試範例
    test_url = (
        "https://hp.sharepoint.com/sites/BPSsecurityValidationlab/Shared%20Documents/"
        "Forms/AllItems.aspx?id=%2Fsites%2FBPSsecurityValidationlab%2FShared%20Documents%2F"
        "SVL%20Files%2FTest%20Tools%20and%20Documents%2FIntel%20Tools%2FIntel%20BLDT%2F"
        "bldt%2Dnda%5Fsetup%2D2%2E7%2E0%2Ezip&parent=%2Fsites%2FBPSsecurityValidationlab%2F"
        "Shared%20Documents%2FSVL%20Files%2FTest%20Tools%20and%20Documents%2FIntel%20Tools%2F"
        "Intel%20BLDT"
    )
    
    print("測試 URL:")
    print(test_url)
    print("\n提取的路徑:")
    
    result = extract_path_from_sharepoint_url(test_url)
    if result:
        print(result)
    else:
        print("無法提取路徑")
    
    print("\n" + "="*50 + "\n")
    
    # 互動模式
    while True:
        user_input = input("請輸入 SharePoint URL (或輸入 'q' 離開): ").strip()
        
        if user_input.lower() == 'q':
            print("再見！")
            break
            
        if not user_input:
            continue
            
        result = extract_path_from_sharepoint_url(user_input)
        if result:
            print(f"提取的路徑: {result}\n")
        else:
            print("無法提取路徑，請確認 URL 格式是否正確\n")


if __name__ == "__main__":
    main()

