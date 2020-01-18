"""Make the contractions found in the content into expanded form- contraction removal"""

import re
# to install contractions - pip install contractions
from contractions import contractions_dict
import fact_detection


class ContractionRemoval(object):
    """class for the expansion of the contracted forms of words found in the content"""
    # when 'I' losses its capitalization when at first place
    # then won't detect as pronoun so need to forcefully give the expansion form
    contractions_dict.update({'i\'m': 'i am'})
    contractions_dict.update({'i\'ll': 'i will'})
    contractions_dict.update({'i\'d': 'i would'})
    contractions_dict.update({'i\'ve': 'i have'})
    contractions_dict.update({'i\'d': 'i had'})
    contractions_dict.update({'here\'s': 'here is'})

    # import the method for the detection of facts for preserve its meaning
    fact_detection_obj = fact_detection.FactDetection()

    def __init__(self):
        pass

    def expand_contractions(self, sentence_list):
        """make the contraction identified and make them expanded"""
        # to get the expanded form of contraction with expand_match
        contractions_pattern = re.compile('({})'.format('|'.join(contractions_dict.keys())))

        def expand_match(contraction):
            """get the matching form of the contractions available"""
            match = contraction.group(0)
            # make the selection for expanded form
            expanded_contraction = contractions_dict.get(match) \
                if contractions_dict.get(match) \
                else contractions_dict.get(match.lower())
            # assign the expanded form into expanded_contraction
            return expanded_contraction

        removed_contractions_sentence_list = []
        for sentense in sentence_list:
            # sub-for replacing the contraction with expanded form
            # expanded_text-> the new sentence with contraction replaced
            # sent_list[i][0].upper() + sent_list[i][1:]
            expanded_text = str(contractions_pattern.sub(expand_match, sentense[0].lower() + sentense[1:]))
            # join the expanded text into the original sentence
            removed_contractions_sentence_list.append(expanded_text[0].upper() + expanded_text[1:])

        self.fact_detection_obj.detect_by_phrase_matching(removed_contractions_sentence_list)
