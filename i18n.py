"""
i18n.py - TaskPlovo 国際化テキスト定義
"""

STRINGS = {
    "ja": {
        # メニュー
        "menu_add_task":     "＋ 新規タスクの追加",
        "menu_options":      "オプション",
        "menu_settings":     "設定...",
        "menu_other":        "その他",
        "menu_version":      "バージョン確認",
        "menu_export":       "報告資料の出力(Excel)",

        # ヘッダー
        "btn_this_month":    "今月",
        "btn_today_tasks":   "本日のタスク一覧",
        "lbl_view":          "表示:",
        "view_month":        "月",
        "view_day":          "日",
        "view_year":         "年",
        "view_custom":       "カスタム",

        # 月ビュー
        "days":              ["月","火","水","木","金","土","日"],

        # 日ビュー
        "no_tasks_today":    "この日のタスクはありません",
        "btn_add_today":     "＋ この日にタスクを追加",
        "badge_done":        "完了",
        "badge_ongoing":     "進行中",

        # タスクバー
        "time_suffix":       "",   # 月ビュー：時刻の後ろ（なし）
        "time_suffix_day":   "まで",  # 日ビュー

        # 右クリック
        "ctx_complete":      "✓ 完了にする",
        "ctx_revert":        "↩ 未完了に戻す",
        "ctx_edit":          "✏ 編集",
        "ctx_delete":        "🗑 削除",

        # 削除確認
        "confirm_delete":    "削除確認",
        "confirm_delete_msg":"を削除しますか？",

        # タスクダイアログ
        "dlg_add_title":     "新規タスクの追加",
        "dlg_edit_title":    "タスクを編集",
        "lbl_task_title":    "タスクタイトル *",
        "lbl_detail":        "タスクの詳細",
        "lbl_start_date":    "開始日 *",
        "lbl_due_date":      "期日 *",
        "lbl_due_time":      "〆時刻",
        "lbl_time_until":    "まで",
        "lbl_label_color":   "タスクラベル（色）",
        "lbl_selected":      "選択中: ",
        "lbl_auto_color":    "カレンダーカラーに追従",
        "lbl_note":          "備考",
        "btn_save":          "保存する",
        "btn_cancel":        "キャンセル",
        "btn_delete":        "削除",
        "voice_listening":   "🎤 録音中... 話しかけてください",
        "voice_ok":          "✅ 認識: ",
        "voice_timeout":     "タイムアウトしました",
        "voice_unknown":     "聞き取れませんでした",
        "voice_error":       "エラー: ",
        "voice_missing":     "音声入力には SpeechRecognition と PyAudio が必要です。\n\npip install SpeechRecognition pyaudio",
        "err_title_empty":   "タイトルを入力してください。",
        "err_start_empty":   "開始日を選択してください。",
        "err_due_empty":     "期日を選択してください。",
        "err_date_order":    "期日は開始日以降にしてください。",
        "err_date_format":   "日付の形式が正しくありません。",
        "err_input":         "入力エラー",

        # オプションダイアログ
        "opt_title":         "オプション設定",
        "opt_app_mode":      "アプリモード",
        "opt_dark":          "🌙 ダーク",
        "opt_dark_desc":     "黒ベースの背景・白文字",
        "opt_light":         "☀ ライト",
        "opt_light_desc":    "白ベースの背景・黒文字",
        "opt_language":      "言語設定",
        "opt_behavior":      "動作設定",
        "opt_startup":       "PC起動時に自動起動する",
        "opt_startup_desc":  "レジストリのスタートアップに登録されます",
        "opt_tray":          "× ボタンでタスクトレイに格納する",
        "opt_tray_desc":     "オフにすると × ボタンでアプリが終了します",
        "opt_save":          "保存する",
        "opt_saved":         "設定保存",
        "opt_saved_msg":     "設定を保存しました。",

        # バージョン情報
        "ver_title":         "バージョン情報",
        "ver_version":       "バージョン: ",
        "ver_copyright":     "© 2025 TaskPlovo",
        "btn_ok":            "OK",

        # カスタム期間
        "custom_title":      "カスタム期間を設定",
        "custom_prompt":     "表示する期間を選んでください",
        "custom_start":      "開始日",
        "custom_end":        "終了日",
        "btn_apply":         "適用",

        # 出力
        "export_none":       "タスクがありません。",
        "export_done":       "出力完了",
        "export_saved":      "デスクトップに保存しました:\n",
        "export_err_title":  "エラー",
        "export_err_msg":    "openpyxl が見つかりません。\n\nコマンドプロンプトで以下を実行してください:\npip install openpyxl",
        "export_sheet_title":"TaskPlovo 業務タスク一覧　",
        "export_headers":    ["No.", "タスク名", "詳細", "開始日", "期日", "〆時刻", "備考", "ステータス"],
        "export_done_status":"✓ 完了",
        "export_ongoing":    "進行中",

        # 年ビュー月名
        "month_suffix":      "月",
    },

    "en": {
        # Menu
        "menu_add_task":     "+ New Task",
        "menu_options":      "Options",
        "menu_settings":     "Settings...",
        "menu_other":        "More",
        "menu_version":      "Version Info",
        "menu_export":       "Export Report (Excel)",

        # Header
        "btn_this_month":    "This Month",
        "btn_today_tasks":   "Today's Tasks",
        "lbl_view":          "View:",
        "view_month":        "Month",
        "view_day":          "Day",
        "view_year":         "Year",
        "view_custom":       "Custom",

        # Month view
        "days":              ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"],

        # Day view
        "no_tasks_today":    "No tasks for this day",
        "btn_add_today":     "+ Add Task for This Day",
        "badge_done":        "Done",
        "badge_ongoing":     "Ongoing",

        # Task bar
        "time_suffix":       "",
        "time_suffix_day":   " due",

        # Context menu
        "ctx_complete":      "✓ Mark as Done",
        "ctx_revert":        "↩ Mark as Undone",
        "ctx_edit":          "✏ Edit",
        "ctx_delete":        "🗑 Delete",

        # Delete confirm
        "confirm_delete":    "Confirm Delete",
        "confirm_delete_msg": " — delete this task?",

        # Task dialog
        "dlg_add_title":     "New Task",
        "dlg_edit_title":    "Edit Task",
        "lbl_task_title":    "Task Title *",
        "lbl_detail":        "Details",
        "lbl_start_date":    "Start Date *",
        "lbl_due_date":      "Due Date *",
        "lbl_due_time":      "Due Time",
        "lbl_time_until":    "due",
        "lbl_label_color":   "Label Color",
        "lbl_selected":      "Selected: ",
        "lbl_auto_color":    "Follow calendar color",
        "lbl_note":          "Notes",
        "btn_save":          "Save",
        "btn_cancel":        "Cancel",
        "btn_delete":        "Delete",
        "voice_listening":   "🎤 Listening... Please speak",
        "voice_ok":          "✅ Recognized: ",
        "voice_timeout":     "Timed out",
        "voice_unknown":     "Could not recognize",
        "voice_error":       "Error: ",
        "voice_missing":     "SpeechRecognition and PyAudio are required.\n\npip install SpeechRecognition pyaudio",
        "err_title_empty":   "Please enter a title.",
        "err_start_empty":   "Please select a start date.",
        "err_due_empty":     "Please select a due date.",
        "err_date_order":    "Due date must be on or after start date.",
        "err_date_format":   "Invalid date format.",
        "err_input":         "Input Error",

        # Options dialog
        "opt_title":         "Settings",
        "opt_app_mode":      "App Mode",
        "opt_dark":          "🌙 Dark",
        "opt_dark_desc":     "Dark background, white text",
        "opt_light":         "☀ Light",
        "opt_light_desc":    "Light background, dark text",
        "opt_language":      "Language",
        "opt_behavior":      "Behavior",
        "opt_startup":       "Launch on system startup",
        "opt_startup_desc":  "Registers in Windows startup registry",
        "opt_tray":          "Minimize to tray on close",
        "opt_tray_desc":     "Disabling this will quit the app on close",
        "opt_save":          "Save",
        "opt_saved":         "Saved",
        "opt_saved_msg":     "Settings have been saved.",

        # Version info
        "ver_title":         "Version Info",
        "ver_version":       "Version: ",
        "ver_copyright":     "© 2025 TaskPlovo",
        "btn_ok":            "OK",

        # Custom range
        "custom_title":      "Set Custom Range",
        "custom_prompt":     "Select the date range to display",
        "custom_start":      "Start Date",
        "custom_end":        "End Date",
        "btn_apply":         "Apply",

        # Export
        "export_none":       "No tasks found.",
        "export_done":       "Export Complete",
        "export_saved":      "Saved to Desktop:\n",
        "export_err_title":  "Error",
        "export_err_msg":    "openpyxl not found.\n\nRun the following in Command Prompt:\npip install openpyxl",
        "export_sheet_title":"TaskPlovo Task Report  ",
        "export_headers":    ["No.", "Task", "Details", "Start", "Due", "Due Time", "Notes", "Status"],
        "export_done_status":"✓ Done",
        "export_ongoing":    "Ongoing",

        # Year view month label
        "month_suffix":      "",
    },
}


def get(config: dict, key: str, default: str = "") -> str:
    lang = config.get("language", "ja")
    return STRINGS.get(lang, STRINGS["ja"]).get(key, default)


def get_list(config: dict, key: str) -> list:
    lang = config.get("language", "ja")
    return STRINGS.get(lang, STRINGS["ja"]).get(key, [])
