#-*- encoding:utf-8 -*-
import time
import json
from textrank4zh import TextRank4Keyword, TextRank4Sentence


t1 = time.time()
jsonfile = open("d:/workspace/python-aqs/data/faq.jl","r")
resfile = open("d:/workspace/python-aqs/data/keywords.txt","w")
qas_json = jsonfile.read().split("\n")
questions = []
answers = []
tr4w = TextRank4Keyword()#allow_speech_tags=['r']
for qa_json in qas_json:
	if len(qa_json) >= 1:
		qa = json.loads(qa_json)
		tr4w.analyze(text=qa['question'], lower=True, window=2)   # py2中text必须是utf8编码的str或者unicode对象，py3中必须是utf8编码的bytes或者str对象
		question_keywords = {}
		for item in tr4w.get_keywords(4, word_min_len=1):  #get the key words
			question_keywords[item.word] = round(item.weight,4)
		questions.append(question_keywords)
		answers.append(qa['answer'])
		# for phrase in tr4w.get_keyphrases(keywords_num=20, min_occur_num= 1): #get the key phrases
		#	 print(phrase)
		# print('\n')
		# print(tr4w.words_all_filters[0])
		# resfile.write("/".join(tr4w.words_all_filters[0])+'\n')
		# question = "/".join(jieba.cut(qa['question']))
		# resfile.write(question+'\n')
#dump the res to a json file
json.dump({"questions":questions,"answers":answers}, resfile)

t2 = time.time()
dft = t2 - t1
print("project finish! cost time %s s\n" % round(dft,2))