from setuptools import setup, find_packages
import os

# パッケージのルートディレクトリ
here = os.path.abspath(os.path.dirname(__file__))

# バージョン情報を取得
about = {}
with open(os.path.join(here, 'aclogin', '__init__.py'), 'r', encoding='utf-8') as f:
    exec(f.read(), about)

# READMEを読み込む
with open('README.md', 'r', encoding='utf-8') as f:
    readme = f.read()

setup(
    name='aclogin',
    version=about['__version__'],
    description='AtCoderのセッションクッキーを各種ツールに保存するためのツール',
    long_description=readme,
    long_description_content_type='text/markdown',
    author='key-moon',
    author_email='',
    url='https://github.com/key-moon/aclogin',
    packages=find_packages(),
    include_package_data=True,
    python_requires='>=3.6',
    install_requires=[
        'appdirs>=1.4.4',
    ],
    entry_points={
        'console_scripts': [
            'aclogin=aclogin.cli:main',
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    keywords='atcoder, competitive-programming',
)