import json
import openai
import time

def load_api_key(secrets_file="movie_app/Movie_Data/secret.json"):
    with open(secrets_file) as f:
        secrets = json.load(f)
    return secrets["OPENAI_API_KEY"]

class Generate_explanation:
    def __init__(self, target_movie, model, movie_data):
        self.target_movie = target_movie
        self.model = model
        self.key = load_api_key(secrets_file="movie_app/Movie_Data/secret.json")
        self.movie_data = movie_data
  
    def get_content(self, movie_detail):
        genre = movie_detail.genre
        year = movie_detail.year
        country = movie_detail.country
        kantoku = movie_detail.kantoku
        arasusi = movie_detail.arasusi
        characteristic_words = movie_detail.characteristic_words
        comment_list = []
        for influence_word in self.target_movie.influence:
            element = characteristic_words[influence_word]['comment']
            comment_list.extend(element)
        comment_list = list(set(comment_list))
        comment_content = ""
        comment_length = 0
        print(arasusi)
        for index, comment in enumerate(comment_list):
            comment_content = comment_content +  f"レビュー{str(index+1)}：{comment}。"
            print(f"レビュー{str(index+1)}：{comment}。")
            comment_length = comment_length + len(comment)
        content = f"[メタデータ]タイトル：{movie_detail.title}，ジャンル：{genre}，公開年：{year}，製作国：{country}，監督：{kantoku}，あらすじ：{arasusi}[レビュー]{comment_content}[重要単語]{','.join(self.target_movie.influence)}"
        return (content, comment_length)
    
    def generate(self):
        openai.api_key = self.key
        movie_detail = self.movie_data.get_movie(self.target_movie.title)
        content, comment_length = self.get_content(movie_detail)
        system_content = "これからジャンル・公開年・製作国・監督・あらすじを含む，ある映画のメタデータと，"\
                            "その映画について書かれた複数のレビューとレビュー中の重要単語を提示します。"\
                            "この時，与えられたメタデータとレビューから１つの説明文を記述してください。"\
                            "説明文を書くときは以下の注意事項を守ってください。"\
                            "1.あらすじの内容はあまり記述しないようにしてください。"\
                            "2.あらすじ内の登場人物の名前，年齢，住んでいる場所，職業などの情報は説明文に必ず含めてください"\
                            "3.重要単語に関する言及回数を増やしてください"\
                            "4.レビュー、評価、ファン、視聴者、観客、重要単語という言葉は使わないでください"\
                            "5.推薦するような口調で説明文を記述してください．"\
                            "6.基本的には全てのレビューの内容について言及してください。ただし，映画の内容に関係がないと思われるレビューは無視してください。"\
                            "7.与えられた[メタデータ]と[レビュー]から読み取れる情報のみで説明文を記述してください。"\
                            "8.映画のタイトルは説明文に含めないでください。"\
                            "9.説明文の始まりは「[監督]により[公開年]に[製作国]で製作されたこの[ジャンル]映画は[あらすじ]」としてください。ただし、[ジャンル]がその他の場合は[ジャンル]の部分は無視してください。"\
                            "10.映画のシーンについて言及している部分は必ず説明文に含めてください。"\
                            f"11.説明文は{comment_length}～{comment_length + 150}文字程度で記述してください。ただし，600文字以内で記述してください。"
        response = openai.ChatCompletion.create(
        model = self.model,
        messages=[
            {"role" : "system", "content" : system_content},
            {"role" : "user", "content" : content }
            ],
        )
        return response.choices[0]["message"]["content"]