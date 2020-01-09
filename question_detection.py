"""Filter out the questions found on the transcript"""


class QuestionDetection(object):
    """class for the detection of the questions out of the sentences"""

    def __init__(self):
        pass

    @classmethod
    def identify_questions(cls, sentence):
        """identify the sentences with the presence of the ? mark and filter out the questions"""
        if "?" in sentence:
            return True

        return False
