# 入力解析を行う
import re
# 名詞，形容詞，動詞のストップワード
with open("movie_app/word_file/noun_stop.txt", "r", encoding='utf-8') as f1, open("movie_app/word_file/adjective_stop.txt", "r", encoding='utf-8') as f2, open("movie_app/word_file/verb_stop.txt", "r", encoding='utf-8') as f3:
    noun_stop = f1.read().splitlines()
    adjective_stop = f2.read().splitlines()
    verb_stop = f3.read().splitlines()
    f1.close()
    f2.close()
    f3.close()

# 品詞細分類でのストップ
stop_pos = ["接尾","副詞可能","代名詞","数","固有名詞"]

# 固有名詞で受け入れる単語
with open("movie_app/word_file/koyu_main.txt", "r", encoding='utf-8') as f:
    allow_koyu = f.read().splitlines()
    f.close()

class Input_analysis:

    def __init__(self, utt):
        self.utt = utt
    
    def get_preference(self, parser, word2vec):
        result = self.parse(parser, word2vec)
        return result
    
    def get_preference_movie(self):
        pattern = '(?<=「).+?(?=」)'
        result = re.findall(pattern, self.utt)
        return result
    
    def parse(self, parser, word2vec):
        parse_result = parser.parse(self.utt)
        parse_result = parse_result.strip()
        result = []
        for keitaiso in parse_result.split("\n"):
            try:
                split1 = keitaiso.split("\t")
                split2 = split1[1].split(",")
                if split2[0] == "名詞":
                    if split1[0] not in noun_stop:
                        if split2[1] == "固有名詞":
                            if split1[0] in allow_koyu and split1[0] in word2vec:
                                result.append(split1[0])
                        else:
                            if split2[1] not in stop_pos and split1[0] in word2vec:
                                result.append(split1[0])
                elif split2[0] == "形容詞":
                    if split2[6] not in adjective_stop and split2[1] == "自立" and split2[6] in word2vec:
                        result.append(split2[6])
                elif split2[0] == "動詞":
                    if split2[6] not in verb_stop and split2[1] == "自立" and split2[6] in word2vec:
                        result.append(split2[6])
            except:
                continue
        return result