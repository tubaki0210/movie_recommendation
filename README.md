# 対話型英推薦システム
*Git初心者のため，ソースコードはmasterブランチに置いてあります．*  
これは私が卒業研究において作成した*対話型映画推薦システム*のデモ動画です．  
ファイルサイズの都合上，非常に短く見にくい動画になっていますがご了承ください．

https://github.com/user-attachments/assets/07e2d42c-3773-4417-b564-978e114b0ab9

https://github.com/user-attachments/assets/ea76f82e-0011-43ea-9ce5-4ebe641bc045

## 使用技術
### フロントエンド
* React
* Next.js
* HTML
* CSS
* TypeScript
### バックエンド
* Django
* Django-RestFramework
### その他
* Word2Vec
* BERT
* GPT-4o-mini（OpenAIのAPIを利用することによる）

## 使用した映画データ
[Filmarks](https://filmarks.com/)から1,936作品のメタデータと映画ごとに最低400個のレビューを収集しました．  
## 映画ごとの特徴語の求め方
本研究では映画の特徴を各映画の特徴語を求めることで定義しました．以下，手順
1. レビューを文に分割する（句読点や！など）
2. レビュー文を形態素解析し単語に分割する
3. *TF-IDF*を用いて各映画における単語の重要度を決定する
4. 重要度の高い最大上位40語をその映画の特徴語とする
