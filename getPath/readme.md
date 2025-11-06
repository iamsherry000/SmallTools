# Get Path 
去除多餘的雜訊，把正確路徑回傳出來

## 功能說明
從 SharePoint URL 中提取乾淨的檔案路徑，自動去除網站前綴和雜訊。

## 使用方式

### 方式 1: 使用 .exe 檔案（推薦）
直接執行 `dist/GetPath.exe`，無需安裝 Python。

### 方式 2: 使用 Python 腳本
```bash
python src/getPath.py
```

### 方式 3: 作為模組使用
```python
from src.getPath import extract_path_from_sharepoint_url

url = "https://hp.sharepoint.com/sites/BPSsecurityValidationlab/..."
clean_path = extract_path_from_sharepoint_url(url)
print(clean_path)
```

## 建置 .exe 檔案

如果需要重新建置 .exe 檔案：

```bash
# 安裝建置工具
pip install -r requirements.txt

# 執行建置腳本
python build_exe.py
```

建置完成後，.exe 檔案會在 `dist/GetPath.exe`

## 範例

**輸入 URL:**
```
https://hp.sharepoint.com/sites/BPSsecurityValidationlab/Shared%20Documents/Forms/AllItems.aspx?id=%2Fsites%2FBPSsecurityValidationlab%2FShared%20Documents%2FSVL%20Files%2FTest%20Tools%20and%20Documents%2FIntel%20Tools%2FIntel%20BLDT%2Fbldt%2Dnda%5Fsetup%2D2%2E7%2E0%2Ezip
```

**輸出路徑:**
```
SVL Files/Test Tools and Documents/Intel Tools/Intel BLDT/bldt-nda_setup-2.7.0.zip
```

## 系統需求

### 使用 .exe 檔案
- Windows 作業系統
- 無需安裝 Python

### 使用 Python 腳本
- Python 3.6 或以上版本
- 無需額外安裝套件（使用標準函式庫）