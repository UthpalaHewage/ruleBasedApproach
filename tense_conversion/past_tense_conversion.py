"""Identify the sentences in past tense and make the tense conversion """
import spacy
import inflect
from pyinflect import getInflection
import tense_conversion.Models.verb_sub_container as dict_container
import tense_conversion.perfect_tense_conversion as perfect_tense_conversion

nlp = spacy.load('en_core_web_sm')


class PastTenseConversion(object):
    """class for the tense conversion of past tense sentences"""

    # import the method for the conversion of perfecr tense sentences
    perfect_tense_conversion_obj = perfect_tense_conversion.PerfectTenseConversion()

    # check for the singular nature of noun..
    # if the given noun is singular result- False. If not gives the singular form
    inflect = inflect.engine()

    def __init__(self):
        pass

    def past_tense_con(self, sent_list):
        """conversion of past tense sentences to simple tense"""
        for i in range(len(sent_list)):
            # the sent not marked with #-(for command det) and ###-(for future tense det) earlier
            # as index is checked # is enough to filter out both
            if sent_list[i][0] is not "#":
                content = dict_container.verb_sub_dict.get(i)

                if content is not None:
                    root_verb = content[0]
                    subject = content[1]
                    sentence = nlp(sent_list[i][0].upper() + sent_list[i][1:])

                    # check for the availability of past tense verb(VBD)
                    if str(sentence[root_verb].tag_) == "VBD":
                        # get the base form of the verb
                        base_verb = sentence[root_verb].lemma_

                        # continuous sent with 'I' is converted
                        if str(sentence[subject]) is "I":
                            sent_list[i] = self.i_based_sent(sentence, root_verb, base_verb)

                        # singular continuous sent is converted
                        elif self.check_singularity(sentence[subject]) is False:
                            sent_list[i] = self.singular_sent(sentence, root_verb, base_verb)

                        # plural continuous sent is converted
                        else:
                            sent_list[i] = self.plural_sent(sentence, root_verb, base_verb)

                    # used to deal with  the past tense sentences with "did not" phrase
                    elif "did" in str(sentence[subject:root_verb]):
                        mid_word = str(sentence[subject:root_verb])
                        end_word = str(sentence[root_verb:])
                        # continuous sent with 'I' is converted
                        if str(sentence[subject]) is "I":
                            sent_list[i] = mid_word.replace("did", "do").strip() + " " + end_word.strip()

                        # singular continuous sent is converted
                        elif self.check_singularity(sentence[subject]) is False:
                            sent_list[i] = mid_word.replace("did", "does").strip() + " " + end_word.strip()

                        # plural continuous sent is converted
                        else:
                            sent_list[i] = mid_word.replace("did", "do").strip() + " " + end_word.strip()

            sent_list[i] = sent_list[i][0].lower() + sent_list[i][1:]



        self.perfect_tense_conversion_obj.perfect_tense_con(sent_list)

    @staticmethod
    def i_based_sent(sentence, root_verb, base_verb):
        """conversion of sent with 'I'"""
        return str(sentence[:root_verb]).strip() + " " + base_verb + " " + str(sentence[root_verb + 1:]).strip()

    @staticmethod
    def singular_sent(sentence, root_verb, base_verb):
        """conversion of singular sent """
        # get the singular present tense verb form
        return str(sentence[:root_verb]).strip() + " " + getInflection(base_verb, tag='VBZ')[0] + " " + str(
            sentence[root_verb + 1:]).strip()

    @staticmethod
    def plural_sent(sentence, root_verb, base_verb):
        """conversion of plural sent"""
        return str(sentence[:root_verb]).strip() + " " + base_verb + " " + str(sentence[root_verb + 1:]).strip()

    # check whether the available noun is in singular form
    def check_singularity(self, subject):
        return self.inflect.singular_noun(str(subject))
