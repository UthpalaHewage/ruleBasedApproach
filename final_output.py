"""final output of the formatting module"""
import Model.fact_dict as fact_dict
import Model.paragraph as para


class FinalOutput(object):
    """class for the final output"""

    final_sent_list = []
    final_para = ""

    def __init__(self):
        pass

    def final_output(self, sent_list):
        for i in range(len(sent_list)):
            flag = -1
            # to get rid of the commands,questions and future tense sent
            if len(sent_list[i].strip()) == 3:

                sent_list[i] = fact_dict.facts_on_quotes[i].strip()
                self.final_sent_list.append(sent_list[i][0].upper() + sent_list[i][1:])
                flag = i
            if sent_list[i][0] is not "#" and flag != i:
                # get the facts detected by quotes back into sentence
                if i in fact_dict.facts_on_quotes:
                    sent_list[i] = sent_list[i].strip() + " " + fact_dict.facts_on_quotes[i].strip()
                # get the facts detected by semicolon back into sentence
                if i in fact_dict.facts_on_semicolon:
                    sent_list[i] = sent_list[i].strip() + " " + fact_dict.facts_on_semicolon[i].strip()
                # get the facts detected by colon back into sentence
                if i in fact_dict.facts_on_colon:
                    sent_list[i] = sent_list[i].strip() + " " + fact_dict.facts_on_colon[i].strip()
                # get the facts detected by phrase matching back into sentence
                if i in fact_dict.facts_on_phrases:
                    sent_list[i] = sent_list[i].strip() + " " + fact_dict.facts_on_phrases[i].strip()
                # unite the contents drawn back
                # make the first letter of the sentence capital
                self.final_sent_list.append(sent_list[i][0].upper() + sent_list[i][1:])

        for sent in self.final_sent_list:
            self.final_para = self.final_para + " " + sent
            # get the output sentence vice
            print(sent)
        para.final_para = self.final_para.strip()
        print("---------------------------------------------")
        print("formatted content")
        # print(self.final_para.strip())
