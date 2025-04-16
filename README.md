# ユーザの嗜好に適応した説明文を生成する対話型英推薦システム
**Git初心者のため，ソースコードはmasterブランチに置いてあります．**  
これは私が卒業研究において作成した**対話型映画推薦システム**のデモ動画です．  
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
* BERT（文書分類）
* GPT-4o-mini（OpenAIのAPIを利用することによる）

## 使用した映画データ
[Filmarks](https://filmarks.com/)から1,936作品のメタデータと映画ごとに最低400個のレビューをスクレイピングを用いて収集しました．  

## 映画DBの作成
### 特徴語の求め方
本研究では映画の特徴を各映画の特徴語を求めることで定義しました．以下，手順
1. レビューを文に分割する（句読点や！など）
2. レビュー文を形態素解析し単語に分割する
3. **TF-IDF**を用いて各映画における単語の重要度を決定する
4. 重要度の高い最大上位40語をその映画の特徴語とする
### 特徴語と関連するレビュー文に求めかた
本研究ではユーザの嗜好に適応した説明文を生成するために，特徴語ごとに特徴語と関連するレビュー文3文求めました．
以下の基準で3文を選びました．
* レビュー文が「シーン」，「場面」，「ところ」のいずれかの単語を含んでいるかどうか
* レビュー文を構成する単語数
### 特徴語と共起頻度の高い他の特徴語
本研究ではユーザの嗜好を引き出すために，それまでに獲得したユーザの嗜好を活用してキーワード提示を行いました．
対象の特徴語と共起頻度が10%以上の他の特徴語とその共起回数を記録します．

## BERTを用いたレビュー文の分類
本研究ではユーザの嗜好に適応した説明文を生成するために，BERTを用いてレビュー文の分類を行いました．
私自身で約2,000個のレビュー文に対し以下のラベル付けを行いました．
* ラベル1：映画の内容についてポジティブに述べたレビュー文
* ラベル0：それ以外の文

その後，BERTをファインチューニングし分類モデル作成し，すべてのレビュー文に適用しました．

## 推薦アルゴリズム
本研究では対話で獲得したユーザの嗜好を表す単語と映画の特徴語の分散表現の類似度を計算することで推薦映画を決定していく方法にしました．  
分散表現を獲得するにあたり，レビュー文を用いてWord2Vecを学習しました．  手順は以下の通りです．
1. ユーザの嗜好を表す単語の分散表現を獲得する
2. 推薦候補となっている各映画の特徴語の分散表現を獲得する
3. 嗜好の分散表現と特徴語の分散表現とのコサイン類似度を計算する
4. コサイン類似度の最大値が閾値（**0.60**）未満となった場合は，その映画を推薦候補から外す

なお，この処理で推薦候補に残った映画でコサイン類似度が最大値となった特徴語は**検索に影響を与えた特徴語とします**

## キーワード提示
本研究ではユーザの他の嗜好を引き出すために，それまでに獲得したユーザの嗜好を活用してキーワード提示を行いました．
手順は以下の通りです
1. 検索に影響を与えた特徴語と関連付けてある他の特徴語を抽出する
2. 特徴語ごとに共起回数を合計する
3. 合計値の高い上位20語を提示する

## 説明文生成
検索に影響を与えた特徴語に関連付けてある3つのレビュー文をすべて取ってきます．  
そのレビュー文と検索に影響を与えた特徴語及びいくつかの指示をGpt-4o-miniのプロンプトに与えることで説明文を生成します．


