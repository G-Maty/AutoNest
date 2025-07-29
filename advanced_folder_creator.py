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
            "default_folders": ["Assets/Editor", "Assets/Scripts", "Assets/Textures"],
            "window_settings": {
                "width": 700,
                "height": 500,
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

        # フォルダ選択セクション
        self.setup_folder_selection_frame(main_frame)

        # ボタンフレーム
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=3, pady=10)

        # 作成ボタン
        create_button = ttk.Button(
            button_frame, text="選択されたフォルダを作成", command=self.create_folders
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
            row=4, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0)
        )
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(4, weight=1)

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

    def setup_folder_selection_frame(self, parent):
        """フォルダ選択フレームを設定"""
        folder_selection_frame = ttk.LabelFrame(
            parent, text="作成するフォルダを選択", padding="10"
        )
        folder_selection_frame.grid(
            row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10)
        )
        folder_selection_frame.columnconfigure(0, weight=1)

        # スクロール可能なフレーム
        canvas = tk.Canvas(folder_selection_frame, height=120)
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
            self.folder_vars[folder_path] = var

            checkbox = ttk.Checkbutton(scrollable_frame, text=folder_path, variable=var)
            checkbox.grid(row=i // 2, column=i % 2, sticky=tk.W, padx=10, pady=2)

    def browse_folder(self):
        """フォルダ選択ダイアログを開く"""
        folder_path = filedialog.askdirectory(title="対象フォルダを選択してください")
        if folder_path:
            self.selected_folder.set(folder_path)
            self.log(f"フォルダが選択されました: {folder_path}")

    def select_all_folders(self):
        """全てのフォルダを選択"""
        for var in self.folder_vars.values():
            var.set(True)
        self.log("全てのフォルダが選択されました")

    def deselect_all_folders(self):
        """全てのフォルダ選択を解除"""
        for var in self.folder_vars.values():
            var.set(False)
        self.log("全てのフォルダ選択が解除されました")

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

    def create_folders(self):
        """選択されたフォルダを作成（事前チェック統合）"""
        folder_path = self.selected_folder.get()
        if not folder_path:
            messagebox.showwarning("警告", "フォルダを選択してください。")
            return

        if not os.path.exists(folder_path):
            messagebox.showerror("エラー", "選択されたフォルダが存在しません。")
            return

        # 選択されたフォルダのみ作成
        selected_folders = [path for path, var in self.folder_vars.items() if var.get()]

        if not selected_folders:
            messagebox.showwarning("警告", "作成するフォルダを選択してください。")
            return

        try:
            self.log("=" * 50)
            self.log("フォルダ作成処理開始")
            self.log(f"対象フォルダ: {folder_path}")
            self.log(f"作成対象: {len(selected_folders)}個のフォルダ")
            self.log("-" * 30)

            # 事前チェック：既存フォルダの確認
            self.log("📋 フォルダ構造チェック中...")
            existing_folders = []
            missing_folders = []

            for folder_relative_path in selected_folders:
                full_path = os.path.join(folder_path, folder_relative_path)
                if os.path.exists(full_path):
                    existing_folders.append(folder_relative_path)
                    self.log(f"⚠️  既存: {folder_relative_path}")
                else:
                    missing_folders.append(folder_relative_path)
                    self.log(f"📁 作成予定: {folder_relative_path}")

            # 既存フォルダに対する警告
            if existing_folders:
                self.log("-" * 30)
                self.log(
                    f"🚨 警告: {len(existing_folders)}個のフォルダが既に存在します"
                )
                for folder in existing_folders:
                    self.log(
                        f"   ❌ エラー: {folder} は既に存在するためスキップされます"
                    )
                self.log("-" * 30)

            if not missing_folders:
                self.log("ℹ️  作成する新しいフォルダがありません。")
                self.log("=" * 50)
                messagebox.showinfo(
                    "情報", "選択されたフォルダはすべて既に存在しています。"
                )
                return

            # フォルダ作成実行
            self.log("🔨 フォルダ作成開始...")
            created_count = 0

            for folder_relative_path in missing_folders:
                full_path = os.path.join(folder_path, folder_relative_path)
                os.makedirs(full_path)
                self.log(f"✅ 作成完了: {folder_relative_path}")
                created_count += 1

            self.log("-" * 30)
            self.log(
                f"🎉 【完了】新規作成: {created_count}個, 既存スキップ: {len(existing_folders)}個"
            )
            self.log("=" * 50)

            # 完了メッセージ
            if existing_folders:
                messagebox.showinfo(
                    "完了",
                    f"フォルダ作成が完了しました。\n"
                    f"✅ 新規作成: {created_count}個\n"
                    f"⚠️ 既存スキップ: {len(existing_folders)}個\n\n"
                    f"詳細はログをご確認ください。",
                )
            else:
                messagebox.showinfo(
                    "完了",
                    f"フォルダ作成が完了しました。\n✅ 新規作成: {created_count}個",
                )

        except Exception as e:
            error_msg = f"フォルダ作成中にエラーが発生しました: {str(e)}"
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
