#-*- encoding:utf-8 -*-
import math
import jieba
import json
import os
from operator import itemgetter, attrgetter
from collections import OrderedDict
import numpy as np
from textrank4zh import TextRank4Keyword, TextRank4Sentence

def calTF(qa_list):
	all_words = {}
	for qa in qa_list:
		question = qa['question_seg'] #refer equal
		word_count = sum(question.values())
		for word in question:
			if word in all_words:
				all_words[word] += question[word]
			else:
				all_words[word] = question[word]
			question[word] = round(question[word]/word_count,4)

	return all_words

def calcIDF(all_words):
	words_idf = {} # OrderedDict()
	max_count = max(all_words.values())
	# print(question_sum)
	for word,count in all_words.items():#calc one word in different classes's variance
		# print(word)
		# print(count)
		words_idf[word] = round(math.log(float(max_count)/(float(count)+0.0001)),4)
		# temp.append((word, round(math.log(float(max_count)/(float(count)+0.0001)),4)))
		# print(words_idf[word])
	# words_idf = OrderedDict(sorted(words_idf.items(),key=operator.itemgetter(1,0)))
	return words_idf

def questionPreprocess(sentence):
	#init the seg module
	tr4w = TextRank4Keyword()#allow_speech_tags=['r']
	tr4w.analyze(text=sentence, lower=True, window=2)	#seg the sentence
	ask_seg = {}
	for word in tr4w.words_no_filter[0]:
		if word in ask_seg:
			ask_seg[word] += 1
		else:
			ask_seg[word] = 1
	
	
	#standardization
	word_count = sum(ask_seg.values())
	for word in ask_seg:
		ask_seg[word] = round(ask_seg[word]/word_count, 4)

	return ask_seg

def getVector(words_idf,sentence_seg):
	v = []

	for word in words_idf:
		if word in sentence_seg:
			v.append(words_idf[word]*sentence_seg[word])
		else:
			temp = {}
			for wordt in sentence_seg.keys():
				temp[wordt] = calWordSemanticsSim(word,wordt)

			wordt = max(temp.items(),key=itemgetter(1))
			v.append(words_idf[word]*sentence_seg[wordt[0]]*wordt[1])

	return np.array(v)

def generateQuestionVectors(qa_list):
	# get the vector of all the questions
	# questions_vectors = []
	for qa in qa_list:
		question_seg = qa['question_seg']
		v = getVector(words_idf,question_seg)
		qa['question_vector'] = v
	# return questions_vectors

def calCOS(v1,v2):
	l1 = math.sqrt(v1.dot(v1))
	l2 = math.sqrt(v2.dot(v2))
	cos = v1.dot(v2)/(l1*l2)

	return cos

def generateSynDict(path):
	dictfile = open(path,"r",encoding='utf8')
	lines = dictfile.read().split('\n')
	lines[0] = lines[0][1:]

	words_table = {}
	for wordstr in lines:
		words = wordstr.split(' ')
		for i in range(1,len(words)):
			words_table[words[i]] = words[0]

	return words_table

def calWordSemanticsSim(w1, w2):
	try:
		code1 = syn_table[w1]
		code2 = syn_table[w2]

		for i in range(0,7):
			if code1[i] != code2[i]:
				break
		alpha = 1
		if code1 == code2:
			if code1[7] == '#':
				alpha = 0.5

		return (2*i**2/(7**2+i**2))*alpha
	except KeyError as e:
		return 0

try:
	# read the faq-seg file
	words_file = open(os.path.abspath("./data/faq-seg.json"),"r")
	qa_list = json.load(words_file)
	all_words = calTF(qa_list)
	words_idf = calcIDF(all_words)

	# get the syn dict
	syn_table = generateSynDict(os.path.abspath("./data/worddict_utf8.txt"))

	#read test question file
	test_questions = open(os.path.abspath("./data/test_questions.txt"),"r", encoding='utf8').read().split('\n')
	test_questions[0] = test_questions[0][1::]
except FileNotFoundError as e:
	print("can't open the file!")
	exit()

#cal sim by the tfidf
test_questions = ['新书公告在哪里看？']
test_res = open(os.path.abspath('./data/test_res.txt'),"w",encoding='utf8')

for test_question in test_questions:
	try:
		test_res.write("the test question is:" + test_question + '\n')
		test_question_seg = questionPreprocess(test_question)
		test_res.write("the seg of the question is:"+'/'.join(test_question_seg) + '\n')
		test_question_vector = getVector(words_idf, test_question_seg)
		print(test_question_vector)
		# test_res.write("the vector of the test question is:\n")
		# test_res.write(test_question_vector)
		question_vectors = generateQuestionVectors(qa_list)
		res = []
		for qa in qa_list:
			question_vector = qa['question_vector']
			res.append(round(calCOS(test_question_vector, question_vector),4))
		answer_index = res.index(max(res))
		if res[answer_index] >= 0.7:
			test_res.write("the cos is:"+str(res[answer_index]) + '\n')
			test_res.write("the answer of the test question is:"+qa_list[answer_index]['answer'] + '\n')
			test_res.write("the actual question is:"+qa_list[answer_index]['question'] + '\n')
			test_res.write("the actual question seg is:\n")
			test_res.write(str(qa_list[answer_index]['question_seg']) + '\n')
		else:
			test_res.write("fail to find the answer!")
			test_res.write('\n')
	except IndexError as e:
		print(test_question)
		continue
	except ValueError as e:
		print(test_question)
		continue
	except Exception as e:
		print("the test question is:" + test_question + '\n')
		print(test_question_seg)
		raise e
		exit()
	