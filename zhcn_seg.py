# -*- encoding:utf-8 -*-

from textrank4zh import TextRank4Keyword, TextRank4Sentence
import json
import time
import re
from operator import itemgetter

t1 = time.time()

def getSegs(text):
	tempd = {}
	tr4w.analyze(text=text, lower=True, window=2)   # py2中text必须是utf8编码的str或者unicode对象，py3中必须是utf8编码的bytes或者str对象
	try:
		for word in tr4w.words_no_stop_words[0]:
			if word in tempd:
				tempd[word] += 1
			else:
				tempd[word] = 1
		return tempd
	except IndexError as e:
		return {}
	except Exception as e:
		raise e
	

def getKeywords(text, numbers = 5):
	tempd = {}
	tr4w.analyze(text = text, lower=True, window=2)
	answer_keywords = tr4w.get_keywords(numbers, word_min_len=1)
	for item in answer_keywords:
		if re.match(r"[a-zA-Z0-9]+$", item.word) is not None:
			continue
		tempd[item.word] = round(item.weight, 4)
	return tempd

'''
seg the question in FAQ
'''
jsonfile = open("d:/workspace/python-aqs/data/questions.json","r")
resfile = open("d:/workspace/python-aqs/data/questions-seg.json","w")
faqs = json.load(jsonfile)
tr4w = TextRank4Keyword()#allow_speech_tags=['r']
res = []
for faq in faqs:
	try:
		# get the segments of the question
		if faq['question'] == '' or faq['answer'] == '':
			continue
		faq['question_seg'] = getSegs(faq['question']+faq['answer'])

		# get the keywords of the answer
		faq['answer_keywords'] = getKeywords(faq['answer'])
		res.append(faq)
	except KeyError as e:
		continue
			
json.dump(res, resfile)

t2 = time.time()
dft = t2 - t1
print("project finish! cost time %s s\n" % round(dft,2))