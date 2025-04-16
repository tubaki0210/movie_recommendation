# メインシステム
from rest_framework.response import Response
from rest_framework.views import APIView
import json
import random
import pandas as pd
import datetime
import time
import string
from .movie import Movie
from .utt import Utt
from .session import Session
from .recommend_movie import Recommend_movie
from .all_session import Movie_recommend
from .all_movie import All_Movie

def load_json_file(file_name): # 映画DBのJsonファイルを読み込む関数
    with open(f'movie_app/Movie_Data/{file_name}', "r", encoding='utf-8') as f:
        movie_data = json.load(f)
        f.close()
    return movie_data

def save_dialog(dialog, user_id): # 「終了」と入力されたら対話履歴を保存する関数
    speeker_list, utt_list = [], []
    for element in dialog:
        speeker_list.append(element['speeker'])
        utt_list.append(element['utt'].replace("\n",""))
    data = {"speeker" : speeker_list, "utt" : utt_list}
    df = pd.DataFrame(data)
    now = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    df.to_csv(f'./movie_app/dialog/{user_id}_{now}.csv',sep="\t",index=False)
       
def get_session_id(num): # セッションIDを半角英数字8文字で生成(ユニーク)
    return "".join(random.choices(string.ascii_letters + string.digits, k=num))

movie_data = load_json_file('movie.json') # 映画DB
all_movie = All_Movie([])
for title, detail in movie_data.items():
    movie = Movie(detail['title'], detail['year'], detail['country'], detail['length'], detail['genre'], 
                  detail['kantoku'], detail['kyakuhon'], detail['cast'], detail['arasusi'], detail['characteristic_words'])
    all_movie.add_movie(movie)

first_system_utt = "どんな映画が見たいですか？\n"\
                   "例えば，\n・「感動する映画が観たい。」\n"\
                   "・「怖い映画が観たい。」\n"\
                   "・「戦闘シーンがある映画が観たい。」\n"\
                   "・「夏に関連する映画が観たい。」\n"\
                   "・「映像が綺麗な映画が観たい。」\n"\
                   "・「出演者の演技が上手な映画が観たい。」"

input_limit = 5 # 嗜好を獲得したターンにおける入力上限回数
sessiondic = Movie_recommend([], all_movie)

class SystemUtt(APIView):
    def get(self,request): # GETメソッドが来たとき(対話システムにアクセスしてきたとき)
        if not request.GET.get('session_id'):
            session_id = get_session_id(8)
            while session_id in sessiondic.get_all_session_id():
                session_id = get_session_id(8)
            recommend_movie = [Recommend_movie(movie.title, 0, [], 0, 0, 0) for movie in all_movie.all_movie]
            sessiondic.all_session.append(Session(session_id, '0', [Utt(speeker='システム', utt=first_system_utt, isSystem=True, new=False).response_utt()], [], [], recommend_movie, [], input_limit, all_movie))
        else:
            session_id = request.GET.get('session_id')
            session_object = sessiondic.get_object(session_id)
            for item in session_object.dialog:
                item['new'] = False
        return Response({'dialog' : sessiondic.get_object(session_id).dialog, 'session_id' : session_id}) # 対話履歴とセッションIDを返す(GETメソッドが来たとき)

    def post(self,request): # POSTメソッドが来たとき(メッセージが送信されたとき)
        data = request.data
        # logout = data['isLogOut']
        session_id = data['session_id'] # セッションID
        user_utt = data['utt'] # ユーザの入力
        print(session_id,user_utt)
        start_time = time.time()
        session_object = sessiondic.get_object(session_id)
        for item in session_object.dialog:
            item['new'] = False
        response = session_object.run(user_utt)
        print(response)
        # 対話システムぽくするために応答を少し遅らせる
        end_time = time.time()
        while end_time - start_time < 0.5:    
            end_time = time.time()
        return Response(session_object.dialog) # 現在までの対話履歴をフロントに返す(POSTメソッドが来たとき)