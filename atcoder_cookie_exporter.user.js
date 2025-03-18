// ==UserScript==
// @name         AtCoder Cookie Exporter
// @namespace    https://github.com/key-moon/aclogin
// @version      0.1
// @description  Export REVEL_SESSION cookie from AtCoder to clipboard
// @author       key-moon
// @match        https://atcoder.jp/*
// @grant        GM_addStyle
// @grant        GM.setClipboard
// ==/UserScript==

(function() {
    'use strict';

    // スタイルを追加
    GM_addStyle(`
        #cookie-exporter-button {
            position: fixed;
            bottom: 20px;
            right: 20px;
            background-color: #0275d8;
            color: white;
            border: none;
            border-radius: 4px;
            padding: 8px 12px;
            font-size: 14px;
            cursor: pointer;
            z-index: 9999;
            box-shadow: 0 2px 5px rgba(0,0,0,0.2);
            transition: background-color 0.3s;
        }
        #cookie-exporter-button:hover {
            background-color: #025aa5;
        }
        #cookie-exporter-notification {
            position: fixed;
            bottom: 70px;
            right: 20px;
            background-color: #5cb85c;
            color: white;
            border-radius: 4px;
            padding: 12px 16px;
            font-size: 14px;
            z-index: 9999;
            box-shadow: 0 2px 5px rgba(0,0,0,0.2);
            display: none;
            opacity: 0;
            transition: opacity 0.3s;
            max-width: 300px;
            line-height: 1.4;
        }
    `);

    // ボタンを作成
    const button = document.createElement('button');
    button.id = 'cookie-exporter-button';
    button.textContent = 'REVEL_SESSIONをコピー';
    document.body.appendChild(button);

    // 通知要素を作成
    const notification = document.createElement('div');
    notification.id = 'cookie-exporter-notification';
    notification.innerHTML = `
        <strong>クッキーをクリップボードにコピーしました！</strong><br>
        <small>次のステップ: ターミナルで以下を実行してください:<br>
        <code>pip install aclogin</code><br>
        <code>aclogin</code></small>
    `;
    document.body.appendChild(notification);

    // REVEL_SESSIONクッキーを取得する関数
    function getRevelSessionCookie() {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            cookie = cookie.trim();
            if (cookie.startsWith('REVEL_SESSION=')) {
                return cookie.substring('REVEL_SESSION='.length);
            }
        }
        return null;
    }

    // 通知を表示する関数
    function showNotification() {
        notification.style.display = 'block';
        setTimeout(() => {
            notification.style.opacity = '1';
        }, 10);
        
        setTimeout(() => {
            notification.style.opacity = '0';
            setTimeout(() => {
                notification.style.display = 'none';
            }, 300);
        }, 2000);
    }

    // ボタンクリックイベント
    button.addEventListener('click', () => {
        const revelSession = getRevelSessionCookie();
        
        if (revelSession) {
            // クリップボードにコピー
            if (navigator.clipboard && navigator.clipboard.writeText) {
                navigator.clipboard.writeText(revelSession)
                    .then(() => {
                        showNotification();
                    })
                    .catch(err => {
                        console.error('クリップボードへのコピーに失敗しました:', err);
                        alert('クリップボードへのコピーに失敗しました。');
                    });
            } else if (typeof GM !== 'undefined' && GM.setClipboard) {
                // Tampermonkey API を使用
                GM.setClipboard(revelSession);
                showNotification();
            } else {
                alert('お使いのブラウザはクリップボード機能をサポートしていません。');
            }
        } else {
            alert('REVEL_SESSIONクッキーが見つかりません。AtCoderにログインしていることを確認してください。');
        }
    });
})();