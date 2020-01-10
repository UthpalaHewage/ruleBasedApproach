"""Detect the subject and root_verb of a sentence at tense conversion and passive conversion"""
import spacy

nlp = spacy.load('en_core_web_sm')


def subject_and_root(sentence):
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

            return [root_verb, subject]

    return None
