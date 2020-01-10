"""Make the transcript organized manner, segment the content sentence vice """

# Import spaCy and load the language library
import spacy
from nltk import tokenize
import contraction_removal
import question_detection
import Model.paragraph as para

# load small version of english library
# python -m spacy download en_core_web_sm
nlp = spacy.load('en_core_web_sm')


class SentenceSegmentation(object):
    """class for the sentence segmentation of the transcript"""
    # import the method for the conversion of the contracted words into expanded form
    contraction_removal_obj = contraction_removal.ContractionRemoval()
    # import the method for the filteration of the questions in the content
    question_detection_obj = question_detection.QuestionDetection()

    def __init__(self):
        pass

    def sent_segment(self):
        """segmenting the sentence in the transcript"""
        with open('files/informal collection.txt', 'r') as file:
        # with open('files/selected 6 transcripts/extra/test/v_1.txt','r') as file:
            # read the text file_transcript
            data = file.read()
            # tokenize the sent and replace the uneven line breaks
        all_sent_list = tokenize.sent_tokenize(data.replace("\n", " "))

        sent_list = []
        # obtain sentences
        for sent in all_sent_list:
            sent = str(sent)
            # filter out the questions available - with question_detection.py
            check_question = self.question_detection_obj.identify_questions(sent)
            # check for the availability of the questions
            if check_question:
                # check whether the sentence is a question
                pass
            else:
                # make the first letter of the sentence into lower case
                sentence = sent[0].lower() + sent[1:]
                # make the array with list of sentences
                sent_list.append(sentence.strip())
                # print(sent)

        self.contraction_removal_obj.expand_contractions(sent_list)
        self.print_para()

    @staticmethod
    def print_para():
        print(para.final_para)
        para.final_para = ""
