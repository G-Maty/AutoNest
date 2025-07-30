# AutoNest EXE 化手順書

## 📋 概要

AutoNest ツール（拡張版）を exe ファイルに変換してスタンドアロンで実行可能にする手順です。
現在はドラッグ&ドロップ機能を削除し、シンプルで安定した操作になっています。

## 🔧 必要な環境

- **Python**: 3.7 以上
- **PyInstaller**: 6.0 以上
- **仮想環境**: 推奨（`.venv`フォルダ使用）

## 📦 手順

### 1. 開発環境のセットアップ

```bash
# 仮想環境をアクティベート（Windowsの場合）
.venv\Scripts\activate

# または（Linux/macOSの場合）
source .venv/bin/activate

# 必要なライブラリをインストール
pip install -r requirements_build.txt
```

### 2. EXE 化の実行

#### 🎯 EXE 化の実行（推奨）

```bash
# シンプル版
build_exe_simple.bat
```

#### ⚙️ 手動での EXE 化

```bash
# 拡張版を手動ビルド
pyinstaller --onefile --windowed --name="AutoNest_Advanced" --add-data="config.json;." --add-data="templates;templates" advanced_folder_creator.py
```

### 3. 生成されるファイル

#### 📁 出力先

- `dist/` フォルダ内に EXE ファイルが生成されます

#### 📄 生成されるファイル

- `AutoNest_Advanced.exe` - 拡張版（メインアプリケーション）

### 4. PyInstaller オプション詳細

| オプション   | 説明                          | 使用理由                       |
| ------------ | ----------------------------- | ------------------------------ |
| `--onefile`  | 単一の EXE ファイルとして出力 | 配布の簡便性                   |
| `--windowed` | コンソールウィンドウを非表示  | GUI 専用アプリ                 |
| `--name`     | 出力ファイル名を指定          | 分かりやすい名前               |
| `--add-data` | 追加データファイルを含める    | 設定ファイル・テンプレート同梱 |
| `--upx`      | UPX でファイルサイズを圧縮    | ファイルサイズ削減             |

### 5. 🔍 トラブルシューティング

#### ❌ よくある問題と解決法

**問題 1: ModuleNotFoundError**

```bash
# 隠れた依存関係を明示的に追加
pyinstaller --hidden-import=tkinter.filedialog --hidden-import=tkinter.messagebox --onefile advanced_folder_creator.py
```

**問題 2: ファイルサイズが大きい（50MB 以上）**

```bash
# 不要なモジュールを除外
pyinstaller --onefile --exclude-module=matplotlib --exclude-module=numpy --exclude-module=pandas advanced_folder_creator.py
```

**問題 3: 起動が遅い（10 秒以上）**

- `--onefile`の代わりに`--onedir`を使用（複数ファイル出力）
- ウイルススキャンの除外設定を確認
- SSD の使用を推奨

**問題 4: テンプレートファイルが見つからない**

```bash
# テンプレートフォルダを明示的に含める
pyinstaller --onefile --add-data="templates;templates" advanced_folder_creator.py
```

### 6. 📦 配布用パッケージ作成

#### ✅ 配布前チェックリスト

- [ ] EXE ファイルが正常に起動する
- [ ] フォルダ選択機能が動作する
- [ ] フォルダ・ファイル作成機能が動作する
- [ ] プレビュー機能が動作する
- [ ] ログ表示が正常に動作する
- [ ] 設定ファイルが読み込まれる
- [ ] テンプレートファイルが含まれている
- [ ] README.md を同梱する

#### 📂 推奨配布構成

```
AutoNest_v3.0/
├── AutoNest_Advanced.exe        # メイン実行ファイル
├── config.json                  # 設定ファイル（オプション）
├── templates/                   # テンプレートフォルダ（オプション）
│   └── README.md
├── 配布版README.md              # 使用方法
└── LICENSE                      # ライセンス
```

## 🔧 詳細設定

### spec ファイルを使用した高度なビルド

```bash
# 既存のspecファイルを使用
pyinstaller AutoNest_Advanced.spec
```

## ⚡ パフォーマンス最適化

### 📉 ファイルサイズ削減

```bash
# 最小構成でビルド
pyinstaller --onefile --windowed --strip --optimize=2 advanced_folder_creator.py
```

### 🚀 起動速度向上

```bash
# ディレクトリ形式で出力（起動高速化）
pyinstaller --onedir --windowed advanced_folder_creator.py
```
