"""Identify the commands found in the transcript-commands
used in the explanation in the verbal form"""

import spacy
import informal_word_replacement

nlp = spacy.load('en_core_web_sm')


class CommandDetection(object):
    """class for the detection of the commands - imperative form of statements found"""
    # import the method for the replacement of the informal words with matching formal words
    informal_word_replacement_obj = informal_word_replacement.InformalWordReplacement()

    def __init__(self):
        pass

    def command_det(self, sent_list):
        """detecting the commands and filter out them"""
        for i in range(len(sent_list)):
            # make the first letter of the selected sentence into upper case
            # because if not named entities will also be detect as base verbs
            sentence = str(sent_list[i])[0].upper() + str(sent_list[i])[1:]
            sentence = nlp(sentence)
            # print(f'{sentence[0].text:{10}} {sentence[0].tag_}')

            # check whether the sent begin with base form of verb(VB)
            if str(sentence[0].tag_) == 'VB':
                # replace the position of the commands with # for later use
                sent_list[i] = '#'

        self.informal_word_replacement_obj.informal_word_detection(sent_list)
