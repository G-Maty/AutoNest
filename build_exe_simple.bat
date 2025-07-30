@echo off
echo AutoNest Advanced - EXEファイル作成スクリプト
echo.

REM 仮想環境のPythonパスを設定
set PYTHON_PATH=C:\GIT\AutoNest\.venv\Scripts\python.exe

echo PyInstallerでEXEファイルを作成中...
echo.

echo 拡張版 advanced_folder_creator.py をEXE化しています...
%PYTHON_PATH% -m PyInstaller --onefile --windowed --name="AutoNest_Advanced" --add-data="config.json;." --add-data="templates;templates" advanced_folder_creator.py

echo.
echo EXEファイルの作成が完了しました！
echo distフォルダ内にEXEファイルが作成されています。
echo - AutoNest_Advanced.exe (拡張版)
echo.

pause
