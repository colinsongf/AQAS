# -*- encoding:utf-8 -*-

from textrank4zh import TextRank4Keyword, TextRank4Sentence
import json
import time
import re
from operator import itemgetter

t1 = time.time()

'''
seg the question of online question
'''
tr4w = TextRank4Keyword()#allow_speech_tags=['r']
jsonfile = open("d:/workspace/python-aqs/data/questions-seg.json","r")
resfile = open("d:/workspace/python-aqs/data/IIndex_keywords.json","w")
questions = json.load(jsonfile)
IIndex_keywords = {}
print("begin to generate the Inverted Index.")
for question in questions:
	try:
		for keyword in question['answer_keywords']:
			if keyword not in IIndex_keywords:
				IIndex_keywords[keyword] = {'count':1, 'ids':[]}
			IIndex_keywords[keyword]['ids'].append(question['id'])
			IIndex_keywords[keyword]['count'] += 1
	except Exception as e:
		raise e

json.dump(IIndex_keywords,resfile)

t2 = time.time()
dft = t2 - t1
print("project finish! cost time %s s\n" % round(dft,2))