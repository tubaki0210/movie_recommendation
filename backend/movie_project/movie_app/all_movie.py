class All_Movie:
    def __init__(self, all_movie):
        self.all_movie = all_movie
    
    def add_movie(self, target_movie):
        self.all_movie.append(target_movie)
    
    def get_movie(self, title):
        for movie in self.all_movie:
            if title == movie.title:
                return movie