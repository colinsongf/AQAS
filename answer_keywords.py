# -*- encoding:utf-8 -*-

import json
import re
from textrank4zh import TextRank4Keyword, TextRank4Sentence

words_file = open("d:/workspace/python-aqs/data/faq-seg.json","r")
qa_list = json.load(words_file)

tr4w = TextRank4Keyword()#allow_speech_tags=['r']

for qa in qa_list:
	if 'answer' in qa:
		tempd = {}
		tr4w.analyze(text = qa['answer'], window=2)
		answer_keywords = tr4w.get_keywords(5, word_min_len=1)
		for item in answer_keywords:
			if re.match(r"[a-zA-Z0-9]+$", item.word) is not None:
				continue
			tempd[item.word] = round(item.weight, 4)
		qa['answer_keywords'] = tempd