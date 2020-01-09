"""Replace the informal word with the corresponding formal word as suits"""
import string
import spacy
from spacy.matcher import PhraseMatcher
import tense_conversion.future_tense_identification as future_tense_detection

nlp = spacy.load('en_core_web_sm')


class InformalWordReplacement(object):
    """class for the replacement of the informal words with formal word"""
    # import the method for the detection of future tense sentences detection and removal
    tense_conversion_obj = future_tense_detection.FutureTenseIdentification()

    def __init__(self):
        pass

    def informal_word_detection(self, sent_list):
        """detection and replacement of informal words with formal words"""
        # get the punctuations for the manipulation
        punctuation_list = string.punctuation
        matcher = PhraseMatcher(nlp.vocab)

        # get the list of informal word list
        with open('Model/informal_word_list.txt', 'r') as file:
            informal_word_list = ["" + line.strip() + "" for line in file]
        # get the list of formal word list
        with open('Model/formal_word_list.txt', 'r') as file:
            formal_word_list = ["" + line.strip() + "" for line in file]

        # Convert each phrase to a Doc object:
        phrase_patterns = [nlp(text) for text in informal_word_list]
        matcher.add('Informal word matcher', None, *phrase_patterns)

        for i in range(len(sent_list)):
            sentense = nlp(sent_list[i])
            matches = matcher(sentense)

            if len(matches) != 0:
                # print(sentense[matches[0][1]:matches[0][2]])
                new_sent = ""
                # declare variable for later use
                previous_end = None
                # get match the informal word with formal word
                for match in matches:
                    informal_word = str(sentense[match[1]:match[2]])
                    # get  the index with respect to the informal word
                    index = informal_word_list.index(informal_word)
                    # get the respective formal word upon the index
                    formal_word = formal_word_list[index]

                    # if it indicates a new sentence.
                    if previous_end is None:
                        new_sent = new_sent + str(sentense[:match[1]]).strip() + " " + formal_word
                        # if next character is not a punctuation need to put a space
                        if str(sentense[match[2]]) not in punctuation_list:
                            new_sent = new_sent + " "
                            previous_end = match[2]
                        else:
                            previous_end = match[2]

                    else:

                        # continuation of sentence
                        new_sent = new_sent + str(sentense[previous_end:match[1]]).strip() + " " + formal_word
                        # if next character is not a punctuation need to put a space
                        if str(sentense[match[2]]) not in punctuation_list:
                            new_sent = new_sent + " "
                            previous_end = match[2]
                        else:
                            previous_end = match[2]

                new_sent = new_sent + str(sentense[previous_end:]).strip()
                # print(new_sent.strip())

                sent_list[i] = new_sent.strip()

        self.tense_conversion_obj.future_tense_det(sent_list)
