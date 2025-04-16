class Movie:
    def __init__(self, title, year, country, length, genre, kantoku,
                 kyakuhon, cast, arasusi, characteristic_words):
        self._title = title
        self._year = year
        self._country = country
        self._length = length
        self._genre = genre
        self._kantoku = kantoku
        self._kyakuhon = kyakuhon
        self._cast = cast
        self._arasusi = arasusi
        self._characteristic_words = characteristic_words

    @property
    def title(self):
        return self._title
    
    @property
    def year(self):
        return self._year
    
    @property
    def country(self):
        return self._country

    @property
    def length(self):
        return self._length
    
    @property
    def genre(self):
        return self._genre
    
    @property
    def kantoku(self):
        return self._kantoku

    @property
    def kyakuhon(self):
        return self._kyakuhon

    @property
    def cast(self):
        return self._cast

    @property
    def arasusi(self):
        return self._arasusi

    @property
    def characteristic_words(self):
        return self._characteristic_words
    

    