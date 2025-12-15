# Railway.appへのデプロイ手順（最も簡単！）

## Railway.appとは？
- GitHubと連携して自動デプロイ
- 無料枠あり（月5ドル分のクレジット）
- セットアップが最も簡単

## ステップ1: Railwayアカウントの作成

1. https://railway.app/ にアクセス
2. **「Start a New Project」**をクリック
3. **「Login with GitHub」**でログイン

## ステップ2: プロジェクトの作成

1. **「New Project」**をクリック
2. **「Deploy from GitHub repo」**を選択
3. リポジトリを検索：`mmi-management-department/ai-manager-app-1210`
4. リポジトリを選択

## ステップ3: 環境変数の設定

1. デプロイされたプロジェクトをクリック
2. **「Variables」**タブをクリック
3. 以下の環境変数を追加：

```
GOOGLE_API_KEY = AIzaSyCVOryUeFaYf1n8Oun9wAh9RxGYD4MkKuY
OPENAI_API_KEY = your-openai-api-key-here
AUTH_PASSWORD = your-secure-password-here
AUTH_SESSION_TIMEOUT_MINUTES = 60
AUTH_MAX_LOGIN_ATTEMPTS = 3
PORT = 8501
```

## ステップ4: デプロイ設定

1. **「Settings」**タブをクリック
2. **「Start Command」**を設定：
   ```
   streamlit run main.py --server.port=$PORT --server.address=0.0.0.0
   ```
3. **「Deploy」**をクリック

## ステップ5: 公開URLの取得

1. **「Settings」**タブで**「Generate Domain」**をクリック
2. URLが生成されます：`https://your-app.railway.app`
3. このURLをクリックしてアプリにアクセス！

## 自動デプロイの設定

Railwayは自動的にGitHubと連携しているので：

```powershell
# コードを変更
git add .
git commit -m "Update application"
git push origin main
```

**自動的に再デプロイされます！**（約2〜3分）

## 料金について

Railway.appの料金：
- **無料枠**: 月5ドル分のクレジット（約500時間の実行時間）
- **課金**: $0.000463/GB-hour のメモリ使用料

通常の社内利用であれば、**無料枠で十分です**。

## メリット

✅ GitHubとの連携が超簡単  
✅ 自動デプロイ（Gitにプッシュするだけ）  
✅ 無料枠あり  
✅ セットアップが5分で完了  
✅ ログが見やすい  
✅ カスタムドメイン対応  

## ログの確認

1. プロジェクトページで**「Deployments」**タブをクリック
2. 最新のデプロイをクリック
3. **「View Logs」**でリアルタイムログを確認

## トラブルシューティング

### エラー: "Build failed"
1. **「Deployments」**タブでログを確認
2. `requirements.txt`が正しいか確認
3. 再デプロイ：**「Redeploy」**をクリック

### アプリが起動しない
1. 環境変数が正しく設定されているか確認
2. **「Start Command」**が正しいか確認：
   ```
   streamlit run main.py --server.port=$PORT --server.address=0.0.0.0
   ```

### メモリ不足
1. **「Settings」**タブで**「Resources」**を確認
2. メモリを増やす（有料プランが必要）

## カスタムドメインの設定

1. **「Settings」**タブで**「Custom Domain」**をクリック
2. ドメイン名を入力（例：`ai-manager.yourcompany.com`）
3. DNSレコードを設定（Railwayが指示を表示）

## パフォーマンス監視

1. **「Metrics」**タブでCPU/メモリ使用量を確認
2. **「Analytics」**でアクセス統計を確認

---

## 🎯 推奨：Railway.appが最も簡単！

Streamlit Cloudがブロックされている場合、**Railway.app**が最も簡単な代替案です：

| 項目 | Streamlit Cloud | Railway.app |
|------|----------------|-------------|
| セットアップ | 簡単 | **超簡単** |
| GitHubとの連携 | 手動設定 | **自動** |
| 無料枠 | あり | あり（$5/月） |
| デプロイ時間 | 3〜5分 | **2〜3分** |
| 推奨度 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

**今すぐ試せます！** → https://railway.app/

