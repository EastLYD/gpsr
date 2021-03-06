import nltk
from nltk.corpus import wordnet as wn
from nltk.corpus import cmudict
import networkx as nx
import matplotlib.pyplot as plt
import nlpnet



class CommandAnalyzer:
    def __init__(self):
        self.cmudict = cmudict.dict()
        nlpnet.set_data_dir("dependency")
        self.tagger = nlpnet.taggers.DependencyParser(language="en")
        pass

    def normalize(self, sentence):
        lowered_sentence = sentence.lower()
        non_polite_sentence = lowered_sentence.replace("could you", "").replace("please", "")
        normalized_sentence = non_polite_sentence
        return normalized_sentence
        
    def synsets(self, word, POS):
        word_list = wn.synsets(word)
        word_list = filter(lambda n : n.name().find(".%s." % (POS)) != -1, word_list)
        return word_list

    def tag(self, string_input):
        parsed_text = self.tagger.tag(string_input)
        parsed_text = parsed_text[0]
        return [(parsed_text.tokens[i], parsed_text.pos[i], parsed_text.heads[i], parsed_text.labels[i]) for i in range(len(parsed_text.tokens))]
        #return sent.pos
    
    def synonym(self, string_input):
        synset_list = wn.synsets(string_input)
        lemmas = flatten([syn.lemma_names() for syn in synset_list])
        vocab = list(set(lemmas))
        return vocab

    def NGramSimilarity(self, input_list, input_string, threshold=0.0):
        G = ngram.NGram(input_list)
        return G.search(input_string, threshold)


    def estimateWord(self, target_dict,target_list, target_word, threshold=0.0):
        if target_word in target_dict:
            f_pro_dict = []
            for j in range(len(target_list)):
                if target_list[j].find(" ") != -1:
                    f_multi = target_list[j].split()
                    f = []
                    for k in range(len(f_multi)):
                        f = f + ['_'] + target_dict[f_multi[k]][0]
                    f_pro_dict.append("".join(f))
                elif target_list[j].find("_") != -1:
                    f_multi = target_list[j].split("_")
                    f = []
                    for k in range(len(f_multi)):
                        f = f + ['_'] + target_dict[f_multi[k]][0]
                    f_pro_dict.append("".join(f))

                else:
                    f_pro_dict.append("".join(target_dict[target_list[j]][0]))
                    
            f_dict = dict([(f_pro_dict[j], target_list[j]) for j in range(len(target_list))])
            return f_dict[self.NGramSimilarity(f_pro_dict, "".join(target_dict[target_word][0]), threshold)]


        else:
            return self.NGramSimilarity(target_list, target_word, threshold)
                                                        
    
    def refSolver(self, grammer):
        pos = [gram[1] for gram in grammer]
        for i in range(len(grammer)):
            if grammer[i] != -1:
                ref_index = i
                break

        print "ref_index:", ref_index
        prp = ""

        
        for i in range(ref_index, 0):
            print grammer[ref_index][0]
            if grammer[ref_index][1].find("NN") != -1:
                prp = grammer[ref_index][0]
                break
        print "prp estimate:", prp
        return prp

        
    def Analyze(self, sentence):
        normalized_sentence = self.normalize(sentence)
        grammer = self.tag(normalized_sentence)
        pos = {}

        
        for gram in grammer:
            pos[gram[0]] = gram[1]

        vb = filter(lambda n : n[1].find("VB") != -1, pos.items())
        nn = filter(lambda n : n[1].find("NN") != -1, pos.items())
        prp = filter(lambda n : n[1].find("PRP") != -1, pos.items())
        print "VB:", vb
        print self.refSolver(grammer)
        print "NN:", nn
        
        
if __name__=="__main__":
    analyzer = CommandAnalyzer()

    while True:
        sentence = raw_input("input: ")
        analyzer.Analyze(sentence)
