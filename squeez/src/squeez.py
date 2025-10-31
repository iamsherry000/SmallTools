#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Squeez - 壓縮子資料夾工具
當資料夾中有太多子資料夾時，將每個子資料夾壓縮成 zip 檔案並刪除原本的資料夾
"""

import os
import shutil
import zipfile
import argparse
from pathlib import Path
from typing import List
from tkinter import Tk, filedialog


def count_files_in_folder(folder_path: Path) -> int:
    """
    計算資料夾中的檔案總數（包含子資料夾）
    
    Args:
        folder_path: 資料夾路徑
    
    Returns:
        int: 檔案總數
    """
    count = 0
    for root, dirs, files in os.walk(folder_path):
        count += len(files)
    return count


def verify_zip_integrity(zip_path: Path, expected_file_count: int, folder_name: str) -> bool:
    """
    驗證 ZIP 檔案的完整性
    
    Args:
        zip_path: ZIP 檔案路徑
        expected_file_count: 預期的檔案數量
        folder_name: 資料夾名稱（用於顯示）
    
    Returns:
        bool: ZIP 檔案是否完整且正確
    """
    try:
        with zipfile.ZipFile(zip_path, 'r') as zipf:
            # 測試 ZIP 檔案完整性
            bad_file = zipf.testzip()
            if bad_file is not None:
                print(f"❌ ZIP 檔案損壞，發現錯誤: {bad_file}")
                return False
            
            # 檢查檔案數量是否正確
            zip_file_count = len([name for name in zipf.namelist() if not name.endswith('/')])
            if zip_file_count != expected_file_count:
                print(f"❌ 檔案數量不符！原始: {expected_file_count} 個，ZIP 中: {zip_file_count} 個")
                return False
            
            return True
    except Exception as e:
        print(f"❌ 驗證 ZIP 檔案時發生錯誤: {str(e)}")
        return False


def zip_folder(folder_path: Path, output_path: Path) -> bool:
    """
    壓縮資料夾成 zip 檔案，並確保檔案完整性
    
    Args:
        folder_path: 要壓縮的資料夾路徑
        output_path: 輸出的 zip 檔案路徑
    
    Returns:
        bool: 是否成功壓縮且驗證通過
    """
    try:
        # 先計算原始檔案數量
        original_file_count = count_files_in_folder(folder_path)
        
        if original_file_count == 0:
            print(f"⚠️  資料夾是空的")
            return False
        
        # 壓縮資料夾
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    # 計算相對路徑，避免包含完整路徑
                    arcname = os.path.relpath(file_path, folder_path.parent)
                    zipf.write(file_path, arcname)
        
        # 驗證 ZIP 檔案完整性
        if not verify_zip_integrity(output_path, original_file_count, folder_path.name):
            # 驗證失敗，刪除損壞的 ZIP 檔案
            if output_path.exists():
                os.remove(output_path)
            return False
        
        return True
    except Exception as e:
        print(f"❌ 壓縮失敗 {folder_path.name}: {str(e)}")
        # 如果壓縮失敗，刪除可能不完整的 ZIP 檔案
        if output_path.exists():
            try:
                os.remove(output_path)
            except:
                pass
        return False


def select_directory() -> Path:
    """
    使用圖形介面選擇目錄
    
    Returns:
        Path: 選擇的目錄路徑，如果取消則返回 None
    """
    print("請選擇要處理的資料夾...")
    root = Tk()
    root.withdraw()  # 隱藏主視窗
    root.attributes('-topmost', True)  # 將對話框置於最上層
    
    folder_path = filedialog.askdirectory(
        title='選擇要壓縮子資料夾的目錄',
        mustexist=True
    )
    
    root.destroy()
    
    if folder_path:
        return Path(folder_path)
    return None


def get_subfolders(directory: Path) -> List[Path]:
    """
    取得指定目錄下的所有子資料夾
    
    Args:
        directory: 目標目錄
    
    Returns:
        List[Path]: 子資料夾列表
    """
    return [item for item in directory.iterdir() if item.is_dir()]


def squeez_subfolders(target_dir: Path, min_count: int = 1, dry_run: bool = False) -> None:
    """
    壓縮目錄下的所有子資料夾
    
    Args:
        target_dir: 目標目錄
        min_count: 最少子資料夾數量才執行壓縮（預設為 1）
        dry_run: 是否只模擬執行，不實際壓縮和刪除
    """
    if not target_dir.exists():
        print(f"❌ 目錄不存在: {target_dir}")
        return
    
    if not target_dir.is_dir():
        print(f"❌ 指定路徑不是目錄: {target_dir}")
        return
    
    subfolders = get_subfolders(target_dir)
    
    if len(subfolders) == 0:
        print(f"ℹ️  目錄中沒有子資料夾: {target_dir}")
        return
    
    if len(subfolders) < min_count:
        print(f"ℹ️  子資料夾數量 ({len(subfolders)}) 少於最小值 ({min_count})，不執行壓縮")
        return
    
    print(f"📁 找到 {len(subfolders)} 個子資料夾")
    print(f"📍 目標目錄: {target_dir.absolute()}\n")
    
    if dry_run:
        print("🔍 模擬模式 - 不會實際壓縮或刪除檔案\n")
    
    success_count = 0
    fail_count = 0
    
    for idx, folder in enumerate(subfolders, 1):
        folder_name = folder.name
        zip_name = f"{folder_name}.zip"
        zip_path = target_dir / zip_name
        
        print(f"\n[{idx}/{len(subfolders)}] 處理: {folder_name}")
        
        if zip_path.exists():
            print(f"  ⚠️  跳過 - zip 檔案已存在")
            continue
        
        if dry_run:
            file_count = count_files_in_folder(folder)
            print(f"  📄 檔案數量: {file_count} 個")
            print(f"  ✓ (模擬)")
            success_count += 1
            continue
        
        # 計算並顯示檔案數量
        file_count = count_files_in_folder(folder)
        print(f"  📄 檔案數量: {file_count} 個")
        print(f"  🗜️  正在壓縮...", end=" ")
        
        # 壓縮資料夾（已內建完整性驗證）
        if zip_folder(folder, zip_path):
            print(f"完成")
            print(f"  ✅ 壓縮驗證通過")
            
            # 確認 zip 檔案已建立且完整
            if zip_path.exists():
                # 刪除原始資料夾
                print(f"  🗑️  刪除原始資料夾...", end=" ")
                try:
                    shutil.rmtree(folder)
                    print(f"完成")
                    print(f"  ✓ 成功完成")
                    success_count += 1
                except Exception as e:
                    print(f"失敗")
                    print(f"  ⚠️  壓縮成功但刪除失敗: {str(e)}")
                    print(f"  💡 ZIP 檔案已保留，請手動刪除原始資料夾")
                    fail_count += 1
            else:
                print(f"  ❌ 壓縮檔案建立失敗")
                fail_count += 1
        else:
            print(f"失敗")
            print(f"  ❌ 壓縮失敗或驗證未通過，原始資料夾已保留")
            fail_count += 1
    
    # 顯示統計
    print(f"\n{'='*50}")
    print(f"✅ 成功: {success_count} 個")
    if fail_count > 0:
        print(f"❌ 失敗: {fail_count} 個")
    print(f"{'='*50}")


def main():
    """主程式進入點"""
    parser = argparse.ArgumentParser(
        description='Squeez - 壓縮子資料夾工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
範例:
  python squeez.py                      # 使用圖形介面選擇目錄
  python squeez.py .                    # 壓縮當前目錄的所有子資料夾
  python squeez.py C:\\MyFolder          # 壓縮指定目錄的所有子資料夾
  python squeez.py --gui                # 強制使用圖形介面選擇
  python squeez.py . --min-count 5      # 只在子資料夾數量 >= 5 時才執行
  python squeez.py . --dry-run          # 模擬執行，不實際壓縮
        """
    )
    
    parser.add_argument(
        'directory',
        type=str,
        nargs='?',
        default=None,
        help='要處理的目錄路徑（不指定則使用圖形介面選擇）'
    )
    
    parser.add_argument(
        '--gui',
        action='store_true',
        help='使用圖形介面選擇目錄'
    )
    
    parser.add_argument(
        '--min-count',
        type=int,
        default=1,
        help='最少子資料夾數量才執行壓縮（預設為 1）'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='模擬執行，不實際壓縮和刪除'
    )
    
    args = parser.parse_args()
    
    print("=" * 50)
    print("Squeez - 壓縮子資料夾工具")
    print("=" * 50 + "\n")
    
    # 決定目標路徑
    if args.gui or args.directory is None:
        # 使用圖形介面選擇
        target_path = select_directory()
        if target_path is None:
            print("❌ 未選擇任何目錄，程式結束")
            return
    else:
        # 使用命令列參數
        target_path = Path(args.directory).resolve()
    
    squeez_subfolders(target_path, args.min_count, args.dry_run)


if __name__ == "__main__":
    main()

