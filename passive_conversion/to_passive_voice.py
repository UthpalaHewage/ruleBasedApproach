import spacy
import inflect
from pyinflect import getInflection

from spacy.matcher import PhraseMatcher
import tense_conversion.Models.verb_sub_container as dict_container
import passive_conversion.replacement as replace
import final_output

inflect = inflect.engine()
nlp = spacy.load('en_core_web_sm')
matcher = PhraseMatcher(nlp.vocab)


class ConversionToPassive(object):
    # import the method for the final output of the module
    final_output_obj = final_output.FinalOutput()
    # list of personal pronoun list
    word_list = ["i", "I", "she", "he", "we", "you", "they", "it"]
    # list of aux_list patterns
    aux_pattern_list = ["do not", "does not"]
    # get use of obj_patterns_for identification of patterns of  object occurrences
    with open('passive_conversion/obj_patterns', 'r') as file:
        phrase_list = ["" + line.strip() + "" for line in file]

    # declare the object patterns possible in the sentences
    object_patterns = [nlp(text) for text in phrase_list]
    matcher.add('Object_Matcher', None, *object_patterns)

    aux_patterns = [nlp(text) for text in aux_pattern_list]
    matcher.add('Aux_Matcher', None, *aux_patterns)

    def __init__(self):
        pass

    def sub_root_obj_detection(self, sent_list):

        for i in range(len(sent_list)):
            # the sent not marked with #-(for command det) and ###-(for future tense det) earlier
            # as index is checked # is enough to filter out both
            if sent_list[i][0] is not "#":
                content = dict_container.verb_sub_dict.get(i)
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

                        if str(sentence[subject]) in self.word_list:
                            # check for the presence of comma to detect high complex sentences
                            comma_check = [idx for idx in range(len(sentence)) if str(sentence[idx]) in ","]
                            # sent for the replacement of the subject with "it" or "they" in replacement.py
                            # that is because the rule based conversion is quite difficult with complex sentences
                            if len(comma_check) != 0:
                                replaced_result = replace.replace_pronoun(sentence, subject)
                                sent_list[i] = replaced_result
                            # if sentence is not a complex sentence
                            else:
                                # get the object index with required conditions
                                obj_index = [idx for idx in range(len(sentence)) if
                                             (str(sentence[idx].dep_) == "obj" or
                                              str(sentence[idx].dep_) == "dobj")
                                             and idx > root_verb and (
                                                     str(sentence[idx].pos_) == "NOUN" or str(
                                                 sentence[idx].pos_) == "PROPN")]
                                if len(obj_index) != 0:

                                    result = self.get_object_bound(sentence)

                                    if result != 0:
                                        object_start_idx = result[0]
                                        object_end_idx = result[1]
                                        # check for the negation availability ; a boolean will be returned
                                        negation_availability = self.check_negation(str(sentence[:root_verb]))
                                        # responsible for passive sentence creation
                                        result = self.create_passive(sentence, int(root_verb), int(obj_index[0]),
                                                                     int(object_start_idx), int(object_end_idx),
                                                                     negation_availability)
                                        sent_list[i] = result.strip()

                                else:
                                    # replace_pronoun - call for the pronoun replacing method
                                    replaced_result = replace.replace_pronoun(sentence, subject)
                                    sent_list[i] = replaced_result
                    else:
                        # get the subject index with required conditions
                        sub_index = [idx for idx in range(len(sentence)) if
                                     str(sentence[idx].dep_) == "nsubj" or
                                     str(sentence[idx].dep_) == "nsubjpass"
                                     and str(sentence[idx]) in self.word_list]
                        if len(sub_index) != 0 and content is None:
                            # replace_pronoun - call for the pronoun replacing method
                            replaced_result = replace.replace_pronoun(sentence, sub_index[0])
                            sent_list[i] = replaced_result

        self.final_output_obj.final_output(sent_list)

    # get the object of the related sentence as per the match
    @staticmethod
    def get_object_bound(sentence):
        new_sentence = ""
        for token in sentence:
            # organize the sentence in 'token.dep_' form
            new_sentence = new_sentence + token.dep_ + " "
        new_sentence = nlp(new_sentence)
        matches = matcher(new_sentence)

        if len(matches) != 0:
            for match in matches:
                # loop the matches found and get the first matching for 'Object Matcher'
                # match[0] : refers to match id
                if nlp.vocab.strings[match[0]] == "Object_Matcher":
                    # match[1] : refers to starting word of matcher
                    # match[2] : refers to ending word of matcher
                    return [match[1], match[2]]
        return 0

    @staticmethod
    def create_passive(doc, root_idx, obj_index, obj_start, obj_end, negation_availability):
        # 'obj_end + 2' check whether sent ends with fullstop or not. If end with '.' need not to keep space in-between
        print(doc)
        try:

            if len(doc) > obj_end + 2:
                if negation_availability:
                    if inflect.singular_noun(str(doc[obj_index])) is False:

                        return str(doc[obj_start:obj_end]) + " is not " + str(
                            getInflection(doc[root_idx].lemma_, tag='VBN')[0]) + " " + str(doc[obj_end:])
                    else:
                        return str(doc[obj_start:obj_end]) + " are not " + str(
                            getInflection(doc[root_idx].lemma_, tag='VBN')[0]) + " " + str(doc[obj_end:])
                else:
                    if inflect.singular_noun(str(doc[obj_index])) is False:

                        return str(doc[obj_start:obj_end]) + " is " + str(
                            getInflection(doc[root_idx].lemma_, tag='VBN')[0]) + " " + str(doc[obj_end:])
                    else:
                        return str(doc[obj_start:obj_end]) + " are " + str(
                            getInflection(doc[root_idx].lemma_, tag='VBN')[0]) + " " + str(doc[obj_end:])
                # print(negation_availability)
            else:
                # sentence ending with object ;need keep a fullstop just after word without a space
                if negation_availability:
                    if inflect.singular_noun(str(doc[obj_index])) is False:
                        return str(doc[obj_start:obj_end]) + " is not " + str(
                            getInflection(doc[root_idx].lemma_, tag='VBN')[0]) + "."
                    else:
                        return str(doc[obj_start:obj_end]) + " are not" + str(
                            getInflection(doc[root_idx].lemma_, tag='VBN')[0]) + "."
                else:
                    if inflect.singular_noun(str(doc[obj_index])) is False:
                        return str(doc[obj_start:obj_end]) + " is " + str(
                            getInflection(doc[root_idx].lemma_, tag='VBN')[0]) + "."
                    else:
                        return str(doc[obj_start:obj_end]) + " are " + str(
                            getInflection(doc[root_idx].lemma_, tag='VBN')[0]) + "."
                # print(negation_availability)
        except:
            return str(doc)

    @staticmethod
    def check_negation(sentence):
        matches = matcher(nlp(sentence))
        if len(matches) != 0:
            for match in matches:
                # check for the availability of negation with 'do not' or 'does not'
                if nlp.vocab.strings[match[0]] == "Aux_Matcher":
                    return True
        return False
