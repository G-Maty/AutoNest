# AutoNest EXE 化手順書

## 概要

AutoNest ツールを exe ファイルに変換してスタンドアロンで実行可能にする手順です。

## 必要な環境

- Python 3.6 以上
- PyInstaller
- 仮想環境（推奨）

## 手順

### 0. プロジェクト準備

#### .gitignore の設定

開発に必要のないファイルをGit管理対象外にするため、プロジェクトルートに`.gitignore`が設定されています：

```gitignore
# Python関連（__pycache__、*.pyc等）
# 仮想環境（.venv、venv/等）
# PyInstaller関連（build/、dist/、*.spec等）
# IDE・エディタ関連（.vscode/、.idea/等）
# OS関連（.DS_Store、Thumbs.db等）
# 実行ファイル（*.exe）
```

### 1. PyInstaller のインストール

```bash
# 仮想環境内で実行
pip install pyinstaller
```

### 2. EXE 化の実行

#### EXE 化の実行（推奨）

```bash
build_exe_simple.bat
```

#### 手動での EXE 化

```bash
# 基本版
pyinstaller --onefile --windowed --name="AutoNest" folder_creator.py

# 拡張版
pyinstaller --onefile --windowed --name="AutoNest_Advanced" --add-data="config.json;." advanced_folder_creator.py
```

### 3. 生成されるファイル

#### 出力先

- `dist/` フォルダ内に EXE ファイルが生成されます

#### 生成されるファイル

- `AutoNest.exe` - 基本版
- `AutoNest_Advanced.exe` - 拡張版

### 4. PyInstaller オプション説明

| オプション   | 説明                                   |
| ------------ | -------------------------------------- |
| `--onefile`  | 単一の EXE ファイルとして出力          |
| `--windowed` | コンソールウィンドウを非表示（GUI 用） |
| `--name`     | 出力ファイル名を指定                   |
| `--add-data` | 追加データファイルを含める             |
| `--upx`      | UPX でファイルサイズを圧縮             |

### 5. トラブルシューティング

#### よくある問題と解決法

**問題 1: ModuleNotFoundError**

```bash
# 隠れた依存関係を明示的に追加
pyinstaller --hidden-import=tkinter.filedialog --onefile folder_creator.py
```

**問題 2: ファイルサイズが大きい**

```bash
# 不要なモジュールを除外
pyinstaller --onefile --exclude-module=matplotlib --exclude-module=numpy folder_creator.py
```

**問題 3: 起動が遅い**

- `--onefile`の代わりに`--onedir`を使用（複数ファイル出力）
- ウイルススキャンの除外設定を確認

### 6. 配布用パッケージ作成

#### 配布前チェックリスト

- [ ] EXE ファイルが正常に起動する
- [ ] 全ての機能が動作する
- [ ] 必要な設定ファイルが含まれている
- [ ] README.md を同梱する

#### 推奨配布構成

```
AutoNest_v1.0/
├── AutoNest.exe              # 基本版
├── AutoNest_Advanced.exe     # 拡張版
├── config.json              # 設定ファイル
├── README.md               # 使用方法
└── LICENSE                 # ライセンス
```

## 詳細設定

### spec ファイルを使用した高度なビルド

```bash
# specファイルを使用
pyinstaller autonest.spec
```

## パフォーマンス最適化

### ファイルサイズ削減

```bash
# 最小構成でビルド
pyinstaller --onefile --windowed --strip --upx-dir=upx folder_creator.py
```

### 起動速度向上

```bash
# ディレクトリ形式で出力（起動高速）
pyinstaller --onedir --windowed folder_creator.py
```

## 注意事項

1. **ウイルススキャン**: 生成された EXE ファイルが誤検知される可能性があります
2. **ファイルサイズ**: 単一 EXE ファイルは 20-50MB 程度になります
3. **互換性**: 生成された EXE は同じ OS/アーキテクチャでのみ動作します
4. **設定ファイル**: `config.json`は必要に応じて同じフォルダに配置してください
