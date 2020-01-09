"""Used for the continuous and perfect tense conversion"""
import inflect
from pyinflect import getInflection

# check for the singular nature of noun..
# if the given noun is singular result- False. If not gives the singular form
inflect = inflect.engine()


def modifier(sentence, root_verb, subject, aux_list):
    # out of the aux identified specifically select the
    # aux matches to aux_list declared
    # 'str(sentense[idx]) in self.aux_list'
    aux_index = [idx for idx in range(len(sentence)) if
                 str(sentence[idx].dep_) == "aux" and subject < idx <
                 root_verb and str(sentence[idx]) in aux_list]
    # get the base form of the verb
    base_verb = sentence[root_verb].lemma_

    if len(aux_index) != 0:
        aux_idx = aux_index[0]
        # check the availability of 'not' in the sentence - negation
        negation_availability = True if str(sentence[aux_idx + 1]) == "not" else False

        # continuous sent with 'I' is converted
        if str(sentence[subject]) is "I":
            return i_based_sent(negation_availability, sentence, aux_idx, root_verb,
                                base_verb)

        # singular continuous sent is converted
        elif inflect.singular_noun(str(sentence[subject])) is False:
            return singular_sent(negation_availability, sentence, aux_idx, root_verb,
                                 base_verb)

        # plural continuous sent is converted
        else:
            return plural_sent(negation_availability, sentence, aux_idx, root_verb,
                               base_verb)
    return False


def i_based_sent(negation_availability, sentense, aux_idx, root_verb, base_verb):
    """conversion of sent with 'I'"""
    if negation_availability:
        return str(sentense[:aux_idx]).strip() + " do " + str(
            sentense[aux_idx + 1:root_verb]).strip() + " " + base_verb + " " + str(
            sentense[root_verb + 1:]).strip()

    return str(sentense[:aux_idx]).strip() + " " + str(
        sentense[aux_idx + 1:root_verb]).strip() + base_verb + " " + str(
        sentense[root_verb + 1:]).strip()


def singular_sent(negation_availability, sentense, aux_idx, root_verb, base_verb):
    """conversion of singular sent """
    if negation_availability:
        return str(sentense[:aux_idx]).strip() + " does " + str(
            sentense[aux_idx + 1:root_verb]).strip() + " " + base_verb + " " + str(
            sentense[root_verb + 1:]).strip()

    # VBZ - verb, 3rd person singular present
    return str(sentense[:aux_idx]).strip() + " " + str(
        sentense[aux_idx + 1:root_verb]).strip() + getInflection(base_verb, tag='VBZ')[0] + " " + str(
        sentense[root_verb + 1:]).strip()


def plural_sent(negation_availability, sentense, aux_idx, root_verb, base_verb):
    """conversion of plural sent"""
    if negation_availability:
        return str(sentense[:aux_idx]).strip() + " do " + str(
            sentense[aux_idx + 1:root_verb]).strip() + " " + base_verb + " " + str(
            sentense[root_verb + 1:]).strip()

    return str(sentense[:aux_idx]).strip() + " " + str(
        sentense[aux_idx + 1:root_verb]).strip() + base_verb + " " + str(
        sentense[root_verb + 1:]).strip()
