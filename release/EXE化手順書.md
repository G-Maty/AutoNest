# AutoNest EXE化手順書

## 概要
AutoNestツールをexeファイルに変換してスタンドアロンで実行可能にする手順です。

## 必要な環境
- Python 3.6以上
- PyInstaller
- 仮想環境（推奨）

## 手順

### 1. PyInstallerのインストール
```bash
# 仮想環境内で実行
pip install pyinstaller
```

### 2. EXE化の実行

#### 簡単な方法（推奨）
```bash
# アイコンなし版（推奨）
build_exe_simple.bat
```

#### カスタムアイコンを使用する場合
1. `icon.ico`ファイルをプロジェクトルートに配置
2. 以下を実行:
```bash
build_exe.bat
```

#### 手動でのEXE化
```bash
# 基本版
pyinstaller --onefile --windowed --name="AutoNest" folder_creator.py

# 拡張版
pyinstaller --onefile --windowed --name="AutoNest_Advanced" --add-data="config.json;." advanced_folder_creator.py
```

### 3. 生成されるファイル

#### 出力先
- `dist/` フォルダ内にEXEファイルが生成されます

#### 生成されるファイル
- `AutoNest.exe` - 基本版
- `AutoNest_Advanced.exe` - 拡張版

### 4. PyInstallerオプション説明

| オプション | 説明 |
|-----------|------|
| `--onefile` | 単一のEXEファイルとして出力 |
| `--windowed` | コンソールウィンドウを非表示（GUI用） |
| `--name` | 出力ファイル名を指定 |
| `--icon` | アイコンファイルを指定 |
| `--add-data` | 追加データファイルを含める |
| `--upx` | UPXでファイルサイズを圧縮 |

### 5. トラブルシューティング

#### よくある問題と解決法

**問題1: ModuleNotFoundError**
```bash
# 隠れた依存関係を明示的に追加
pyinstaller --hidden-import=tkinter.filedialog --onefile folder_creator.py
```

**問題2: ファイルサイズが大きい**
```bash
# 不要なモジュールを除外
pyinstaller --onefile --exclude-module=matplotlib --exclude-module=numpy folder_creator.py
```

**問題3: 起動が遅い**
- `--onefile`の代わりに`--onedir`を使用（複数ファイル出力）
- ウイルススキャンの除外設定を確認

### 6. 配布用パッケージ作成

#### 配布前チェックリスト
- [ ] EXEファイルが正常に起動する
- [ ] 全ての機能が動作する  
- [ ] 必要な設定ファイルが含まれている
- [ ] README.mdを同梱する

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

### specファイルを使用した高度なビルド
```bash
# specファイルを使用
pyinstaller autonest.spec
```

### カスタムアイコンの作成
- 推奨サイズ: 256x256, 128x128, 64x64, 32x32, 16x16
- 形式: ICO形式
- オンラインツール: [ConvertICO](https://convertio.co/ja/png-ico/)

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

1. **ウイルススキャン**: 生成されたEXEファイルが誤検知される可能性があります
2. **ファイルサイズ**: 単一EXEファイルは20-50MB程度になります
3. **互換性**: 生成されたEXEは同じOS/アーキテクチャでのみ動作します
4. **設定ファイル**: `config.json`は必要に応じて同じフォルダに配置してください
