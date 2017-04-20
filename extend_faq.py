# -*- encoding:utf8 -*-

import json
import os
from operator import itemgetter, attrgetter
from textrank4zh import TextRank4Keyword, TextRank4Sentence

def isInFAQ(faq_extend, question):
	for mid,q in faq_extend.items():
		print(q['answer'])
		print(question['answer'])
		if isSameSentence(q['answer'],question['answer']):
			return mid
		else:
			return False

def isSameSentence(s1,s2):
	tr4w.analyze(text=s1, lower=True, window=2)
	s1_seg = tr4w.words_no_stop_words[0]
	s1_keyword = tr4w.get_keyphrases(keywords_num=5, min_occur_num= 2)
	tr4w.analyze(text=s2, lower=True, window=2)
	s2_seg = tr4w.words_no_stop_words[0]
	s2_keyword = tr4w.get_keyphrases(keywords_num=5, min_occur_num= 2)
	if s1_seg == s2_seg and s1_keyword == s2_keyword:
		return True
	else:
		return False

filedir = os.path.abspath("./data/IIndex_phase.json")
jsonfile = open(filedir,"r")
IIndexs = json.load(jsonfile)
tr4w = TextRank4Keyword()#allow_speech_tags=['r']

phase_tuples = []
for (word,wdict) in IIndexs.items():
	phase_tuples.append((word, wdict['count']))

phase_tuples.sort(key=itemgetter(1), reverse=True)
for k,v in phase_tuples:
	print(k+" "+str(v))
exit()
del phase_tuples[0]
del phase_tuples[0]
del phase_tuples[0]

faq_extend_ids = []
for k,v in phase_tuples:
	# print(k+" %s" % v)
	if v >= 10:
		faq_extend_ids.append(IIndexs[k]['ids'])

qfile = open(os.path.abspath("./data/questions.json"), "r")
questions = json.load(qfile)
extend_faq = open(os.path.abspath("./data/test_question_new.txt"), "wb")

faq_extend = {}
for i in range(0, len(faq_extend_ids)):
	for qid in faq_extend_ids[i]:
		for question in [q for q in questions if q['id'] == qid]:
			question['question'] = question['question'].strip(' \n\r')
			question['answer'] = question['answer'].strip(' \n\r')
			# extend_faq.write((question['question']+'\r\n').encode('utf8'))
			extend_faq.write(('question:'+question['question']+'\nanswer:'+question['answer']+'\n').encode('utf8'))
			mid = isInFAQ(faq_extend, question)
			if mid:
				faq_extend[mid]['count'] += 1
			else:
				tempd = {}
				tempd['question'] = question['question']
				tempd['answer'] = question['answer']
				tempd['count'] = 1
				faq_extend[question['id']] = tempd
	extend_faq.write(b'---------------------------------------------------\r\n\r\n')