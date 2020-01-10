"""Identify the sentences in continuous form and make the tense conversion """
import spacy
import tense_conversion.Models.verb_sub_container as dict_container
import tense_conversion.past_tense_conversion as past_tense_conversion
import tense_conversion.sent_modifier as modifier

nlp = spacy.load('en_core_web_sm')


class ContinuousTenseConversion(object):
    """class for the tense conversion of continuous sentences"""

    # import the method for the conversion of past tense sentences
    past_tense_conversion_obj = past_tense_conversion.PastTenseConversion()

    # declare the aux_list need for the  conversion of tenses
    aux_list = ["is", "are", "am", "was", "were"]

    def __init__(self):
        pass

    def continuous_tense_con(self, sent_list):
        """conversion of continuous tense sentences to simple tense"""

        for i in range(len(sent_list)):
            # the sent not marked with #-(for command det) and ###-(for future tense det) earlier
            # as index is checked # is enough to filter out both
            if sent_list[i][0] is not "#":
                sentence = nlp(sent_list[i][0].upper() + sent_list[i][1:])
                # check for the dep_=ROOT and pos_=VERB combination to get as the base root of the sentence
                root_verb_index = [idx for idx in range(len(sentence)) if
                                   str(sentence[idx].dep_) == "ROOT" and str(sentence[idx].pos_) == "VERB"]

                if len(root_verb_index) != 0:
                    # check for the (dep_=nsubj or dep_=nsubjpass)
                    # combination out from the sent filtered out above   to get as the subject of the sentence
                    sub_index = [idx for idx in range(len(sentence)) if
                                 str(sentence[idx].dep_) == "nsubj" or
                                 str(sentence[idx].dep_) == "nsubjpass"
                                 and idx < root_verb_index[0]]

                    if len(sub_index) != 0:
                        root_verb = root_verb_index[0]
                        subject = sub_index[0]

                        if str(sentence[root_verb].tag_) == "VBG":

                            result = modifier.modifier(sentence, root_verb, subject, self.aux_list)
                            if result is not False:
                                sent_list[i] = result[0].lower() + result[1:]

        self.past_tense_conversion_obj.past_tense_con(sent_list)
