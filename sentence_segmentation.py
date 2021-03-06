"""Make the transcript organized manner, segment the content sentence vice """

# Import spaCy and load the language library
import spacy
from nltk import tokenize


import Model.paragraph as para
import contraction_removal

# load small version of english library
# python -m spacy download en_core_web_sm
nlp = spacy.load('en_core_web_sm')


class SentenceSegmentation(object):
    """class for the sentence segmentation of the transcript"""

    # import the method for the conversion of the contracted words into expanded form
    contraction_removal_obj = contraction_removal.ContractionRemoval()

    def __init__(self):
        pass

    def sent_segment(self):
        """segmenting the sentence in the transcript"""
        with open('files/evaluation dataset collection/to passive-simple.txt', 'r') as file:
        # with open('files/transcript collection/8/8.1 How prepositions function, problems with prepositions.txt', 'r') as file:

            # read the text file_transcript
            data = file.read()
            # tokenize the sent and replace the uneven line breaks
        all_sent_list = tokenize.sent_tokenize(data.replace("\n", " "))
        # for sent in all_sent_list:
        #     print(sent)
        self.contraction_removal_obj.expand_contractions(all_sent_list)
        # get the complete formatted paragraph
        self.print_para()

    @staticmethod
    def print_para():
        print(para.final_para)
        para.final_para = ""
