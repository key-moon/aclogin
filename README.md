# aclogin

AtCoderのセッションクッキーを各種ツールに保存するためのツール

## 概要

AtCoderでは、CAPTCHAの導入によりコマンドラインツールからの自動ログインができなくなりました。
このツールは、ブラウザでログインした後のセッションクッキー（REVEL_SESSION）を取得し、
各種コマンドラインツール（oj等）のクッキーファイルに保存することで、ツールからのAtCoderへのアクセスを可能にします。

## インストール方法

### 1. Tampermonkeyスクリプトのインストール

1. [Tampermonkey](https://www.tampermonkey.net/)をブラウザにインストール
2. [atcoder_cookie_exporter.user.js](https://github.com/key-moon/aclogin/raw/main/atcoder_cookie_exporter.user.js)をインストール

### 2. CLIツールのインストール

```bash
pip install aclogin
```

## 使い方

1. ブラウザでAtCoderにログイン
2. ページ右下に表示される「REVEL_SESSIONをコピー」ボタンをクリック
3. ターミナルで以下のコマンドを実行
   ```bash
   aclogin
   ```
4. プロンプトが表示されたら、クリップボードからクッキーを貼り付け（Ctrl+V）

## オプション

```
usage: aclogin [-h] [--tools TOOLS [TOOLS ...]] [--oj-cookie-path OJ_COOKIE_PATH]

AtCoder の REVEL_SESSION クッキーを各種ツールに保存します

optional arguments:
  -h, --help            ヘルプメッセージを表示して終了
  --tools TOOLS [TOOLS ...]
                        クッキーを保存するツール名（指定なしの場合は自動検出）
  --oj-cookie-path OJ_COOKIE_PATH
                        oj のクッキーファイルのパス
```

## 対応ツール

現在、以下のツールに対応しています：

- [online-judge-tools (oj)](https://github.com/online-judge-tools/oj)

## ライセンス

MIT