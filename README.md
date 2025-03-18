# aclogin

AtCoderのセッションクッキーを各種ツールに保存するためのツール

## 概要

AtCoderでは、CAPTCHAの導入によりコマンドラインツールからの自動ログインができなくなりました。
このツールは、ブラウザでログインした後のセッションクッキー（REVEL_SESSION）を取得し、
各種コマンドラインツール（oj等）のクッキーファイルに保存することで、ツールからのAtCoderへのアクセスを可能にします。

## インストール方法

```bash
pip install aclogin
```

## 使い方

### 1. AtCoderにログイン

ブラウザでAtCoderにログインします。

### 2. REVEL_SESSIONクッキーを取得

REVEL_SESSIONクッキーはhttpOnly属性が設定されているため、JavaScriptから直接取得できません。以下の手順で手動で取得してください。

#### Step 1: 開発者ツールを開く

キーボードで **F12** キーを押すか、右クリックして「検証」または「Inspect」を選択します。

#### Step 2: Application/Storageタブを開く

開発者ツールの上部メニューから「Application」タブをクリックします。（Firefoxの場合は「Storage」タブ）

左側のサイドバーから「Cookies」→「https://atcoder.jp 」を選択します。

#### Step 3: REVEL_SESSIONの値をコピー

クッキーの一覧から「REVEL_SESSION」という名前の行を探します。

「Value」列の値を**ダブルクリック**して選択し、右クリックしてコピーするか、Ctrl+C（MacならCmd+C）でコピーします。

![](/img/session_location.png)

### 3. CLIツールでクッキーを保存

ターミナルで以下のコマンドを実行します。

```bash
aclogin
```

プロンプトが表示されたら、コピーしたREVEL_SESSIONクッキーの値を貼り付けます（Ctrl+V）。

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