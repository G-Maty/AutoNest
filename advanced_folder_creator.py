#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
フォルダ自動作成ツール (AutoNest) - 拡張版
設定ファイルに対応し、複数のフォルダ構造を作成できるGUIツール
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import sys
import json
import shutil
import time
from pathlib import Path


class AdvancedFolderCreatorApp:
    def __init__(self, root):
        self.root = root
        self.config = self.load_config()

        # 設定に基づいてウィンドウを設定
        window_config = self.config.get("window_settings", {})
        self.root.title(window_config.get("title", "AutoNest - フォルダ自動作成ツール"))
        width = window_config.get("width", 700)
        height = window_config.get("height", 500)
        self.root.geometry(f"{width}x{height}")
        self.root.resizable(True, True)

        # 選択されたフォルダパス
        self.selected_folder = tk.StringVar()

        # フォルダ作成リスト
        self.folder_vars = {}
        
        # ファイル作成リスト
        self.file_vars = {}

        self.setup_ui()

    def load_config(self):
        """設定ファイルを読み込む"""
        config_file = "config.json"
        try:
            if os.path.exists(config_file):
                with open(config_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            else:
                return self.get_default_config()
        except Exception as e:
            print(f"設定ファイル読み込みエラー: {e}")
            return self.get_default_config()

    def get_default_config(self):
        """デフォルト設定を返す"""
        return {
            "default_folders": ["Assets/Editor"],
            "default_files": [
                {
                    "name": ".gitignore",
                    "description": "Git無視ファイル",
                    "template_path": "templates/.gitignore",
                    "target_path": ".gitignore"
                }
            ],
            "window_settings": {
                "width": 700,
                "height": 600,
                "title": "AutoNest - フォルダ自動作成ツール",
            },
            "log_settings": {"max_lines": 1000, "auto_scroll": True},
        }

    def setup_ui(self):
        """UIコンポーネントを設定"""
        # メインフレーム
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # ルートをグリッドで拡張可能にする
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)

        # タイトル
        title_label = ttk.Label(
            main_frame,
            text="AutoNest - フォルダ自動作成ツール",
            font=("Arial", 16, "bold"),
        )
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))

        # フォルダ選択セクション
        folder_frame = ttk.LabelFrame(
            main_frame, text="対象フォルダの選択", padding="10"
        )
        folder_frame.grid(
            row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10)
        )
        folder_frame.columnconfigure(1, weight=1)

        ttk.Label(folder_frame, text="選択フォルダ:").grid(
            row=0, column=0, sticky=tk.W, padx=(0, 10)
        )

        folder_entry = ttk.Entry(
            folder_frame, textvariable=self.selected_folder, state="readonly", width=50
        )
        folder_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))

        browse_button = ttk.Button(
            folder_frame, text="参照...", command=self.browse_folder
        )
        browse_button.grid(row=0, column=2, sticky=tk.W)

        # フォルダ・ファイル選択セクション（水平配置）
        selection_frame = ttk.Frame(main_frame)
        selection_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        selection_frame.columnconfigure(0, weight=1)
        selection_frame.columnconfigure(1, weight=1)
        
        # フォルダ選択セクション（左側）
        self.setup_folder_selection_frame(selection_frame, column=0)
        
        # ファイル選択セクション（右側）
        self.setup_file_selection_frame(selection_frame, column=1)
        
        # プレビューセクション
        self.setup_preview_frame(main_frame)

        # ボタンフレーム
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=4, column=0, columnspan=3, pady=10)

        # 作成ボタン
        create_button = ttk.Button(
            button_frame, text="フォルダとファイルを作成", command=self.create_folders_and_files
        )
        create_button.grid(row=0, column=0, padx=(0, 10))

        # 全選択/全解除ボタン
        select_all_button = ttk.Button(
            button_frame, text="全て選択", command=self.select_all_folders
        )
        select_all_button.grid(row=0, column=1, padx=(0, 10))

        deselect_all_button = ttk.Button(
            button_frame, text="全て解除", command=self.deselect_all_folders
        )
        deselect_all_button.grid(row=0, column=2, padx=(0, 10))

        # ログフレーム
        log_frame = ttk.LabelFrame(main_frame, text="ログ", padding="10")
        log_frame.grid(
            row=5, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0)
        )
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(5, weight=1)

        # ログテキストエリア（スクロールバー付き）
        self.log_text = tk.Text(log_frame, height=8, wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(
            log_frame, orient=tk.VERTICAL, command=self.log_text.yview
        )
        self.log_text.configure(yscrollcommand=scrollbar.set)

        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))

        # ログクリアボタン
        clear_log_button = ttk.Button(
            log_frame, text="ログクリア", command=self.clear_log
        )
        clear_log_button.grid(row=1, column=0, sticky=tk.W, pady=(5, 0))

    def setup_folder_selection_frame(self, parent, column=0):
        """フォルダ選択フレームを設定"""
        folder_selection_frame = ttk.LabelFrame(
            parent, text="作成するフォルダを選択", padding="10"
        )
        folder_selection_frame.grid(
            row=0, column=column, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5 if column == 0 else 0)
        )
        folder_selection_frame.columnconfigure(0, weight=1)

        # スクロール可能なフレーム
        canvas = tk.Canvas(folder_selection_frame, height=80)
        scrollbar_folder = ttk.Scrollbar(
            folder_selection_frame, orient="vertical", command=canvas.yview
        )
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar_folder.set)

        canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar_folder.grid(row=0, column=1, sticky=(tk.N, tk.S))

        # 設定からフォルダリストを読み込んでチェックボックスを作成
        default_folders = self.config.get("default_folders", [])
        for i, folder_path in enumerate(default_folders):
            var = tk.BooleanVar(value=True)  # デフォルトで選択
            # チェックボックスの変更時にプレビューを更新
            var.trace_add("write", lambda *args: self.update_preview())
            self.folder_vars[folder_path] = var

            checkbox = ttk.Checkbutton(scrollable_frame, text=folder_path, variable=var)
            checkbox.grid(row=i, column=0, sticky=tk.W, padx=10, pady=2)

    def setup_file_selection_frame(self, parent, column=1):
        """ファイル選択フレームを設定"""
        file_selection_frame = ttk.LabelFrame(
            parent, text="作成するファイルを選択", padding="10"
        )
        file_selection_frame.grid(
            row=0, column=column, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(5 if column == 1 else 0, 0)
        )
        file_selection_frame.columnconfigure(0, weight=1)

        # スクロール可能なフレーム
        canvas = tk.Canvas(file_selection_frame, height=80)
        scrollbar_file = ttk.Scrollbar(
            file_selection_frame, orient="vertical", command=canvas.yview
        )
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar_file.set)

        canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar_file.grid(row=0, column=1, sticky=(tk.N, tk.S))

        # 設定からファイルリストを読み込んでチェックボックスを作成
        default_files = self.config.get("default_files", [])
        for i, file_config in enumerate(default_files):
            var = tk.BooleanVar(value=False)  # デフォルトで非選択
            # チェックボックスの変更時にプレビューを更新
            var.trace_add("write", lambda *args: self.update_preview())
            file_name = file_config.get("name", "")
            file_description = file_config.get("description", "")
            
            # ファイル設定全体を保存
            self.file_vars[file_name] = {
                "var": var,
                "config": file_config
            }

            display_text = f"{file_name} - {file_description}"
            checkbox = ttk.Checkbutton(scrollable_frame, text=display_text, variable=var)
            checkbox.grid(row=i, column=0, sticky=tk.W, padx=10, pady=2)

    def setup_preview_frame(self, parent):
        """ディレクトリ構造プレビューフレームを設定"""
        preview_frame = ttk.LabelFrame(
            parent, text="作成予定のディレクトリ構造", padding="10"
        )
        preview_frame.grid(
            row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10)
        )
        preview_frame.columnconfigure(0, weight=1)
        preview_frame.rowconfigure(0, weight=1)

        # プレビューテキストエリア（スクロールバー付き）
        self.preview_text = tk.Text(
            preview_frame, 
            height=5, 
            wrap=tk.NONE,
            font=("Consolas", 9),
            bg="#f8f8f8",
            state=tk.DISABLED
        )
        preview_scrollbar_v = ttk.Scrollbar(
            preview_frame, orient=tk.VERTICAL, command=self.preview_text.yview
        )
        preview_scrollbar_h = ttk.Scrollbar(
            preview_frame, orient=tk.HORIZONTAL, command=self.preview_text.xview
        )
        
        self.preview_text.configure(
            yscrollcommand=preview_scrollbar_v.set,
            xscrollcommand=preview_scrollbar_h.set
        )

        self.preview_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        preview_scrollbar_v.grid(row=0, column=1, sticky=(tk.N, tk.S))
        preview_scrollbar_h.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        # 更新ボタン
        update_preview_button = ttk.Button(
            preview_frame, text="プレビュー更新", command=self.update_preview
        )
        update_preview_button.grid(row=2, column=0, sticky=tk.W, pady=(5, 0))
        
        # 初期プレビューを表示
        self.update_preview()

    def update_preview(self):
        """プレビューテキストを更新"""
        if not hasattr(self, 'preview_text'):
            return
            
        # プレビューテキストをクリア
        self.preview_text.config(state=tk.NORMAL)
        self.preview_text.delete(1.0, tk.END)
        
        target_path = self.selected_folder.get().strip()
        if not target_path:
            self.preview_text.insert(tk.END, "ターゲットフォルダが指定されていません。")
            self.preview_text.config(state=tk.DISABLED)
            return
            
        # 選択されたフォルダとファイルを取得
        selected_folders = [
            name for name, var in self.folder_vars.items() if var.get()
        ]
        selected_files = [
            {
                "name": file_name,
                "config": file_data["config"]
            }
            for file_name, file_data in self.file_vars.items() 
            if file_data["var"].get()
        ]
        
        if not selected_folders and not selected_files:
            self.preview_text.insert(tk.END, "作成するフォルダまたはファイルが選択されていません。")
            self.preview_text.config(state=tk.DISABLED)
            return
            
        # ツリー構造を生成
        tree_structure = self.generate_tree_structure(target_path, selected_folders, selected_files)
        self.preview_text.insert(tk.END, tree_structure)
        self.preview_text.config(state=tk.DISABLED)

    def generate_tree_structure(self, target_path, selected_folders, selected_files):
        """ディレクトリツリー構造文字列を生成"""
        import os
        
        tree_lines = []
        tree_lines.append(f"📁 {os.path.basename(target_path) or target_path}")
        
        # フォルダを追加
        for i, folder_name in enumerate(selected_folders):
            is_last_folder = (i == len(selected_folders) - 1) and not selected_files
            prefix = "└── " if is_last_folder else "├── "
            tree_lines.append(f"{prefix}📁 {folder_name}/")
        
        # ファイルを追加
        for i, file_info in enumerate(selected_files):
            file_name = file_info.get("name", "")
            is_last = i == len(selected_files) - 1
            prefix = "└── " if is_last else "├── "
            
            # ファイルタイプに応じてアイコンを選択
            if file_name.endswith(('.txt', '.md')):
                icon = "📄"
            elif file_name.endswith(('.cs', '.py', '.js')):
                icon = "📝"
            elif file_name.startswith('.'):
                icon = "⚙️"
            else:
                icon = "📄"
                
            tree_lines.append(f"{prefix}{icon} {file_name}")
        
        return "\n".join(tree_lines)

    def browse_folder(self):
        """フォルダ選択ダイアログを開く"""
        folder_path = filedialog.askdirectory(title="対象フォルダを選択してください")
        if folder_path:
            self.selected_folder.set(folder_path)
            self.log(f"フォルダが選択されました: {folder_path}")
            # プレビューを更新
            self.update_preview()

    def select_all_folders(self):
        """全てのフォルダを選択"""
        for var in self.folder_vars.values():
            var.set(True)
        for file_name, file_data in self.file_vars.items():
            file_data["var"].set(True)
        self.log("全てのフォルダとファイルが選択されました")

    def deselect_all_folders(self):
        """全てのフォルダ選択を解除"""
        for var in self.folder_vars.values():
            var.set(False)
        for file_name, file_data in self.file_vars.items():
            file_data["var"].set(False)
        self.log("全てのフォルダとファイル選択が解除されました")

    def log(self, message):
        """ログメッセージを表示"""
        self.log_text.insert(tk.END, f"{message}\n")

        # 最大行数を超えた場合は古い行を削除
        max_lines = self.config.get("log_settings", {}).get("max_lines", 1000)
        lines = self.log_text.get(1.0, tk.END).count("\n")
        if lines > max_lines:
            self.log_text.delete(1.0, f"{lines - max_lines + 1}.0")

        if self.config.get("log_settings", {}).get("auto_scroll", True):
            self.log_text.see(tk.END)
        self.root.update()

    def clear_log(self):
        """ログをクリア"""
        self.log_text.delete(1.0, tk.END)

    def create_folders_and_files(self):
        """選択されたフォルダとファイルを作成（事前チェック統合）"""
        folder_path = self.selected_folder.get()
        if not folder_path:
            messagebox.showwarning("警告", "フォルダを選択してください。")
            return

        if not os.path.exists(folder_path):
            messagebox.showerror("エラー", "選択されたフォルダが存在しません。")
            return

        # 選択されたフォルダとファイルを取得
        selected_folders = [path for path, var in self.folder_vars.items() if var.get()]
        selected_files = [
            (file_name, file_data["config"]) 
            for file_name, file_data in self.file_vars.items() 
            if file_data["var"].get()
        ]

        if not selected_folders and not selected_files:
            messagebox.showwarning("警告", "作成するフォルダまたはファイルを選択してください。")
            return

        try:
            self.log("=" * 50)
            self.log("フォルダ・ファイル作成処理開始")
            self.log(f"対象フォルダ: {folder_path}")
            self.log(f"作成対象: フォルダ{len(selected_folders)}個, ファイル{len(selected_files)}個")
            self.log("-" * 30)

            # === フォルダのチェックと作成 ===
            if selected_folders:
                self.log("� フォルダ構造チェック中...")
                existing_folders = []
                missing_folders = []

                for folder_relative_path in selected_folders:
                    full_path = os.path.join(folder_path, folder_relative_path)
                    if os.path.exists(full_path):
                        existing_folders.append(folder_relative_path)
                        self.log(f"⚠️  既存フォルダ: {folder_relative_path}")
                    else:
                        missing_folders.append(folder_relative_path)
                        self.log(f"📁 フォルダ作成予定: {folder_relative_path}")

                # フォルダ作成実行
                if missing_folders:
                    self.log("🔨 フォルダ作成開始...")
                    folder_created_count = 0
                    for folder_relative_path in missing_folders:
                        full_path = os.path.join(folder_path, folder_relative_path)
                        os.makedirs(full_path)
                        self.log(f"✅ フォルダ作成完了: {folder_relative_path}")
                        folder_created_count += 1
                else:
                    folder_created_count = 0
                    existing_folders = selected_folders

            else:
                existing_folders = []
                folder_created_count = 0

            # === ファイルのチェックと作成 ===
            if selected_files:
                self.log("-" * 30)
                self.log("📄 ファイル構造チェック中...")
                existing_files = []
                missing_files = []
                file_errors = []

                for file_name, file_config in selected_files:
                    target_path = file_config.get("target_path", file_name)
                    template_path = file_config.get("template_path", "")
                    full_target_path = os.path.join(folder_path, target_path)
                    
                    # テンプレートファイルの存在確認
                    if not os.path.exists(template_path):
                        file_errors.append(f"{file_name}: テンプレートファイル {template_path} が見つかりません")
                        continue
                    
                    if os.path.exists(full_target_path):
                        existing_files.append(file_name)
                        self.log(f"⚠️  既存ファイル: {target_path}")
                    else:
                        missing_files.append((file_name, file_config))
                        self.log(f"📄 ファイル作成予定: {target_path}")

                # ファイルエラーの表示
                if file_errors:
                    self.log("-" * 30)
                    self.log("🚨 ファイルエラー:")
                    for error in file_errors:
                        self.log(f"   ❌ {error}")

                # ファイル作成実行
                if missing_files:
                    self.log("🔨 ファイル作成開始...")
                    file_created_count = 0
                    for file_name, file_config in missing_files:
                        try:
                            target_path = file_config.get("target_path", file_name)
                            template_path = file_config.get("template_path", "")
                            full_target_path = os.path.join(folder_path, target_path)
                            
                            # ターゲットディレクトリが存在しない場合は作成
                            target_dir = os.path.dirname(full_target_path)
                            if target_dir and not os.path.exists(target_dir):
                                os.makedirs(target_dir)
                                self.log(f"📁 ディレクトリ作成: {os.path.relpath(target_dir, folder_path)}")
                            
                            # ファイルをコピー
                            shutil.copy2(template_path, full_target_path)
                            self.log(f"✅ ファイル作成完了: {target_path}")
                            file_created_count += 1
                        except Exception as e:
                            self.log(f"❌ ファイル作成エラー: {file_name} - {str(e)}")
                else:
                    file_created_count = 0

            else:
                existing_files = []
                file_created_count = 0
                file_errors = []

            # 結果表示
            self.log("-" * 30)
            self.log(
                f"🎉 【完了】フォルダ新規作成: {folder_created_count}個, "
                f"ファイル新規作成: {file_created_count}個"
            )
            if existing_folders or existing_files:
                self.log(
                    f"⚠️ 既存スキップ: フォルダ{len(existing_folders)}個, "
                    f"ファイル{len(existing_files)}個"
                )
            self.log("=" * 50)

            # 完了メッセージ
            message_parts = []
            if folder_created_count > 0:
                message_parts.append(f"✅ フォルダ新規作成: {folder_created_count}個")
            if file_created_count > 0:
                message_parts.append(f"✅ ファイル新規作成: {file_created_count}個")
            if existing_folders or existing_files:
                message_parts.append(f"⚠️ 既存スキップ: {len(existing_folders) + len(existing_files)}個")
            if file_errors:
                message_parts.append(f"❌ エラー: {len(file_errors)}個")

            if message_parts:
                messagebox.showinfo(
                    "完了",
                    f"フォルダ・ファイル作成が完了しました。\n\n" + "\n".join(message_parts) + 
                    f"\n\n詳細はログをご確認ください。"
                )
            else:
                messagebox.showinfo("情報", "作成する新しいフォルダ・ファイルがありませんでした。")

        except Exception as e:
            error_msg = f"作成処理中にエラーが発生しました: {str(e)}"
            self.log(f"💥 {error_msg}")
            messagebox.showerror("エラー", error_msg)


def main():
    """メイン関数"""
    root = tk.Tk()
    app = AdvancedFolderCreatorApp(root)

    # ウィンドウを中央に配置
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f"{width}x{height}+{x}+{y}")

    root.mainloop()


if __name__ == "__main__":
    main()
