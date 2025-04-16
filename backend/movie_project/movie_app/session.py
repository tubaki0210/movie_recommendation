from .input_analysis import Input_analysis
from .utt import Utt
from .search_movie import Search_movie
from .generate_explanation import Generate_explanation
from collections import defaultdict
import MeCab
import gensim

class Session:

    parser = MeCab.Tagger(r'-r C:/MeCab/etc/mecabrc -d C:/MeCab/dic/NEologd/mecab-ipadic-neologd')
    word2vec = gensim.models.KeyedVectors.load_word2vec_format('movie_app/Word2VecModel/movie30epo100dim.bin',binary=True,unicode_errors='ignore')

    def __init__(self, session_id, system_state, dialog, preference_word, preference_movie,
                 recommend_movie, keywords, input_count, movie_data):
        self.session_id = session_id
        self.system_state = system_state
        self.dialog = dialog
        self.preference_word = preference_word
        self.preference_movie = preference_movie
        self.recommend_movie = recommend_movie
        self.keywords = keywords
        self.input_count = input_count
        self.movie_data = movie_data

    def get_keywords(self):
        result = []
        kyoki_word_dict = defaultdict(int)
        for rec_movie in self.recommend_movie:
                influence_words = rec_movie.influence
                result.extend(influence_words)
                for influence_word in influence_words:
                    movie = self.movie_data.get_movie(rec_movie.title)
                    characteristic_words = movie.characteristic_words
                    kyoki_words = characteristic_words[influence_word]['kyoki']
                    for kyoki_word in kyoki_words:
                        kyoki_word_dict[kyoki_word['word']] = kyoki_word_dict[kyoki_word['word']] + int(kyoki_word['count'])
        result = list(set(result))
        kyoki_word_dict = sorted(kyoki_word_dict.items(), key = lambda x : x[1],reverse=True)
        
        result_dict = [{"word" : word, "is_kyoki" : True, "count" : count} for word, count in kyoki_word_dict]
        for word in result:
            for kyoki_word in result_dict:
                if Session.word2vec.similarity(word, kyoki_word['word']) >= 0.60:                    
                    kyoki_word['is_kyoki'] = False
        result_dict = [value['word'] for value in result_dict if value['is_kyoki']]
        return result_dict
    
    def make_keyword(self): # 提示するキーワードを20個、取得する関数
        if len(self.keywords) >= 20:
            show_keywords = self.keywords[:20]
        else:
            show_keywords = self.keywords
        return show_keywords
    
    def remove_keywords(self, keywords):
        for sk in keywords:
            self.keywords.remove(sk)
        return self.keywords
    
    def get_genre(self, movie_title):
        genre = self.movie_data.get_movie(movie_title).genre
        return genre.split(",")

    def make_recommend_movie_list(self):
        result, genre_list = [], []
        for pre_movie in self.preference_movie:
            genre_list.extend(self.get_genre(pre_movie))
        for movie in self.recommend_movie:
            split1 = self.get_genre(movie.title)
            for element in split1:
                if element in genre_list:
                    movie.genre_score += 1
            result.append(movie)
        return sorted(result, key=lambda  x : (x.genre_score, x.sim_score, x.match_word), reverse=True)

    def first_state_run(self, utt):
        input_analysis = Input_analysis(utt.utt)
        user_preference = input_analysis.get_preference(Session.parser, Session.word2vec) # ユーザの嗜好を抽出する
        if len(user_preference) > 0: # 嗜好が1つ以上獲得できたら
            self.input_count += 1
            preference_not_list = []
            for preference in user_preference: # 獲得した嗜好の数だけ映画検索を行う
                if preference not in self.preference_word:
                    self.preference_word.append(preference)                            
                    record_recommend_movie = self.recommend_movie # 映画検索前の推薦候補となっている映画を記録しておく変数
                    search = Search_movie(self.movie_data)
                    self.recommend_movie = search.search(self.recommend_movie, preference, Session.word2vec)
                    if len(self.recommend_movie) == 0: # 映画検索により推薦映画が0個になってしまったら，映画検索前の情報に戻す
                        preference_not_list.append(preference)
                        self.recommend_movie = record_recommend_movie
                        del self.preference_word[-1]
            if preference_not_list:
                system_utt = f"{'、'.join('「' + not_pre + '」' for not_pre in preference_not_list)}というキーワードでは検索できません。別のキーワードを入力してください。"
                system_utt_object = Utt(speeker='システム', utt=system_utt, isSystem=True, new=True)
                self.dialog.append(system_utt_object.response_utt())

            if len(self.recommend_movie) <= 10: # 推薦する映画が10個以下になったらシステムの状態を2に遷移させる
                self.system_state = '2' # 好きな映画獲得状態へと移動
                system_utt = "次に，今まで見た映画の中で好きな映画があればタイトルを教えてください！「」の中に「千と千尋の神隠し」、「シン・ゴジラ」のようにタイトルを１つずつ入れてください。複数の映画を書いてもらって大丈夫です。タイトルは完璧に入力できなくても大体でいいので書いてください。"
            elif len(self.preference_word) >= 1: # 嗜好格納用のリストに１つ以上あればキーワードを提示して先に進む
                    self.system_state = '1' # キーワード提示状態に移動
                    self.keywords = self.get_keywords()
                    show_keywords = self.make_keyword() # 提示するキーワード獲得
                    self.keywords = self.remove_keywords(show_keywords)
                    system_utt = f"キーワードを提示します。\n興味あるキーワードがあれば教えてください。\nもし、他のキーワードが知りたければ「他のキーワードは？」と聞いてください。\nもちろん，このキーワード以外を入力しても構いません。\n"
                    system_utt += "、".join(['「' + pre + '」' for pre in show_keywords])       
        else: # 嗜好が１つも獲得できなかった場合は、別の言葉の入力を促す
            system_utt = "ごめんなさい！別の言葉で入力していただけると助かります！"
        self.dialog.append(Utt(speeker='システム', utt=system_utt, isSystem=True, new=True).response_utt())    
        return 

    def second_state_run(self, utt):
        if any(word in utt.utt for word in ["他", "別"]): # 「他」，「別」の言葉が入力に含まれていたら，別のキーワードを提示する
            show_keywords = self.make_keyword()
            if len(show_keywords) > 0:
                self.keywords = self.remove_keywords(show_keywords)
                system_utt = f"さらにキーワードを提示します。\n"
                system_utt = system_utt + "、".join(['「' + pre + '」' for pre in show_keywords])
            else:
                system_utt = f"キーワードはもうありません。"
            self.dialog.append(Utt(speeker='システム', utt=system_utt, isSystem=True, new=True).response_utt()) 
        else:
            self.first_state_run(utt)
        return 
    
    def third_state_run(self, utt):
        input_analysis = Input_analysis(utt.utt)
        input_preference_movie = input_analysis.get_preference_movie() # ユーザの好きな映画の取得(「」内を検索)
        if "ありません" in utt.utt: # 好きな映画がない場合は推薦に移る
            self.system_state = '3'
            # 推薦映画のランキング
            self.recommend_movie = self.make_recommend_movie_list()
            generate_explanation = Generate_explanation(self.recommend_movie[0], 'gpt-4o-mini')
            explanation = generate_explanation.generate(self.movie_data)
            system_utt = f"おすすめな映画です。\n{chr(10).join(['「' + movie.title + '」' for movie in self.recommend_movie[:3]])}"
            self.dialog.append(Utt(speeker='システム', utt=system_utt, isSystem=True, new=True).response_utt())    
            system_utt = f"タイトル：「{self.recommend_movie[0].title}」\n説明文\n{explanation}"
            self.dialog.append(Utt(speeker='システム', utt=system_utt, isSystem=True, new=True).response_utt())  
            del self.recommend_movie[0]
            
        elif len(input_preference_movie) == 0:
            system_utt = "「」で囲んで映画のタイトルを入力してください。"
            self.dialog.append(Utt(speeker='システム', utt=system_utt, isSystem=True, new=True).response_utt())                                     
        else:
            preference_movie = Search_movie(self.movie_data)
            preference_movie = preference_movie.serach_preference_movie(input_preference_movie)
            movie_check_flag = True # ユーザが映画名を入力しているかの判定フラグ
            for user_input, movie in preference_movie.items():
                # print(user_input, movie)
                if len(movie['match_movie']) > 0: # 映画名が完全一致した場合はその映画を好きな映画にする
                    system_utt =  f"「{user_input}」ですね。"
                    if user_input not in self.preference_movie:
                        self.preference_movie.append(user_input)
                elif len(movie['find_movie']) > 0: # 映画名が部分一致した場合はリストを提示し，その中から再度入力してもらう
                    movie_check_flag = False
                    system_utt = f"「{user_input}」について該当する映画があればもう一度「」の中に入力してください。\n{chr(10).join(['「' + movie + '」' for movie in movie['find_movie']])}"
                    self.dialog.append(Utt(speeker='システム', utt=system_utt, isSystem=True, new=True).response_utt())

                elif len(movie['levenshtein']) > 0: # 「シンゴジラ」のように一部抜けている場合は，レーベンシュタイン距離を利用してリストを提示する
                    movie_check_flag = False
                    system_utt = f"「{user_input}」について該当する映画があればもう一度「」の中に入力してください。\n{chr(10).join(['「' + movie[0] + '」' for movie in movie['levenshtein']])}"
                    self.dialog.append(Utt(speeker='システム', utt=system_utt, isSystem=True, new=True).response_utt())                                     
                else:
                    system_utt = f"「{user_input}」については該当する映画を見つけることができませんでした。他の入力をしてもかまいません"
                    movie_check_flag = False
                    self.dialog.append(Utt(speeker='システム', utt=system_utt, isSystem=True, new=True).response_utt())                                     
                    
            if movie_check_flag: # 好きな映画が決まったらスコア順に並び替えて推薦映画決定。同時に説明文を生成する。
                self.system_state = '3'
                self.recommend_movie = self.make_recommend_movie_list()
                generate_explanation = Generate_explanation(self.recommend_movie[0], 'gpt-4o-mini', self.movie_data)
                explanation = generate_explanation.generate()
                system_utt = f"おすすめな映画です。\n{chr(10).join(['「' + movie.title + '」' for movie in self.recommend_movie[:3]])}\n最初の映画を既に観たことがある場合には「他の映画はありますか？」と入力してください！"
                self.dialog.append(Utt(speeker='システム', utt=system_utt, isSystem=True, new=True).response_utt())    
                system_utt = f"タイトル：「{self.recommend_movie[0].title}」\n説明文\n{explanation}"
                self.dialog.append(Utt(speeker='システム', utt=system_utt, isSystem=True, new=True).response_utt())  
                del self.recommend_movie[0]    
        return 

    def forth_state_run(self, utt):
        if "他" in utt.utt: # 「他」という単語が含まれていたら別の映画を推薦する(あれば！)
            if len(self.recommend_movie) != 0: 
                generate_explanation = Generate_explanation(self.recommend_movie[0], 'gpt-4o-mini', self.movie_data)
                explanation = generate_explanation.generate()
                system_utt = f"おすすめな映画です。\n{chr(10).join(['「' + movie.title + '」' for movie in self.recommend_movie[:3]])}"
                self.dialog.append(Utt(speeker='システム', utt=system_utt, isSystem=True, new=True).response_utt())    
                system_utt = f"タイトル：「{self.recommend_movie[0].title}」\n説明文\n{explanation}"
                self.dialog.append(Utt(speeker='システム', utt=system_utt, isSystem=True, new=True).response_utt())  
                del self.recommend_movie[0]    

            else: # 推薦映画がもうない場合
                system_utt = "ごめんなさい。推薦映画はもうないです。"
                self.dialog.append(Utt(speeker='システム', utt=system_utt, isSystem=True, new=True).response_utt())  
        else:
            system_utt = "他の映画の説明文が観たい場合は「他の映画はありますか？」と入力してください！やり直したい場合は「リセット」と入力してください。"
            self.dialog.append(Utt(speeker='システム', utt=system_utt, isSystem=True, new=True).response_utt()) 
        return 
                
    def run(self, user_utt):
        utt = Utt(speeker='ユーザ', utt=user_utt, isSystem=False, new=False)
        self.dialog.append(utt.response_utt())
        if self.system_state == '0':
             self.first_state_run(utt)
        elif self.system_state == '1':
             self.second_state_run(utt)
            # for rec_movie in self.recommend_movie:
                # print(rec_movie.title,rec_movie.influence)
        elif self.system_state == '2':
             self.third_state_run(utt)
        elif self.system_state == '3':
            self.forth_state_run(utt)
        return self.dialog