class Utt:
    def __init__(self, speeker, isSystem, utt, new):
        self.speeker = speeker
        self.utt = utt
        self.isSystem = isSystem
        self.new = new

    def response_utt(self):
        return {'speeker' : self.speeker, 'utt' : self.utt,'isSystem' : self.isSystem, 'new' : self.new }
