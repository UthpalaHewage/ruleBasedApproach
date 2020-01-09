"""Identify the sentences in future tense and filter out them"""

import spacy
import tense_conversion.Models.verb_sub_container as dict_container
import tense_conversion.continuous_tense_conversion as continuous_tense_conversion

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
            sub_index = []
            aux_index = []
            root_verb_index = []

            # get the sent not marked with #-(for command det) earlier
            if sent_list[i][0] is not "#":
                sentense = nlp(sent_list[i][0].upper() + sent_list[i][1:])

                # check for the dep_=ROOT and pos_=VERB combination to get as the base root of the sentence
                root_verb_index = [idx for idx in range(len(sentense)) if
                                   str(sentense[idx].dep_) == "ROOT" and str(sentense[idx].pos_) == "VERB"]
                if len(root_verb_index) != 0:
                    # check for the (dep_=nsubj or dep_=nsubjpass)
                    # combination out from the sent filtered out above   to get as the subject of the sentence
                    sub_index = [idx for idx in range(len(sentense)) if
                                 str(sentense[idx].dep_) == "nsubj" or
                                 str(sentense[idx].dep_) == "nsubjpass"
                                 and idx < root_verb_index[0]]

                if len(sub_index) != 0:
                    # update the created dict with root_verb_index and sub_index for later use
                    dict_container.verb_sub_dict.update({i: [root_verb_index[0], sub_index[0]]})
                    # check for the (dep_=aux and tag_=MD combination
                    # out from the sent filtered out above  to get as the subject of the sentence
                    aux_index = [idx for idx in range(len(sentense)) if
                                 str(sentense[idx].dep_) == "aux" and str(sentense[idx].tag_) == "MD" and sub_index[
                                     0] < idx <
                                 root_verb_index[0]]
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
