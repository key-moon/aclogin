#!/usr/bin/env python3
import argparse
import pathlib
import subprocess
import sys
import http.cookiejar
from abc import ABC, abstractmethod
from typing import List, Optional

try:
    import appdirs
except ImportError:
    print("appdirs パッケージがインストールされていません。")
    print("pip install appdirs でインストールしてください。")
    sys.exit(1)

class ToolBase(ABC):
    """ツールの基底クラス"""
    
    @property
    @abstractmethod
    def name(self) -> str:
        """ツール名を返す"""
        pass
    
    @classmethod
    def tool_exists(cls) -> bool:
        """ツールがシステムに存在するかを確認する"""
        try:
            result = subprocess.run(
                ["which", cls.name], 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE,
                text=True,
                check=False
            )
            return result.returncode == 0
        except Exception:
            return False
    
    @abstractmethod
    def store_session(self, cookie_value: str) -> bool:
        """セッションクッキーを保存する"""
        pass


class OJTool(ToolBase):
    """online-judge-tools 用のツールクラス"""
    
    name = "oj"
    
    def __init__(self, cookie_path: Optional[pathlib.Path] = None):
        self.cookie_path = cookie_path or self.default_cookie_path()
    
    @staticmethod
    def default_cookie_path() -> pathlib.Path:
        """デフォルトのクッキーパスを返す"""
        user_data_dir = pathlib.Path(appdirs.user_data_dir('online-judge-tools'))
        return user_data_dir / 'cookie.jar'
    
    def store_session(self, cookie_value: str) -> bool:
        """
        REVEL_SESSION クッキーを oj の cookie.jar に保存する
        
        Args:
            cookie_value: REVEL_SESSION クッキーの値
            
        Returns:
            bool: 保存に成功したかどうか
        """
        try:
            # 親ディレクトリが存在しない場合は作成
            self.cookie_path.parent.mkdir(parents=True, exist_ok=True)
            
            # LWPCookieJar を作成
            cookie_jar = http.cookiejar.LWPCookieJar(str(self.cookie_path))
            
            # 既存のクッキーがあれば読み込む（エラーは表示しない）
            if self.cookie_path.exists():
                try:
                    cookie_jar.load(ignore_discard=True)
                except Exception:
                    pass
            
            # AtCoder の REVEL_SESSION クッキーを設定
            from http.cookiejar import Cookie
            import time
            
            # 現在時刻（秒）
            now = int(time.time())
            # 2年後（秒）
            two_years_later = now + 60 * 60 * 24 * 365 * 2
            
            cookie = Cookie(
                version=0,
                name='REVEL_SESSION',
                value=cookie_value,
                port=None,
                port_specified=False,
                domain='atcoder.jp',
                domain_specified=True,
                domain_initial_dot=False,
                path='/',
                path_specified=True,
                secure=True,
                expires=two_years_later,
                discard=False,
                comment=None,
                comment_url=None,
                rest={'HttpOnly': None},
                rfc2109=False
            )
            
            cookie_jar.set_cookie(cookie)
            
            # クッキーを保存
            cookie_jar.save(ignore_discard=True)
            
            print(f"✅ {self.name}: クッキーを {self.cookie_path} に保存しました")
            return True
            
        except Exception as e:
            print(f"❌ {self.name}: クッキーの保存に失敗しました: {e}")
            return False


# 将来的に他のツールを追加する場合はここに実装
# class MarapiTool(ToolBase):
#     name = "marapi"
#     ...


# 利用可能なツールのリスト
AVAILABLE_TOOLS = [OJTool]


def get_installed_tools(specified_tools: Optional[List[str]] = None) -> List[ToolBase]:
    """
    インストールされているツールのリストを取得する
    
    Args:
        specified_tools: 指定されたツール名のリスト（Noneの場合は全ツールをチェック）
        
    Returns:
        List[ToolBase]: インストールされているツールのインスタンスのリスト
    """
    tools = []
    
    # ツールクラスとツール名のマッピングを作成
    tool_classes = {cls.name: cls for cls in AVAILABLE_TOOLS}
    
    # 指定されたツールがある場合はそれらのみをチェック
    if specified_tools:
        for tool_name in specified_tools:
            if tool_name in tool_classes:
                tool_cls = tool_classes[tool_name]
                if tool_cls.tool_exists():
                    tools.append(tool_cls())
                else:
                    print(f"警告: {tool_name} はインストールされていないようです")
            else:
                print(f"警告: {tool_name} は未対応のツールです")
    else:
        # 指定がない場合は全ツールをチェック
        for tool_cls in AVAILABLE_TOOLS:
            if tool_cls.tool_exists():
                tools.append(tool_cls())
    
    return tools


def main():
    parser = argparse.ArgumentParser(description='AtCoder の REVEL_SESSION クッキーを各種ツールに保存します')
    parser.add_argument('--tools', nargs='+', help='クッキーを保存するツール名（指定なしの場合は自動検出）')
    
    # ツール固有のオプションを追加
    parser.add_argument('--oj-cookie-path', type=str, help='oj のクッキーファイルのパス')
    
    args = parser.parse_args()
    
    # インストールされているツールを取得
    tools = get_installed_tools(args.tools)
    
    if not tools:
        print("エラー: 対応するツールがインストールされていません")
        sys.exit(1)

    print("検知されたツール:")
    for tool in tools:
        print(f"- {tool.name}")

    # ツール固有のオプションを適用
    for i, tool in enumerate(tools):
        if isinstance(tool, OJTool) and args.oj_cookie_path:
            tools[i] = OJTool(pathlib.Path(args.oj_cookie_path))
    
    # ユーザーにクッキーの入力を促す
    print("AtCoder の REVEL_SESSION クッキーを貼り付けてください:")
    cookie_value = input().strip()
    
    if not cookie_value:
        print("エラー: クッキーが入力されていません")
        sys.exit(1)
    
    # 各ツールにクッキーを保存
    success_count = 0
    for tool in tools:
        if tool.store_session(cookie_value):
            success_count += 1
    
    # 結果を表示
    if success_count == len(tools):
        print(f"✅ すべてのツール ({success_count}/{len(tools)}) にクッキーを保存しました")
    elif success_count > 0:
        print(f"⚠️ 一部のツール ({success_count}/{len(tools)}) にクッキーを保存しました")
    else:
        print("❌ クッキーの保存に失敗しました")
        sys.exit(1)


if __name__ == "__main__":
    main()