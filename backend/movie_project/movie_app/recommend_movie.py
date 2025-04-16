class Recommend_movie:
    def __init__(self, title, score, influence_words, match_word, genre_score, sim_score):
        self.title = title
        self.score = score
        self.influence = influence_words
        self.match_word = match_word
        self.genre_score = genre_score
        self.sim_score = sim_score
    
    