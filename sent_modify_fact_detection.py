"""Modify the sentence fragments that remain after the extraction of the facts at fact_detection"""
import spacy
import command_detection
import Model.fact_dict as fact_container_dict

nlp = spacy.load('en_core_web_sm')


class SentModifyFactDetection(object):
    """class for modification of the sentence segment after fact detection
    into present tense if available with any other tense"""
    # import the method for the detection of the commands found
    command_detection_obj = command_detection.CommandDetection()

    def __init__(self):
        pass

    def sent_modify(self, sent_list):
        """modify the sentences fragments remains"""
        # get the keys for the facts detected
        keys_list = self.get_list_of_facts()

        for key in keys_list:
            # print(sent_list[key])
            tokenized_sent = nlp(sent_list[key])

            # tokenized and get the root-verb and check the tense.
            for token in tokenized_sent:
                # check for the verb of the sentence with the ROOT authority
                # (VBD -verb, past tense)
                if str(token.dep_) == 'ROOT' and str(token.tag_) == 'VBD':
                    # If it is any other tense convert to base form - (lemma_)
                    new_sent = str(tokenized_sent[:token.i]) + " " + str(token.lemma_) + " " + str(
                        tokenized_sent[token.i + 1:])
                    sent_list[key] = new_sent.strip()
                    # to get out of the conversion process
                    break

        self.command_detection_obj.command_det(sent_list)

    @classmethod
    def get_list_of_facts(cls):
        """used to obtain the details(keys) of the facts extracted"""
        keys = []

        # unit the 3 dict obtained through the fact collection
        all_dict = {**fact_container_dict.facts_on_phrases, **fact_container_dict.facts_on_quotes, **fact_container_dict.facts_on_colon}

        for key in all_dict:
            keys.append(key)

        return keys
