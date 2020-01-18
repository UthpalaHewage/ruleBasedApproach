"""Replace the informal word with the corresponding formal word as suits"""
import string
import spacy
from spacy.matcher import PhraseMatcher
from spacy.matcher import Matcher
from pyinflect import getInflection
import tense_conversion.future_tense_identification as future_tense_detection

nlp = spacy.load('en_core_web_sm')


class InformalWordReplacement(object):
    """class for the replacement of the informal words with formal word"""

    # import the method for the detection of future tense sentences detection and removal
    tense_conversion_obj = future_tense_detection.FutureTenseIdentification()

    def __init__(self):
        pass

    def informal_word_detection(self, sent_list):
        """detection and replacement of informal words with formal words"""
        # get the punctuations for the manipulation
        punctuation_list = string.punctuation
        matcher_rule = Matcher(nlp.vocab)
        matcher_phrase = PhraseMatcher(nlp.vocab)
        verb_types = ["VB", "VBD", "VBG", "VBN", "VBP", "VBZ"]
        # get the list of informal word list
        with open('Model/informal_word_list.txt', 'r') as file:
            informal_word_list = ["" + line.strip() + "" for line in file]
        # get the list of formal word list
        with open('Model/formal_word_list.txt', 'r') as file:
            formal_word_list = ["" + line.strip() + "" for line in file]

        phrase_list = list()
        for i in range(len(informal_word_list)):
            word = informal_word_list[i]
            if len(word.split()) == 1 and str(nlp(word)[0].tag_) in verb_types:
                pattern = [{'LEMMA': word}, {'IS_PUNCT': True, 'OP': '?'}]
                matcher_rule.add(str(i), None, pattern)
            else:
                phrase_list.append(word)
        phrase_patterns = [nlp(text) for text in phrase_list]
        matcher_phrase.add('Informal word matcher', None, *phrase_patterns)
        # Convert each phrase to a Doc object:
        # phrase_patterns = [nlp(text) for text in informal_word_list]
        # matcher.add('Informal word matcher', None, *phrase_patterns)

        for i in range(len(sent_list)):
            sentense = nlp(sent_list[i])
            matches_1 = matcher_rule(sentense)
            matches_2 = matcher_phrase(sentense)
            matches = matches_1 + matches_2

            if len(matches) != 0:
                new_sent = ""
                # declare variable for later use
                previous_end = None
                # get match the informal word with formal word
                for match in matches:
                    informal_word = str(sentense[match[1]:match[2]])
                    word_type = str(sentense[match[1]:match[2]][0].tag_)
                    # get  the index with respect to the informal word
                    if not informal_word_list.__contains__(informal_word) and word_type in verb_types:
                        index = informal_word_list.index(sentense[match[1]:match[2]][0].lemma_)
                        formal_word = getInflection(formal_word_list[index], tag=str(word_type))[0]

                    else:
                        index = informal_word_list.index(informal_word)
                        formal_word = formal_word_list[index]
                    # get the respective formal word upon the index

                    # if it indicates a new sentence.
                    if previous_end is None:
                        new_sent = new_sent + str(sentense[:match[1]]).strip() + " " + formal_word
                        # if next character is not a punctuation need to put a space
                        if len(sentense) != match[2] and str(sentense[match[2]]) not in punctuation_list:
                            new_sent = new_sent + " "
                            previous_end = match[2]
                        else:
                            previous_end = match[2]

                    else:

                        # continuation of sentence
                        new_sent = new_sent + str(sentense[previous_end:match[1]]).strip() + " " + formal_word
                        # if next character is not a punctuation need to put a space
                        if len(sentense) != match[2] and str(sentense[match[2]]) not in punctuation_list:
                            new_sent = new_sent + " "
                            previous_end = match[2]
                        else:
                            previous_end = match[2]

                new_sent = new_sent + str(sentense[previous_end:]).strip()
                sent_list[i] = new_sent.strip()
        for sent in sent_list:
            print(sent)
        # self.tense_conversion_obj.future_tense_det(sent_list)
