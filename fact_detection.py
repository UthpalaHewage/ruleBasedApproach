"""Identify the facts available in the content"""
import re
import spacy
from spacy.matcher import PhraseMatcher
import sent_modify_fact_detection
import Model.fact_dict as fact_container_dict

nlp = spacy.load('en_core_web_sm')


class FactDetection(object):
    """class for the detection of the facts out of the content in the transcript"""
    # import the method for the modification of the sentences from which facts are extracted
    sent_modify_fact_detection_obj = sent_modify_fact_detection.SentModifyFactDetection()

    # define the pattern for the identification of quoted text
    pattern = re.compile(r"['\"](.*?)['\"]")

    def __init__(self):
        pass

    def detect_by_phrase_matching(self, sent_list):
        """detect the facts using the presence of specific phrases"""
        matcher = PhraseMatcher(nlp.vocab)

        # need to declare different phrases- added to phrase_list_for_fact_detection
        phrase_list = []
        # get use of phrase_list_for_fact_detection.txt for the phrases
        with open('Model/phrase_list_for_fact_detection.txt', 'r') as file:
            phrase_list = ["" + line.strip() + "" for line in file]

        # Convert each phrase to a Doc object:
        phrase_patterns = [nlp(text) for text in phrase_list]
        matcher.add('Fact_Matcher', None, *phrase_patterns)

        for i in range(len(sent_list)):
            sentense = nlp(sent_list[i])
            matches = matcher(sentense)

            if len(matches) > 0:
                end_index = matches[0][2]
                # dictionary is updated with the index respect to the fact
                # identified with defined phrases
                fact_container_dict.facts_on_phrases.update(({i: str(sentense[end_index:])}))
                sent_list[i] = str(sentense[:end_index])

        self.detect_by_colon(sent_list)

    def detect_by_colon(self, sent_list):
        """detect the facts using the presence of colon"""
        for i in range(len(sent_list)):

            if ":" in sent_list[i]:
                # detect the colon
                index = sent_list[i].index(":")
                # dictionary is updated with the index respect to the fact identified with colon
                fact_container_dict.facts_on_colon.update({i: sent_list[i][index:]})
                sent_list[i] = sent_list[i][:index]

        self.detect_by_semicolon(sent_list)

    def detect_by_semicolon(self, sent_list):
        """detect the facts using the presence of semicolon"""
        for i in range(len(sent_list)):

            if ";" in sent_list[i]:
                # detect the semicolon
                index = sent_list[i].index(";")
                # dictionary is updated with the index respect to the fact identified with semicolon
                fact_container_dict.facts_on_semicolon.update({i: sent_list[i][index:]})
                sent_list[i] = sent_list[i][:index]

        self.detect_by_quotes(sent_list)

        # printing the dict
        # for key in dict.facts_on_semicolon:
        #     print("semicolon dict")
        #     print(dict.facts_on_semicolon[key])

    def detect_by_quotes(self, sent_list):
        """detect the facts using the presence of quotes"""
        for i in range(len(sent_list)):
            # search for the pattern defined above
            result = self.pattern.search(sent_list[i])
            if result is not None:
                # dictionary is updated with the index respect to the fact identified with quotes
                fact_container_dict.facts_on_quotes.update({i: sent_list[i][result.start():]})

                # if the sentence(output) begins with a quote
                # it will completely replaced with ## for later use
                if result.start() == 0:
                    sent_list[i] = "##"
                else:
                    sent_list[i] = sent_list[i][:result.start()]

        self.sent_modify_fact_detection_obj.sent_modify(sent_list)
