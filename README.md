# [Houdini] Force Cook Tool
ノードを強制的に再クックするためのツールです。

## 動作確認環境
Houdini Indie Limited-Commercial 21.0.440

## 導入方法
本ツールはシェルフツールです。
script.pyの内容を登録してください。
詳細な手順に関しては、過去に作成したツールとほぼ同様ですので、そちらをご参照ください。

[[Houdini] Bezier Curve Tool](https://github.com/iribo0425/bezier_curve_tool?tab=readme-ov-file#%E5%B0%8E%E5%85%A5%E6%96%B9%E6%B3%95)

## 使用方法&GUI説明
<img src="image/usage000.jpg" width="400">

| | |
| - | - |
| Add Button | 選択中のノードに強制クックのボタンを追加します。<br><img src="image/usage001.jpg" width="200"> |
| Force Cook Display Node | 表示フラグがONになっているノードより上流の全ノードをクックします。<br>以下の例では、null1より上流のpythonノードとsubnetノードの中身を全てクックします。<br><img src="image/usage002.jpg" width="200"> |

