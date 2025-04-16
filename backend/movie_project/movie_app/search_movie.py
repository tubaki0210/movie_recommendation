# 推薦候補の映画の絞り込みや好きな映画受け取った際の検索を行う
from Levenshtein import ratio

class Search_movie:
    def __init__(self, movie_data):
        self.movie_data = movie_data

    def search(self, recommend_movie, preference, model):
        result = [] 
        for movie in recommend_movie:
            user_pre = [{'word' : feature_word, 'sim' : model.similarity(preference, feature_word)} for feature_word in (self.movie_data.get_movie(movie.title)).characteristic_words if model.similarity(preference, feature_word) >= 0.60]
            user_pre = sorted(user_pre, key = lambda x : x['sim'], reverse=True)
            if user_pre:
                if user_pre[0]['word'] not in movie.influence:
                    movie.influence.append(user_pre[0]['word'])
                movie.sim_score = movie.sim_score + user_pre[0]['sim']
                movie.match_word += len(user_pre)
                result.append(movie)
        result = sorted(result, key= lambda x : x.sim_score, reverse=True)
        return result
    
    def serach_preference_movie(self, preference_movie):
        result_dict = {}
        for pre_movie in preference_movie:
            serach_dict = {"match_movie" : [], "find_movie" : [], 'levenshtein' : []}
            for movie in self.movie_data.all_movie:
                if pre_movie == movie.title:
                    serach_dict['match_movie'].append(movie.title)
                elif movie.title.find(pre_movie) != -1:
                    serach_dict['find_movie'].append(movie.title)
                else:
                    sim = ratio(pre_movie, movie.title)
                    if sim > 0.5:
                        serach_dict['levenshtein'].append((movie.title, sim))
            serach_dict['levenshtein'] = sorted(serach_dict['levenshtein'], key=lambda x : x[1],reverse=True)
            result_dict[pre_movie] = serach_dict        
        return result_dict