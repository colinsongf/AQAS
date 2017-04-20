#-*- encoding:utf-8 -*-
import math
import jieba
import json
import operator
import numpy as np
from textrank4zh import TextRank4Keyword, TextRank4Sentence

keywords_file = open("d:/workspace/python-aqs/data/keywords.txt","r")
qa_dict = json.load(keywords_file)
questions = qa_dict['questions']
answers = qa_dict['answers']

def standardization(keydict):
	max_count = max(keydict.values())
	for word,count in keydict.items():
		keydict[word] = round(float(count)/max_count,4)

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

def getVector(words_idf,sentence_seg):
	v = []

	for word in words_idf:
		if word in sentence_seg:
			v.append(words_idf[word]*sentence_seg[word])
		else:
			v.append(0)

	return np.array(v)

def generateQuestionVectors(qa_list):
	# get the vector of all the questions
	# questions_vectors = []
	for qa in qa_list:
		question_seg = qa['question_seg']
		v = getVector(words_idf,question_seg)
		qa['question_vector'] = v
	# return questions_vectors

#init the textrank4keyword
tr4w = TextRank4Keyword()#allow_speech_tags=['r']


# print(questions)
# print(question_keywords)


keywords = {}
for d in questions:
	for word in d.keys():
		if word not in keywords:
			keywords[word] = 1;
		else:
			keywords[word] += 1;

words_idf = calcIDF(keywords)
ave_idf = sum(words_idf.values())/len(words_idf)

n_questions = []
for question in questions:
	v = []
	for word in words_idf:
		if word in question:
			v.append(words_idf[word]*question[word])
		else:
			v.append(0)
	n_questions.append(v)



#cal sim by the textrank weight
test_questions = open("d:/workspace/python-aqs/data/test_questions.txt","r").read().split('\n')
for test_question in test_questions:
	test_question = "书可以借多长时间，可以续借嘛？"
	tr4w.analyze(text=test_question, lower=True, window=2)
	question_keywords = {}
	for item in tr4w.get_keywords(4, word_min_len=1):  #get the key words
		question_keywords[item.word] = round(item.weight,4)
	v_question = []
	for word in words_idf:
		if word in question_keywords:
			v_question.append(words_idf[word]*question_keywords[word])
		else:
			v_question.append(0)
	res = []
	for qv in n_questions:
		# get the two vector of the sentence
		v1 = np.array(qv)
		v2 = np.array(v_question)
		l1 = math.sqrt(v1.dot(v1))
		l2 = math.sqrt(v2.dot(v2))
		temp = v1.dot(v2)/(l1*l2)
		res.append(temp)
	print(res)
	answer_index = res.index(max(res))
	# print(question_keywords)
	# print(questions)
	print(questions[answer_index])
	# print(answer_index)
	print(answers[answer_index])

