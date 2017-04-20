# -*- encoding:utf8 -*-

class Question(object):

	def __init__(self, question, answer = '', ):
		"""
		Keyword arguments:
	    question  --  str，the original sentenc of the question in faq set.
	    answer       --  the answer of the question
	    
	    Object Var:
	    self.words_no_filter      --  对sentences中每个句子分词而得到的两级列表。
	    self.words_no_stop_words  --  去掉words_no_filter中的停止词而得到的两级列表。
	    self.words_all_filters    --  保留words_no_stop_words中指定词性的单词而得到的两级列表。
		"""
		super(Question, self).__init__()

		self.segments = None
		self.keywords = None
		self.question = arg
