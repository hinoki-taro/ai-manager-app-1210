# Google Drive セキュリティガイド

Google Drive連携機能のセキュリティを強化するための完全ガイドです。

---

## 🔒 セキュリティ機能

### 実装済みセキュリティ対策

1. ✅ **アカウントホワイトリスト** - 許可されたアカウントのみアクセス可
2. ✅ **IPアドレス制限** - 特定のIPアドレスからのみアクセス可
3. ✅ **ファイル形式制限** - 許可されたファイル形式のみダウンロード可
4. ✅ **ファイルサイズ制限** - 大容量ファイルのダウンロード防止
5. ✅ **レート制限** - 過度なアクセスの防止
6. ✅ **アクセスログ** - すべてのアクセスを記録
7. ✅ **監査ログ** - セキュリティイベントを記録
8. ✅ **不正アクセス検知** - 疑わしいアクティビティの検出
9. ✅ **トークン暗号化** - 認証情報の安全な保存
10. ✅ **セキュリティダッシュボード** - リアルタイムの監視

---

## 🚀 セットアップ

### ステップ1: セキュリティ設定ファイルの作成

```bash
# テンプレートをコピー
copy google_drive_security_config.json.template google_drive_security_config.json
```

### ステップ2: セキュリティ設定の編集

`google_drive_security_config.json` を開いて編集：

```json
{
    "enabled": true,
    "require_authentication": true,
    "whitelist_enabled": true,
    "whitelisted_accounts": [
        "shared@mm-international.co.jp",
        "@mm-international.co.jp"
    ],
    "whitelisted_ips": [],
    "allowed_file_types": [
        "pdf", "docx", "txt", "xlsx", "pptx", "csv", "md"
    ],
    "max_file_size_mb": 100,
    "audit_log_enabled": true,
    "access_log_enabled": true,
    "rate_limit": {
        "enabled": true,
        "max_requests_per_minute": 60,
        "max_downloads_per_hour": 100
    }
}
```

---

## 🔐 セキュリティ機能の詳細

### 1. アカウントホワイトリスト

**用途:** 許可されたGoogleアカウントのみがGoogle Driveにアクセスできるようにします。

**設定例:**

```json
{
    "whitelist_enabled": true,
    "whitelisted_accounts": [
        "admin@mm-international.co.jp",
        "shared@mm-international.co.jp",
        "@mm-international.co.jp"
    ]
}
```

**ワイルドカード:**
- `@mm-international.co.jp` - ドメイン全体を許可
- 個別のメールアドレスを列挙

**動作:**
- ホワイトリストに含まれないアカウントは自動的にブロック
- アクセス拒否は監査ログに記録

---

### 2. IPアドレス制限

**用途:** 特定のIPアドレスからのみアクセスを許可します。

**設定例:**

```json
{
    "whitelisted_ips": [
        "192.168.1.100",
        "203.0.113.0"
    ]
}
```

**動作:**
- リストが空の場合は全てのIPを許可
- リストが設定されている場合は含まれるIPのみ許可

**ユースケース:**
- オフィスのIPアドレスのみ許可
- VPN経由のアクセスのみ許可

---

### 3. ファイル形式制限

**用途:** 許可されたファイル形式のみダウンロードできるようにします。

**設定例:**

```json
{
    "allowed_file_types": [
        "pdf",
        "docx",
        "txt",
        "xlsx",
        "pptx",
        "csv",
        "md"
    ]
}
```

**動作:**
- リストに含まれないファイル形式はダウンロード拒否
- 拒否された試みは監査ログに記録

**セキュリティ上の利点:**
- 実行可能ファイル（.exe, .bat）の防止
- スクリプトファイル（.js, .vbs）の防止
- 不正なファイルの拡散防止

---

### 4. ファイルサイズ制限

**用途:** 大容量ファイルのダウンロードを防止します。

**設定例:**

```json
{
    "max_file_size_mb": 100
}
```

**動作:**
- 制限を超えるファイルはダウンロード拒否
- 拒否された試みは監査ログに記録

**セキュリティ上の利点:**
- ストレージの過度な消費防止
- 不正なデータ転送の防止

---

### 5. レート制限

**用途:** 過度なアクセスを防止します。

**設定例:**

```json
{
    "rate_limit": {
        "enabled": true,
        "max_requests_per_minute": 60,
        "max_downloads_per_hour": 100
    }
}
```

**動作:**
- 制限を超えるアクセスは一時的にブロック
- 自動化されたスクレイピングの防止

---

### 6. アクセスログ

**用途:** すべてのアクセスを記録します。

**記録内容:**
- タイムスタンプ
- アカウント
- アクション（list_folders, download_file等）
- リソース（フォルダID、ファイル名等）
- ステータス（success, denied, error）
- IPアドレス

**保存先:** `logs/google_drive_access.json`

**ログの確認:**

```python
from google_drive_security import GoogleDriveSecurityManager

security = GoogleDriveSecurityManager()
logs = security.get_access_logs(limit=100)

for log in logs:
    print(f"{log['timestamp']} - {log['account']} - {log['action']}")
```

---

### 7. 監査ログ

**用途:** セキュリティイベントを記録します。

**記録内容:**
- タイムスタンプ
- アカウント
- イベントタイプ（auth, download_denied等）
- 説明
- 重要度（info, warning, error, critical）

**保存先:** `logs/google_drive_audit.json`

**ログの確認:**

```python
security = GoogleDriveSecurityManager()
audit_logs = security.get_audit_logs(severity="warning", limit=50)

for log in audit_logs:
    print(f"{log['timestamp']} - {log['description']}")
```

---

### 8. 不正アクセス検知

**用途:** 疑わしいアクティビティを検出します。

**検知対象:**
- ホワイトリストにないアカウントからのアクセス
- 許可されていないIPアドレスからのアクセス
- 許可されていないファイル形式のダウンロード試行
- レート制限超過
- 繰り返しのアクセス拒否

**動作:**
- 検知されたイベントは監査ログに記録
- 重要度 `warning` または `error` として記録
- 設定に応じてアラートメール送信（今後実装予定）

---

## 💻 使用方法

### Pythonコードでの使用

```python
from google_drive_manager import GoogleDriveManager
from google_drive_security import GoogleDriveSecurityManager

# セキュリティ機能を有効にしてマネージャーを初期化
drive = GoogleDriveManager(
    account_config={
        'email': 'shared@mm-international.co.jp',
        'credentials_file': 'google_drive_credentials.json',
        'token_file': 'google_drive_token.pickle'
    },
    enable_security=True  # セキュリティ有効化
)

# フォルダ一覧を取得（自動的にセキュリティチェック）
folders = drive.list_folders()

# ファイルをダウンロード（自動的にセキュリティチェック）
drive.download_file(file_id, 'local_file.pdf')
```

### セキュリティダッシュボードの表示

```bash
streamlit run google_drive_security.py
```

**表示内容:**
- 総アクセス数
- 許可/拒否されたアクセス
- アカウント別統計
- 最近の拒否されたアクセス
- 重要なセキュリティイベント

---

## 📊 セキュリティレポート

### レポートの生成

```python
from google_drive_security import GoogleDriveSecurityManager

security = GoogleDriveSecurityManager()
report = security.generate_security_report()

print(f"総アクセス: {report['access_summary']['total_accesses']}")
print(f"拒否: {report['access_summary']['denied_accesses']}")
print(f"警告: {report['audit_summary']['warnings']}")
```

### レポート内容

```json
{
    "generated_at": "2025-12-13T10:00:00",
    "access_summary": {
        "total_accesses": 150,
        "allowed_accesses": 145,
        "denied_accesses": 5
    },
    "audit_summary": {
        "total_events": 20,
        "warnings": 3,
        "errors": 2
    },
    "account_statistics": {
        "shared@mm-international.co.jp": {
            "total": 100,
            "denied": 0
        }
    }
}
```

---

## 🎯 推奨設定

### セキュリティレベル: 高

```json
{
    "enabled": true,
    "whitelist_enabled": true,
    "whitelisted_accounts": ["@mm-international.co.jp"],
    "whitelisted_ips": ["192.168.1.0"],
    "allowed_file_types": ["pdf", "docx", "txt"],
    "max_file_size_mb": 50,
    "rate_limit": {
        "enabled": true,
        "max_requests_per_minute": 30,
        "max_downloads_per_hour": 50
    }
}
```

### セキュリティレベル: 中

```json
{
    "enabled": true,
    "whitelist_enabled": true,
    "whitelisted_accounts": ["@mm-international.co.jp"],
    "whitelisted_ips": [],
    "allowed_file_types": ["pdf", "docx", "txt", "xlsx", "pptx"],
    "max_file_size_mb": 100,
    "rate_limit": {
        "enabled": true,
        "max_requests_per_minute": 60,
        "max_downloads_per_hour": 100
    }
}
```

### セキュリティレベル: 標準

```json
{
    "enabled": true,
    "whitelist_enabled": false,
    "whitelisted_ips": [],
    "allowed_file_types": ["pdf", "docx", "txt", "xlsx", "pptx", "csv"],
    "max_file_size_mb": 100,
    "audit_log_enabled": true,
    "access_log_enabled": true
}
```

---

## 🔧 トラブルシューティング

### アクセスが拒否される

**原因1: アカウントがホワイトリストにない**

**解決法:**
1. `google_drive_security_config.json` を開く
2. `whitelisted_accounts` にアカウントを追加
3. または `whitelist_enabled` を `false` に設定

**原因2: ファイル形式が許可されていない**

**解決法:**
1. `allowed_file_types` にファイル形式を追加
2. 例: `"jpg"`, `"png"` 等

**原因3: ファイルサイズが制限を超えている**

**解決法:**
1. `max_file_size_mb` の値を増やす
2. または個別にファイルを確認

### ログが記録されない

**原因: ログ機能が無効**

**解決法:**
```json
{
    "audit_log_enabled": true,
    "access_log_enabled": true
}
```

### セキュリティ機能を無効にしたい

**一時的な無効化:**
```json
{
    "enabled": false
}
```

**コードでの無効化:**
```python
drive = GoogleDriveManager(enable_security=False)
```

---

## 📈 ベストプラクティス

### 1. 定期的なログの確認

```python
# 週次でセキュリティレポートを確認
security = GoogleDriveSecurityManager()
report = security.generate_security_report()

# 拒否されたアクセスを確認
if report['access_summary']['denied_accesses'] > 0:
    print("⚠️ 拒否されたアクセスがあります")
```

### 2. ホワイトリストの最小化

必要最小限のアカウントのみ許可：
```json
{
    "whitelisted_accounts": [
        "admin@mm-international.co.jp",
        "shared@mm-international.co.jp"
    ]
}
```

### 3. ファイル形式の制限

業務に必要なファイル形式のみ許可：
```json
{
    "allowed_file_types": ["pdf", "docx", "xlsx"]
}
```

### 4. レート制限の設定

通常の使用を妨げない範囲で制限：
```json
{
    "rate_limit": {
        "max_requests_per_minute": 60,
        "max_downloads_per_hour": 100
    }
}
```

### 5. ログの定期的なバックアップ

```bash
# ログファイルを定期的にバックアップ
copy logs\google_drive_access.json logs\backup\access_2025_12_13.json
copy logs\google_drive_audit.json logs\backup\audit_2025_12_13.json
```

---

## ✅ チェックリスト

セキュリティ設定完了確認：

- [ ] `google_drive_security_config.json` を作成
- [ ] アカウントホワイトリストを設定
- [ ] 許可するファイル形式を設定
- [ ] ファイルサイズ制限を設定
- [ ] レート制限を設定
- [ ] ログ機能を有効化
- [ ] セキュリティダッシュボードで動作確認
- [ ] テストアクセスで正常動作を確認
- [ ] 定期的なログ確認の運用を開始

---

## 📞 サポート

- **メール:** ai-support@mm-international.co.jp
- **セキュリティダッシュボード:** `streamlit run google_drive_security.py`
- **基本ガイド:** `GOOGLE_DRIVE_SETUP.md`

---

*最終更新：2025年12月13日*  
*株式会社エムエムインターナショナル*



