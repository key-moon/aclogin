# AtCoder 自動ログインサポート計画

## 概要
AtCoder への `REVEL_SESSION` Cookie を、ブラウザ (Tampermonkey UserScript) から簡単に取得 → クリップボードへコピー → CLI ツール経由で複数のツール (oj, etc.) に保存するための仕組み。

## 構成要素

1. **UserScript (Tampermonkey)**
   - AtCoder ログイン済みページに「REVEL_SESSION をコピー」ボタンを設置
   - クリックすると `document.cookie` から `REVEL_SESSION` を抜き出し、`navigator.clipboard.writeText()` でクリップボードにコピー

2. **CLI ツール (`store_cookie.py`)**
   - `argparse` で `--tools` 引数を受け取り、複数のツールを指定可能  
     - 例: `python store_cookie.py --tools oj marapi`
   - `--tools` が指定されなければ、自動検知モード  
     - 事前に想定候補 ( `["oj", "marapi", ...]` ) を列挙し、 `tool_exists()` で `which` コマンド等を用いてインストール済みか確認。  
     - インストールされているツールだけを対象とする
   - ユーザーに（クリップボードからのペースト想定で）Cookie の値を入力させる  
   - 選択された複数ツールに対して、一括で Cookie を保存する

## クラス設計

### `ToolBase`
- **フィールド**:
  - `name` (str): ツール名
- **メソッド**:
  - `tool_exists()` : ツールが実行環境に存在するか ( `which <tool>` など )
  - `store_session(cookie_value: str) -> None` : Cookie の保存ロジックを実装

### `OJTool(ToolBase)`
- `name = "oj"` （例）
- `store_session(cookie_value: str)`
  - `appdirs` や `http.cookiejar.LWPCookieJar` を用いて `cookie.jar` に書き込む

### 他ツール (例: `MarapiTool`, ...)
- 同様に実装可

## 想定フロー

1. ユーザーがブラウザ (AtCoder) でログイン (CAPTCHA は手動対応)
2. Tampermonkey スクリプトのボタンで `REVEL_SESSION` クッキーをコピー
3. `python store_cookie.py` を起動
   - `--tools` を指定しない場合は自動で `oj`, `marapi` 等を検知
4. クリップボードにコピーされている Cookie 値をペースト
5. CLI が複数ツール (`OJTool`, etc.) の `store_session()` を呼び出して Cookie を保存
6. `oj` などのコマンドラインツールが AtCoder にセッション付きでアクセス可能

```mermaid
flowchart TB
    A((AtCoder\nログイン)) --> B[Tampermonkey\nREVEL_SESSION 取得]
    B --> C[クリップボードへコピー]
    C --> D[CLI (store_cookie.py)\n--tools=[oj, ...]]
    D --> E[ユーザーが Cookie をペースト]
    E --> F[ツール毎に\nCookie書き込み]
    F --> G[各ツールを用いてAtCoder操作]