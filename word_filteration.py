"""Make the words filtered out as per defined"""

import spacy
from spacy.matcher import Matcher
import Model.rule_based_word_patterns as pattern_dict
import sent_modify_fact_detection
import Shared.all_fact_list_keys as all_fact_info

nlp = spacy.load('en_core_web_sm')
# Import the Matcher library
matcher = Matcher(nlp.vocab)


class WordFilteration(object):
    """class for the filteration of the word as suits with different patterns"""
    # import the method for the modification of the sentences from which facts are extracted
    sent_modify_fact_detection_obj = sent_modify_fact_detection.SentModifyFactDetection()

    def __init__(self):
        pass

    # added the word patterns of same word that need to be filtered out
    def remove_words_by_rule_based_matching(self, sent_list):
        # get the keys for the facts detected
        keys_list = all_fact_info.get_list_of_facts()
        """remove the words that need to be filtered out- match to different patterns declared"""
        filtered_list = []
        # getting ist of patterns for removal of unnecessary word
        for pattern in pattern_dict.dict_of_patterns:
            matcher.add(pattern, None, pattern_dict.dict_of_patterns[pattern])

        for i in range(len(sent_list)):
            doc = nlp(sent_list[i])
            found_matches = matcher(doc)

            sentence = ""
            # declare variable for later use
            previous_end = None
            # check for the matching words in the list
            if len(found_matches) != 0:
                for matches in found_matches:
                    if previous_end is None:
                        # at the initial point make the match to filter
                        sentence = sentence + " " + str(doc[:matches[1]]).strip()
                        previous_end = matches[2]

                    else:
                        # continue to match and filter and progress
                        sentence = sentence + " " + str(doc[previous_end:matches[1]]).strip()
                        previous_end = matches[2]

                # finalized the output after filteration
                sentence = sentence + " " + str(doc[previous_end:]).strip()
                sent_list[i] = sentence.strip()

            # check for the sentence fragments whether it satisfy the
            # general conditions to be a sentence (availability of min of 3 word)
            # split is used here to get the number of word(count with aid of white space)
            if len(sent_list[i].strip().split()) > 2 or sent_list[i][0] is "#" or i in keys_list:
                pass
            else:
                sent_list[i] = "#"
        # self.fact_detection_obj.detect_by_phrase_matching(filtered_list)
        self.sent_modify_fact_detection_obj.sent_modify(sent_list)
