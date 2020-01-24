"""Filter out the questions found on the transcript"""
import word_filteration


class QuestionDetection(object):
    """class for the detection of the questions out of the sentences"""

    # import the method for the filteration of unwanted words found in the content
    word_filteration_obj = word_filteration.WordFilteration()

    def __init__(self):
        # constructor
        pass

    @classmethod
    def identify_questions(cls, sentence):
        """identify the sentences with the presence of the ? mark and filter out the questions"""
        if "?" in sentence:
            return True

        return False

    def question_removal(self, all_sent_list):
        # obtain sentences
        for i in range(len(all_sent_list)):
            sent = str(all_sent_list[i])
            # filter out the questions available - with question_detection.py
            check_question = self.identify_questions(sent)
            # check for the availability of the questions
            if check_question:
                # check whether the sentence is a question- replace the question with "#"
                all_sent_list[i] = "#"
            else:
                # make the first letter of the sentence into lower case
                sentence = sent[0].lower() + sent[1:]
                # make the array with list of sentences
                all_sent_list[i] = sentence.strip()

        # for sent in all_sent_list:
        #     print(sent)
        self.word_filteration_obj.remove_words_by_rule_based_matching(all_sent_list)
