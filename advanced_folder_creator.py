#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AutoNest - フォルダ・ファイル自動作成ツール

指定したフォルダ内に複数のフォルダ構造とファイルを自動作成するGUIツール。
設定ファイル（config.json）によるカスタマイズに対応し、テンプレート
ベースのファイル作成機能を提供します。

主な機能:
- 複数フォルダの一括作成
- テンプレートファイルの自動生成
- ディレクトリ構造のプレビュー表示
- 既存ファイル・フォルダの保護
- 詳細なログ出力

Author: G-Maty
License: MIT
Version: 2.0.0
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
    """
    AutoNestメインアプリケーションクラス

    フォルダとファイルの自動作成機能を持つGUIアプリケーション。
    設定ファイルベースの柔軟なカスタマイズと安全な作成処理を提供。

    Attributes:
        root (tk.Tk): メインウィンドウ
        config (dict): 設定情報
        selected_folder (tk.StringVar): 選択された対象フォルダパス
        folder_vars (dict): フォルダ選択チェックボックスの状態
        file_vars (dict): ファイル選択チェックボックスの状態
    """

    def __init__(self, root):
        """
        アプリケーションの初期化

        Args:
            root (tk.Tk): Tkinterのルートウィンドウ
        """
        self.root = root
        self.config = self.load_config()

        # ウィンドウ設定の適用
        self._setup_window()

        # アプリケーション状態の初期化
        self._initialize_variables()

        # UIコンポーネントの構築
        self.setup_ui()

    def _setup_window(self):
        """ウィンドウの基本設定を行う"""
        window_config = self.config.get("window_settings", {})
        self.root.title(window_config.get("title", "AutoNest - フォルダ自動作成ツール"))

        width = window_config.get("width", 700)
        height = window_config.get("height", 500)
        self.root.geometry(f"{width}x{height}")
        self.root.resizable(True, True)

    def _initialize_variables(self):
        """アプリケーション変数の初期化"""
        # 選択されたフォルダパス
        self.selected_folder = tk.StringVar()

        # チェックボックス状態管理用辞書
        self.folder_vars = {}  # フォルダ選択状態
        self.file_vars = {}  # ファイル選択状態

    def load_config(self):
        """
        設定ファイル（config.json）を読み込む

        設定ファイルが存在しない場合や読み込みエラーが発生した場合は、
        デフォルト設定を返す。

        Returns:
            dict: 設定情報辞書
        """
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
        """
        デフォルト設定を生成して返す

        config.jsonが存在しない場合や読み込みに失敗した場合に使用される。

        Returns:
            dict: デフォルト設定辞書
        """
        return {
            "default_folders": ["Assets/Editor"],
            "default_files": [
                {
                    "name": ".gitignore",
                    "description": "Git無視ファイル",
                    "template_path": "templates/.gitignore",
                    "target_path": ".gitignore",
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
        """
        メインUIコンポーネントを設定・配置

        以下のUIセクションを順次構築：
        1. メインフレームとグリッド設定
        2. タイトルラベル
        3. フォルダ選択セクション
        4. フォルダ・ファイル選択セクション
        5. プレビューセクション
        6. 操作ボタンセクション
        7. ログ表示セクション
        """
        # メインフレームの構築とグリッド設定
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # ウィンドウ全体のリサイズ対応
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)

        # アプリケーションタイトル
        title_label = ttk.Label(
            main_frame,
            text="AutoNest - フォルダ自動作成ツール",
            font=("Arial", 16, "bold"),
        )
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))

        # 対象フォルダ選択UI
        self._setup_folder_selection_ui(main_frame)

        # フォルダ・ファイル選択UI（水平配置）
        self._setup_item_selection_ui(main_frame)

        # ディレクトリ構造プレビューUI
        self.setup_preview_frame(main_frame)

        # 操作ボタンUI
        self._setup_action_buttons(main_frame)

        # ログ表示UI
        self._setup_log_ui(main_frame)

    def _setup_folder_selection_ui(self, parent):
        """対象フォルダ選択UIセクションを構築"""
        folder_frame = ttk.LabelFrame(parent, text="対象フォルダの選択", padding="10")
        folder_frame.grid(
            row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10)
        )
        folder_frame.columnconfigure(1, weight=1)

        # フォルダパス表示ラベル
        ttk.Label(folder_frame, text="選択フォルダ:").grid(
            row=0, column=0, sticky=tk.W, padx=(0, 10)
        )

        # フォルダパス表示エントリ（読み取り専用）
        folder_entry = ttk.Entry(
            folder_frame, textvariable=self.selected_folder, state="readonly", width=50
        )
        folder_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))

        # フォルダ参照ボタン
        browse_button = ttk.Button(
            folder_frame, text="参照...", command=self.browse_folder
        )
        browse_button.grid(row=0, column=2, sticky=tk.W)

    def _setup_item_selection_ui(self, parent):
        """フォルダ・ファイル選択UIセクションを構築（水平配置）"""
        selection_frame = ttk.Frame(parent)
        selection_frame.grid(
            row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10)
        )
        selection_frame.columnconfigure(0, weight=1)
        selection_frame.columnconfigure(1, weight=1)

        # フォルダ選択セクション（左側）
        self.setup_folder_selection_frame(selection_frame, column=0)

        # ファイル選択セクション（右側）
        self.setup_file_selection_frame(selection_frame, column=1)

    def _setup_action_buttons(self, parent):
        """操作ボタンセクションを構築"""
        button_frame = ttk.Frame(parent)
        button_frame.grid(row=4, column=0, columnspan=3, pady=10)

        # メイン作成ボタン
        create_button = ttk.Button(
            button_frame,
            text="フォルダとファイルを作成",
            command=self.create_folders_and_files,
        )
        create_button.grid(row=0, column=0, padx=(0, 10))

        # 全選択ボタン
        select_all_button = ttk.Button(
            button_frame, text="全て選択", command=self.select_all_folders
        )
        select_all_button.grid(row=0, column=1, padx=(0, 10))

        # 全解除ボタン
        deselect_all_button = ttk.Button(
            button_frame, text="全て解除", command=self.deselect_all_folders
        )
        deselect_all_button.grid(row=0, column=2, padx=(0, 10))

    def _setup_log_ui(self, parent):
        """ログ表示UIセクションを構築"""
        log_frame = ttk.LabelFrame(parent, text="ログ", padding="10")
        log_frame.grid(
            row=5, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0)
        )
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        parent.rowconfigure(5, weight=1)

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
        """
        フォルダ選択チェックボックスフレームを構築

        設定ファイルから読み込んだフォルダリストを基に、
        スクロール可能なチェックボックス群を作成する。

        Args:
            parent: 親ウィジェット
            column (int): グリッド配置用のカラム番号
        """
        folder_selection_frame = ttk.LabelFrame(
            parent, text="作成するフォルダを選択", padding="10"
        )
        folder_selection_frame.grid(
            row=0,
            column=column,
            sticky=(tk.W, tk.E, tk.N, tk.S),
            padx=(0, 5 if column == 0 else 0),
        )
        folder_selection_frame.columnconfigure(0, weight=1)

        # スクロール可能なフレーム構築
        canvas, scrollable_frame = self._create_scrollable_frame(
            folder_selection_frame, height=80
        )

        # 設定からフォルダリストを読み込んでチェックボックスを作成
        default_folders = self.config.get("default_folders", [])
        for i, folder_path in enumerate(default_folders):
            # チェックボックス状態変数を作成（デフォルトで選択）
            var = tk.BooleanVar(value=True)
            var.trace_add("write", lambda *args: self.update_preview())
            self.folder_vars[folder_path] = var

            # チェックボックスウィジェット作成・配置
            checkbox = ttk.Checkbutton(scrollable_frame, text=folder_path, variable=var)
            checkbox.grid(row=i, column=0, sticky=tk.W, padx=10, pady=2)

    def setup_file_selection_frame(self, parent, column=1):
        """
        ファイル選択チェックボックスフレームを構築

        設定ファイルから読み込んだファイルリストを基に、
        スクロール可能なチェックボックス群を作成する。

        Args:
            parent: 親ウィジェット
            column (int): グリッド配置用のカラム番号
        """
        file_selection_frame = ttk.LabelFrame(
            parent, text="作成するファイルを選択(実験機能)", padding="10"
        )
        file_selection_frame.grid(
            row=0,
            column=column,
            sticky=(tk.W, tk.E, tk.N, tk.S),
            padx=(5 if column == 1 else 0, 0),
        )
        file_selection_frame.columnconfigure(0, weight=1)

        # スクロール可能なフレーム構築
        canvas, scrollable_frame = self._create_scrollable_frame(
            file_selection_frame, height=80
        )

        # 設定からファイルリストを読み込んでチェックボックスを作成
        default_files = self.config.get("default_files", [])
        for i, file_config in enumerate(default_files):
            # チェックボックス状態変数を作成（デフォルトで非選択）
            var = tk.BooleanVar(value=True)
            var.trace_add("write", lambda *args: self.update_preview())
            file_name = file_config.get("name", "")

            # ファイル設定全体をfile_varsに保存
            self.file_vars[file_name] = {"var": var, "config": file_config}

            # チェックボックス表示テキスト設定・配置
            display_text = f"{file_name}"
            checkbox = ttk.Checkbutton(
                scrollable_frame, text=display_text, variable=var
            )
            checkbox.grid(row=i, column=0, sticky=tk.W, padx=10, pady=2)

    def _create_scrollable_frame(self, parent, height=80):
        """
        スクロール可能なフレームを作成するヘルパーメソッド

        Args:
            parent: 親ウィジェット
            height (int): キャンバスの高さ

        Returns:
            tuple: (canvas, scrollable_frame) のタプル
        """
        canvas = tk.Canvas(parent, height=height)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        # スクロール領域の更新設定
        scrollable_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # キャンバスとスクロールバーを配置
        canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))

        return canvas, scrollable_frame

    def setup_preview_frame(self, parent):
        """
        ディレクトリ構造プレビューフレームを構築

        作成予定のフォルダ・ファイル構造をツリー形式で表示する
        プレビュー機能を提供する。

        Args:
            parent: 親ウィジェット
        """
        preview_frame = ttk.LabelFrame(
            parent, text="ディレクトリ構造(実験機能)", padding="10"
        )
        preview_frame.grid(
            row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10)
        )
        preview_frame.columnconfigure(0, weight=1)
        preview_frame.rowconfigure(0, weight=1)

        # プレビューテキストエリア（水平・垂直スクロールバー付き）
        self.preview_text = tk.Text(
            preview_frame,
            height=5,
            wrap=tk.NONE,
            font=("Consolas", 9),
            bg="#f8f8f8",
            state=tk.DISABLED,
        )

        # スクロールバーの設定
        preview_scrollbar_v = ttk.Scrollbar(
            preview_frame, orient=tk.VERTICAL, command=self.preview_text.yview
        )
        preview_scrollbar_h = ttk.Scrollbar(
            preview_frame, orient=tk.HORIZONTAL, command=self.preview_text.xview
        )

        self.preview_text.configure(
            yscrollcommand=preview_scrollbar_v.set,
            xscrollcommand=preview_scrollbar_h.set,
        )

        # ウィジェット配置
        self.preview_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        preview_scrollbar_v.grid(row=0, column=1, sticky=(tk.N, tk.S))
        preview_scrollbar_h.grid(row=1, column=0, sticky=(tk.W, tk.E))

        # プレビュー更新ボタン
        update_preview_button = ttk.Button(
            preview_frame, text="プレビュー更新", command=self.update_preview
        )
        update_preview_button.grid(row=2, column=0, sticky=tk.W, pady=(5, 0))

        # 初期プレビューを表示
        self.update_preview()

    def update_preview(self):
        """
        プレビューテキストを更新

        現在選択されているフォルダとファイルを基に、
        作成予定のディレクトリ構造をツリー形式で表示する。
        """
        if not hasattr(self, "preview_text"):
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
        selected_folders = [name for name, var in self.folder_vars.items() if var.get()]
        selected_files = [
            {"name": file_name, "config": file_data["config"]}
            for file_name, file_data in self.file_vars.items()
            if file_data["var"].get()
        ]

        # 選択項目がない場合の処理
        if not selected_folders and not selected_files:
            self.preview_text.insert(
                tk.END, "作成するフォルダまたはファイルが選択されていません。"
            )
            self.preview_text.config(state=tk.DISABLED)
            return

        # ツリー構造を生成・表示
        tree_structure = self.generate_tree_structure(
            target_path, selected_folders, selected_files
        )
        self.preview_text.insert(tk.END, tree_structure)
        self.preview_text.config(state=tk.DISABLED)

    def generate_tree_structure(self, target_path, selected_folders, selected_files):
        """
        ディレクトリツリー構造文字列を生成

        Args:
            target_path (str): 対象フォルダパス
            selected_folders (list): 選択されたフォルダリスト
            selected_files (list): 選択されたファイルリスト

        Returns:
            str: ツリー構造を表現した文字列
        """
        tree_lines = []
        tree_lines.append(f"📁 {os.path.basename(target_path) or target_path}")

        # フォルダをツリーに追加
        for i, folder_name in enumerate(selected_folders):
            is_last_folder = (i == len(selected_folders) - 1) and not selected_files
            prefix = "└── " if is_last_folder else "├── "
            tree_lines.append(f"{prefix}📁 {folder_name}/")

        # ファイルをツリーに追加
        for i, file_info in enumerate(selected_files):
            file_name = file_info.get("name", "")
            is_last = i == len(selected_files) - 1
            prefix = "└── " if is_last else "├── "
            tree_lines.append(f"{prefix} {file_name}")

        return "\n".join(tree_lines)

    def browse_folder(self):
        """
        フォルダ選択ダイアログを開く

        ユーザーが対象フォルダを選択できるファイルダイアログを表示し、
        選択結果をログに記録してプレビューを更新する。
        """
        folder_path = filedialog.askdirectory(title="対象フォルダを選択してください")
        if folder_path:
            self.selected_folder.set(folder_path)
            self.log(f"フォルダが選択されました: {folder_path}")
            self.update_preview()

    def select_all_folders(self):
        """
        全てのフォルダとファイルを選択

        UI上のすべてのチェックボックスを選択状態にし、
        結果をログに記録する。
        """
        for var in self.folder_vars.values():
            var.set(True)
        for file_name, file_data in self.file_vars.items():
            file_data["var"].set(True)
        self.log("全てのフォルダとファイルが選択されました")

    def deselect_all_folders(self):
        """
        全てのフォルダとファイル選択を解除

        UI上のすべてのチェックボックスを非選択状態にし、
        結果をログに記録する。
        """
        for var in self.folder_vars.values():
            var.set(False)
        for file_name, file_data in self.file_vars.items():
            file_data["var"].set(False)
        self.log("全てのフォルダとファイル選択が解除されました")

    def log(self, message):
        """
        ログメッセージを表示

        ログテキストエリアにメッセージを追加し、設定に従って
        行数制限と自動スクロールを適用する。

        Args:
            message (str): 表示するログメッセージ
        """
        self.log_text.insert(tk.END, f"{message}\n")

        # 設定された最大行数を超えた場合は古い行を削除
        max_lines = self.config.get("log_settings", {}).get("max_lines", 1000)
        lines = self.log_text.get(1.0, tk.END).count("\n")
        if lines > max_lines:
            self.log_text.delete(1.0, f"{lines - max_lines + 1}.0")

        # 自動スクロール設定が有効な場合は最新行を表示
        if self.config.get("log_settings", {}).get("auto_scroll", True):
            self.log_text.see(tk.END)
        self.root.update()

    def clear_log(self):
        """
        ログを完全にクリア

        ログテキストエリア内のすべてのテキストを削除する。
        """
        self.log_text.delete(1.0, tk.END)

    def create_folders_and_files(self):
        """
        選択されたフォルダとファイルを作成する（メイン処理）

        以下の処理を順次実行：
        1. 入力値の事前チェック
        2. フォルダの存在確認と作成
        3. ファイルの存在確認と作成
        4. 結果の集計と表示

        既存のフォルダ・ファイルは上書きせず、安全に処理を行う。
        すべての処理状況は詳細ログとして記録される。
        """
        # 入力値の事前検証
        folder_path = self.selected_folder.get()
        if not folder_path:
            messagebox.showwarning("警告", "フォルダを選択してください。")
            return

        if not os.path.exists(folder_path):
            messagebox.showerror("エラー", "選択されたフォルダが存在しません。")
            return

        # 選択されたアイテムを取得
        selected_folders = [path for path, var in self.folder_vars.items() if var.get()]
        selected_files = [
            (file_name, file_data["config"])
            for file_name, file_data in self.file_vars.items()
            if file_data["var"].get()
        ]

        if not selected_folders and not selected_files:
            messagebox.showwarning(
                "警告", "作成するフォルダまたはファイルを選択してください。"
            )
            return

        # メイン作成処理の実行
        try:
            self._execute_creation_process(
                folder_path, selected_folders, selected_files
            )
        except Exception as e:
            error_msg = f"作成処理中にエラーが発生しました: {str(e)}"
            self.log(f"💥 {error_msg}")
            messagebox.showerror("エラー", error_msg)

    def _execute_creation_process(self, folder_path, selected_folders, selected_files):
        """
        フォルダ・ファイル作成処理を実行

        Args:
            folder_path (str): 対象フォルダパス
            selected_folders (list): 作成対象フォルダリスト
            selected_files (list): 作成対象ファイルリスト
        """
        # 処理開始ログ
        self.log("=" * 50)
        self.log("フォルダ・ファイル作成処理開始")
        self.log(f"対象フォルダ: {folder_path}")
        self.log(
            f"作成対象: フォルダ{len(selected_folders)}個, ファイル{len(selected_files)}個"
        )
        self.log("-" * 30)

        # フォルダ作成処理
        folder_created_count, existing_folders = self._process_folders(
            folder_path, selected_folders
        )

        # ファイル作成処理
        file_created_count, existing_files, file_errors = self._process_files(
            folder_path, selected_files
        )

        # 結果の表示
        self._show_completion_results(
            folder_created_count,
            file_created_count,
            existing_folders,
            existing_files,
            file_errors,
        )

    def _process_folders(self, folder_path, selected_folders):
        """
        フォルダ作成処理を実行

        Args:
            folder_path (str): 対象フォルダパス
            selected_folders (list): 作成対象フォルダリスト

        Returns:
            tuple: (作成されたフォルダ数, 既存フォルダリスト)
        """
        if not selected_folders:
            return 0, []

        self.log("📁 フォルダ構造チェック中...")
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
        folder_created_count = 0
        if missing_folders:
            self.log("🔨 フォルダ作成開始...")
            for folder_relative_path in missing_folders:
                full_path = os.path.join(folder_path, folder_relative_path)
                os.makedirs(full_path)
                self.log(f"✅ フォルダ作成完了: {folder_relative_path}")
                folder_created_count += 1
        else:
            existing_folders = selected_folders

        return folder_created_count, existing_folders

    def _process_files(self, folder_path, selected_files):
        """
        ファイル作成処理を実行

        Args:
            folder_path (str): 対象フォルダパス
            selected_files (list): 作成対象ファイルリスト

        Returns:
            tuple: (作成されたファイル数, 既存ファイルリスト, エラーリスト)
        """
        if not selected_files:
            return 0, [], []

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
                file_errors.append(
                    f"{file_name}: テンプレートファイル {template_path} が見つかりません"
                )
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
        file_created_count = 0
        if missing_files:
            self.log("🔨 ファイル作成開始...")
            for file_name, file_config in missing_files:
                try:
                    target_path = file_config.get("target_path", file_name)
                    template_path = file_config.get("template_path", "")
                    full_target_path = os.path.join(folder_path, target_path)

                    # ターゲットディレクトリが存在しない場合は作成
                    target_dir = os.path.dirname(full_target_path)
                    if target_dir and not os.path.exists(target_dir):
                        os.makedirs(target_dir)
                        self.log(
                            f"📁 ディレクトリ作成: {os.path.relpath(target_dir, folder_path)}"
                        )

                    # ファイルをコピー
                    shutil.copy2(template_path, full_target_path)
                    self.log(f"✅ ファイル作成完了: {target_path}")
                    file_created_count += 1
                except Exception as e:
                    self.log(f"❌ ファイル作成エラー: {file_name} - {str(e)}")

        return file_created_count, existing_files, file_errors

    def _show_completion_results(
        self,
        folder_created_count,
        file_created_count,
        existing_folders,
        existing_files,
        file_errors,
    ):
        """
        作成処理完了結果を表示

        Args:
            folder_created_count (int): 作成されたフォルダ数
            file_created_count (int): 作成されたファイル数
            existing_folders (list): 既存フォルダリスト
            existing_files (list): 既存ファイルリスト
            file_errors (list): ファイルエラーリスト
        """
        # 結果ログの表示
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

        # 完了メッセージダイアログの表示
        message_parts = []
        if folder_created_count > 0:
            message_parts.append(f"✅ フォルダ新規作成: {folder_created_count}個")
        if file_created_count > 0:
            message_parts.append(f"✅ ファイル新規作成: {file_created_count}個")
        if existing_folders or existing_files:
            message_parts.append(
                f"⚠️ 既存スキップ: {len(existing_folders) + len(existing_files)}個"
            )
        if file_errors:
            message_parts.append(f"❌ エラー: {len(file_errors)}個")

        if message_parts:
            messagebox.showinfo(
                "完了",
                f"フォルダ・ファイル作成が完了しました。\n\n"
                + "\n".join(message_parts)
                + f"\n\n詳細はログをご確認ください。",
            )
        else:
            messagebox.showinfo(
                "情報", "作成する新しいフォルダ・ファイルがありませんでした。"
            )


def main():
    """
    メイン関数 - アプリケーションのエントリーポイント

    Tkinterウィンドウを作成・初期化し、アプリケーションを起動する。
    ウィンドウを画面中央に配置してメインループを開始する。
    """
    # Tkinterルートウィンドウの作成
    root = tk.Tk()

    # アプリケーションインスタンスの作成
    app = AdvancedFolderCreatorApp(root)

    # ウィンドウを画面中央に配置
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # 中央配置の計算
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    root.geometry(f"{width}x{height}+{x}+{y}")

    # メインループ開始
    root.mainloop()


if __name__ == "__main__":
    main()
