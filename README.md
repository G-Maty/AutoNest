# AutoNest - フォルダ・ファイル自動作成ツール

指定したフォルダ内に自動で複数のフォルダとファイルを作成する Python の GUI ツールです。

## 🎯 機能

- **フォルダ自動作成**: 複数のフォルダ構造を同時作成
- **ファイル自動作成**: テンプレートベースのファイル作成
- **ディレクトリ構造プレビュー**: 作成予定の構造を事前に確認
- **設定ファイルカスタマイズ**: `config.json`で自由にカスタマイズ
- **詳細ログ表示**: すべての処理を確認可能
- **安全設計**: 既存のフォルダ・ファイルは保護

## 🚀 使用方法

### 1. EXE ファイルで実行（推奨）

```bash
# 配布版EXEファイルを使用
AutoNest_Advanced.exe
```

### 2. Python で直接実行（開発者向け）

```bash
# 仮想環境をアクティベート
.venv\Scripts\activate

# アプリケーション実行
python advanced_folder_creator.py
```

### 3. EXE ファイルのビルド（開発者向け）

```bash
# 依存関係をインストール
pip install -r requirements_build.txt

# EXEファイルを作成
build_exe_simple.bat
```

## 📋 GUI 操作手順

1. **フォルダ選択**: 「参照...」ボタンをクリックして対象フォルダを選択
2. **項目選択**: 作成したいフォルダとファイルにチェックを入れる
3. **プレビュー**: 作成予定のディレクトリ構造を確認
4. **実行**: 「フォルダとファイルを作成」ボタンで作成開始

## 📁 作成されるフォルダ構造（デフォルト設定）

```
選択したフォルダ/
├── Assets/
│   ├── Editor/
│   ├── Scripts/
│   └── Textures/
└── README.md （テンプレートから作成）
```

※ `config.json`で自由にカスタマイズ可能

## ⚙️ 設定ファイル（config.json）

```json
{
  "default_folders": [
    "src",
    "src/components",
    "src/styles",
    "src/utils",
    "public",
    "tests",
    "docs"
  ],
  "default_files": [
    {
      "name": "package.json",
      "description": "npm設定ファイル",
      "template_path": "templates/web_package.json",
      "target_path": "package.json"
    },
    {
      "name": "index.html",
      "description": "メインHTMLファイル",
      "template_path": "templates/index.html",
      "target_path": "public/index.html"
    }
  ]
}
```

#### 1. **default_folders** - 作成するフォルダの設定

作成したいフォルダ構造を文字列配列で指定します。

```json
"default_folders": [
    "src",
    "src/components",
    "src/styles",
    "src/utils",
    "public",
    "tests",
    "docs"
  ],
```

#### 2. **default_files** - 作成するファイルの設定

テンプレートベースでファイルを作成する設定です。

```json
"default_files": [
  {
    "name": "README.md",                    // UI表示名（必須）
    "description": "プロジェクト説明ファイル",   // UI表示用説明（省略可）
    "template_path": "templates/README.md",  // テンプレートファイルパス（必須）
    "target_path": "docs/README.md"              // 作成先相対パス（必須）
  },
  {
    "name": ".gitignore",
    "description": "Git除外設定",
    "template_path": "templates/.gitignore",
    "target_path": ".gitignore"
  },
  {
    "name": "package.json",
    "description": "Node.js設定ファイル",
    "template_path": "templates/package.json",
    "target_path": "package.json"
  }
]
```

```json
"window_settings": {
  "width": 700,                             // ウィンドウ幅（ピクセル）
  "height": 600,                            // ウィンドウ高さ（ピクセル）
  "title": "AutoNest - フォルダ自動作成ツール"  // ウィンドウタイトル
},
"log_settings": {
  "max_lines": 1000,    // ログの最大保持行数（古い行は自動削除）
  "auto_scroll": true   // 新しいログが追加時に自動スクロール
}
```

### 💡 設定のコツ

- **フォルダパス**: `/` を使用してネストしたフォルダ構造を指定
- **テンプレートファイル**: `templates/` フォルダ内に実際のファイルを配置
- **target_path**: 作成先の相対パス。サブディレクトリも指定可能
- **バックアップ**: 設定変更前に `config.json` をコピーして保存推奨

## ✨ 特徴

- **安全性**: 既存のフォルダ・ファイルは上書きしません
- **視覚的フィードバック**: 詳細なログでプロセスを確認可能
- **エラーハンドリング**: 適切なエラーメッセージを表示
- **使いやすさ**: 直感的な GUI インターフェース
- **柔軟性**: 設定ファイルで自由にカスタマイズ
- **プレビュー機能**: 作成前に構造を確認可能

## 📦 ファイル構成

```
AutoNest/
├── advanced_folder_creator.py    # メインアプリケーション
├── config.json                   # 設定ファイル
├── templates/                    # テンプレートファイル
│   └── README.md
├── build_exe_simple.bat         # EXE作成スクリプト
├── requirements.txt             # Python依存関係
├── requirements_build.txt       # ビルド用依存関係
└── dist/                        # EXE出力先
    └── AutoNest_Advanced.exe
```

## 🖥️ システム要件

### 実行環境

- **OS**: Windows 10/11, macOS, Linux
- **Python**: 3.7 以上（Python 実行の場合）
- **メモリ**: 100MB 以上

### 開発環境

- **Python**: 3.7 以上
- **ライブラリ**: tkinter（標準ライブラリ）
- **ビルド**: PyInstaller 6.0 以上
