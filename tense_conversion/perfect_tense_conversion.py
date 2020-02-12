"""Identify the sentences in perfecr tense and make the tense conversion """
import spacy
import tense_conversion.sent_modifier as modifier
from passive_conversion import to_passive_voice
import Shared.subject_root_finder as finder

nlp = spacy.load('en_core_web_sm')


class PerfectTenseConversion(object):
    """class for the tense conversion of perfect tense sentences"""

    # import the method for the paasive voice conversion of the module
    to_passive_voice_obj = to_passive_voice.ConversionToPassive()

    # declare the aux_list need for the  conversion of tenses
    aux_list = ["has", "have", "had"]

    def __init__(self):
        pass

    def perfect_tense_con(self, sent_list):
        """conversion of perfect tense sentences to simple tense"""
        for i in range(len(sent_list)):
            # the sent not marked with #-(for command det) and ##-(for future tense det) earlier
            # as index is checked # is enough to filter out both
            if sent_list[i][0] is not "#":
                sentence = nlp(sent_list[i][0].upper() + sent_list[i][1:])
                # use subject_root_finder to detect subj & root_verb of the sentence
                sub_and_root = finder.subject_and_root(sentence)
                if sub_and_root is not None:
                    root_verb = sub_and_root[0]
                    subject = sub_and_root[1]

                    # check for the availability of past participle verb(VBN)
                    if str(sentence[root_verb].tag_) == "VBN":
                        result = modifier.modifier(sentence, root_verb, subject, self.aux_list)
                        if result is not False:
                            sent_list[i] = result[0].lower() + result[1:]

        # for sent in sent_list:
        #     print(sent)
        self.to_passive_voice_obj.sub_root_obj_detection(sent_list)
