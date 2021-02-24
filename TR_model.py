import nltk
from nltk.tokenize import word_tokenize
import eng_to_ipa as ipa
import string    

suspicious_words = set(""""abstract accent address annex ally attribute combat compound compress 
                           conduct conflict conscript consort contract contrast converse convert 
                           convict decrease desert detail discharge envelope escort exploit export 
                           extract finance fragment impact imprint increase insert insult mandate 
                           object perfect permit pervert present process produce progress project 
                           protest rampage rebel recap recall record refill refund refuse reject 
                           replay subject survey suspect torment transfer transplant transport upset""".split())

class Text:
    def __init__(self, path):
       with open(path) as file:
        self.text = file.read()
        self.annotated = nltk.pos_tag(self.remove_punctuation(), tagset='universal')
                
    def tokenize(self):
        return word_tokenize(self.text)
    
    def remove_punctuation(self):
        stripped_text = []
        for el in self.tokenize():
            if el not in string.punctuation and el != "n't" and not el.startswith("'"):
                stripped_text.append(el) 
        return stripped_text
  
    def lower(self):
        lowered_tokens = []
        for el in self.annotated:
            lowered_tokens.append(el[0].lower())
        return lowered_tokens
    
    def remove_duplicates(self):
        return set(self.annotated)
        
    def filter_tokens(self, filtering_arguments):
        chosen_words = []
        for el in self.remove_duplicates():
            if len(filtering_arguments) == 0:
                chosen_words.append(el)
            for arg in filtering_arguments:
                if el[1].startswith(arg):
                    chosen_words.append(el)
        return chosen_words   

    def transcribe(self, tokens):
        transcribed = {}
        for el in tokens:
            trans_el = ipa.ipa_list(el[0])[0]
            if len(trans_el) == 0:
                continue
            elif len(trans_el) == 1:
                transcribed[el] =[trans_el[0]]
            else:
                if el[0].lower() in suspicious_words:
                    if el[1].startswith("V"):
                        transcribed[el] = [trans_el[0]]
                    else:
                        transcribed[el] = [trans_el[-1]]
                else:
                    transcribed[el] = trans_el
        return transcribed
    
    def count_types(self):
        return len(set(self.lower()))
    
    def count_tokens(self):
        return len(self.lower())

    def type2token_ratio(self):
        return round(self.count_types() / self.count_tokens(), 3)
