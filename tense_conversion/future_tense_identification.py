"""Identify the sentences in future tense and filter out them"""

import spacy
import tense_conversion.continuous_tense_conversion as continuous_tense_conversion
import Shared.subject_root_finder as finder

nlp = spacy.load('en_core_web_sm')


class FutureTenseIdentification(object):
    """class for the detection and removal of sentences in future tense"""
    # import the method for the conversion of continuous tense sentences
    continuous_tense_conversion_obj = continuous_tense_conversion.ContinuousTenseConversion()

    def __init__(self):
        pass

    def future_tense_det(self, sent_list):
        """detection of sentences in future tense and remove"""
        for i in range(len(sent_list)):
            # declare variables for later use
            aux_index = []

            # get the sent not marked with #-(for command det) earlier
            if sent_list[i][0] is not "#":
                sentense = nlp(sent_list[i][0].upper() + sent_list[i][1:])
                # use subject_root_finder to detect subj & root_verb of the sentence
                sub_and_root = finder.subject_and_root(sentense)
                if sub_and_root is not None:
                    root_verb = sub_and_root[0]
                    subject = sub_and_root[1]
                    # check for the (dep_=aux and tag_=MD combination
                    # out from the sent filtered out above  to get as the subject of the sentence
                    aux_index = [idx for idx in range(len(sentense)) if
                                 str(sentense[idx].dep_) == "aux" and str(
                                     sentense[idx].tag_) == "MD" and subject < idx < root_verb]
                    if len(aux_index) != 0:
                        for aux in aux_index:
                            # filter out the sentences with will/shall - future tense sentences
                            if str(sentense[aux]) in ["will", "shall"]:
                                # get the details as an  output
                                # print(sentense)
                                # print(sentense[root_verb_index[0]])
                                # print(sentense[sub_index[0]])
                                # print(sentense[aux])
                                # print("")

                                # replace the future tense sentences with "###"
                                sent_list[i] = "###"

        # #print the updated index of dict with the respective sentense
        # for key in dict.verb_sub_dict:
        #     print(sent_list[key])
        #     print(dict.verb_sub_dict[key])
        #     print("")

        self.continuous_tense_conversion_obj.continuous_tense_con(sent_list)
