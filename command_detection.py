"""Identify the commands found in the transcript-commands
used in the explanation in the verbal form"""

import spacy
import informal_word_replacement
import Shared.all_fact_list_keys as all_fact_info

nlp = spacy.load('en_core_web_sm')


class CommandDetection(object):
    """class for the detection of the commands - imperative form of statements found"""

    # import the method for the replacement of the informal words with matching formal words
    informal_word_replacement_obj = informal_word_replacement.InformalWordReplacement()

    def __init__(self):
        pass

    def command_det(self, sent_list):
        """detecting the commands and filter out them"""
        keys_list = all_fact_info.get_list_of_facts()
        for i in range(len(sent_list)):
            # make the first letter of the selected sentence into upper case
            # because if not named entities will also be detect as base verbs
            sentence = str(sent_list[i])[0].upper() + str(sent_list[i])[1:]
            sentence = nlp(sentence)

            # check whether the sent begin with base form of verb(VB)
            if str(sentence[0].tag_) == 'VB' and i not in keys_list:

                # replace the position of the commands with # for later use
                sent_list[i] = '#'

        # for sent in sent_list:
        #     print(sent)
        self.informal_word_replacement_obj.informal_word_detection(sent_list)
