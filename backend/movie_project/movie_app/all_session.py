class Movie_recommend:
    def __init__(self, all_session, all_movie):
        self.all_session = all_session
        self.all_movie = all_movie
    
    def get_all_session_id(self):
        return [session_id for session_id in self.all_session]
    
    def get_object(self, session_id):
        for item in self.all_session:
            if session_id == item.session_id:
                return item