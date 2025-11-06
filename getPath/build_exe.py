#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
建置腳本 - 將 getPath.py 打包成 .exe 檔案
"""

import os
import subprocess
import sys

def main():
    print("=== GetPath 建置工具 ===\n")
    
    # 檢查是否安裝 PyInstaller
    try:
        import PyInstaller
        print("✓ PyInstaller 已安裝")
    except ImportError:
        print("× PyInstaller 未安裝")
        print("\n正在安裝 PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("✓ PyInstaller 安裝完成\n")
    
    # 建置參數
    script_path = os.path.join("src", "getPath.py")
    
    # PyInstaller 命令
    cmd = [
        "pyinstaller",
        "--onefile",           # 打包成單一檔案
        "--console",           # 顯示控制台視窗（互動式程式需要）
        "--name=GetPath",      # 輸出檔案名稱
        "--clean",             # 清理暫存檔案
        script_path
    ]
    
    print("開始建置 .exe 檔案...")
    print(f"命令: {' '.join(cmd)}\n")
    
    try:
        subprocess.check_call(cmd)
        print("\n" + "="*50)
        print("✓ 建置完成！")
        print(f"✓ 執行檔位置: {os.path.join('dist', 'GetPath.exe')}")
        print("="*50)
    except subprocess.CalledProcessError as e:
        print(f"\n× 建置失敗: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

