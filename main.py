"""Develop the main method of the code"""
import sentence_segmentation


def main():
    """This is the starting point of the program"""
    # initiate the process with the segmentation of the sentences
    sentence_segmentation_obj = sentence_segmentation.SentenceSegmentation()
    sentence_segmentation_obj.sent_segment()


if __name__ == '__main__':
    main()
