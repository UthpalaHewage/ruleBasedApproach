import inflect

inflect = inflect.engine()


def replace_pronoun(sentence, subject_idx):
    # if the present subject is a singular term convert it to "it"
    if inflect.singular_noun(str(sentence[subject_idx])) is False:
        new_sentence = str(sentence[:subject_idx]).strip() + " it " + str(sentence[subject_idx + 1:]).strip()
        return new_sentence.strip()
    else:
        # if the present subject is a plural term convert it to "they"
        new_sentence = str(sentence[:subject_idx]).strip() + " they " + str(sentence[subject_idx + 1:]).strip()
        return new_sentence.strip()
