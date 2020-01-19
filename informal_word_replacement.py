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
        # define matchers used for replacement purpose
        matcher_rule = Matcher(nlp.vocab)
        matcher_phrase = PhraseMatcher(nlp.vocab)
        # define different types of verbs
        verb_types = ["VB", "VBD", "VBG", "VBN", "VBP", "VBZ"]
        # get the list of informal word list
        with open('Model/informal_word_list.txt', 'r') as file:
            informal_word_list = ["" + line.strip() + "" for line in file]
        # get the list of formal word list
        with open('Model/formal_word_list.txt', 'r') as file:
            formal_word_list = ["" + line.strip() + "" for line in file]

        phrase_list = list()
        for i in range(len(informal_word_list)):
            try:
                # get the words that matcher informal word list
                word = informal_word_list[i]
                # check whether the word length is 1 and it's a verb
                if len(word.split()) == 1 and str(nlp(word)[0].tag_) in verb_types:
                    # apply the rule base matching
                    # get the base verb of the selected verb
                    pattern = [{'LEMMA': word}, {'IS_PUNCT': True, 'OP': '?'}]
                    # match with according to matcher_rule
                    matcher_rule.add(str(i), None, pattern)
                else:
                    # assign the words to the list(phrase_list) that need to formalize with phrase matching technique
                    phrase_list.append(word)
            except Exception:
                continue
        # tokenize the phrases
        phrase_patterns = [nlp(text) for text in phrase_list]
        # match with according to matcher_phrase concept - direct phrase replacement
        matcher_phrase.add('Informal word matcher', None, *phrase_patterns)

        for i in range(len(sent_list)):
            # sentence tokenized
            sentense = nlp(sent_list[i])
            # check for matching with respect to rule base technique in the sentence
            matches_1 = matcher_rule(sentense)
            # check for matching with respect to phrase base technique in the sentence
            matches_2 = matcher_phrase(sentense)
            # unit the two matches into a single
            matches = matches_1 + matches_2

            # sort the matches according to the occurrence of words in the original sentence
            # with the aim of preventing the complication due to availability of two matches
            matches.sort(key=lambda x: x[1])

            if len(matches) != 0:

                try:
                    new_sent = ""
                    # declare variable for later use
                    previous_end = None
                    # get match the informal word with formal word
                    for match in matches:
                        # get the informal word of the related match in sentence
                        informal_word = str(sentense[match[1]:match[2]])
                        # get the tag as word type - of single word match
                        word_type = str(sentense[match[1]:match[2]][0].tag_)
                        # as the informal word list is in base for check for the other possibilities of occurrence
                        # (verb types)
                        # if these conditions as match get them
                        if not informal_word_list.__contains__(informal_word) and word_type in verb_types:
                            # get the index of the base form of those words in informal list
                            index = informal_word_list.index(sentense[match[1]:match[2]][0].lemma_)
                            # get the respective formal word using index.
                            # convert that formal word into initial word_type as detected(tenses)
                            formal_word = getInflection(formal_word_list[index], tag=str(word_type))[0]

                        # applies for the phrase base direct replacement
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
                except Exception:
                    sent_list[i] = str(sentense)
        # for sent in sent_list:
        #     print(sent)
        self.tense_conversion_obj.future_tense_det(sent_list)
