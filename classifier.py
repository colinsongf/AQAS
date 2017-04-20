#-*- encoding:utf-8 -*-

import os
import json
import numpy as np
import time


def normalize(l1):
	return [round(x/(sum(l1)+0.0001), 4) for x in l1]

def calWordCoOccurrence(word1, word2, IIndexs):
	if word1 in IIndexs:
		ids1 = set(IIndexs[word1]['ids'])
	else:
		ids1 = set()
	if word2 in IIndexs:
		ids2 = set(IIndexs[word2]['ids'])
	else:
		ids2 = set()
		
	
	intersection = ids1 & ids2
	union = ids1 | ids2
	return len(intersection)/(len(union)+0.0001)

def generateVector(question_list, words_set):
	vector = {}
	#init the vector
	for word in words_set:
		vector[word] = 0
	#cal the vector
	for question in question_list:
		for word,count in question['answer_keywords'].items():
			vector[word] += count

	return np.array(normalize(vector.values()))

def calEuclideanDistance(v1, v2):
	return np.sqrt(sum((v1-v2)**2))

def calCOS(v1,v2):
	l1 = np.sqrt(v1.dot(v1))
	l2 = np.sqrt(v2.dot(v2))
	cos = v1.dot(v2)/(l1*l2)

	return cos

def calSim(set1,set2,IIndexs):
	words_set1 = set()
	words_set2 = set()
	# print('begin to calculate the cos sim!')
	for question in set1:
		words_set1 |= set(question['answer_keywords'])
	for question in set2:
		words_set2 |= set(question['answer_keywords'])

	v1 = generateVector(set1,words_set1|words_set2)
	v2 = generateVector(set2,words_set1|words_set2)
	cos = round(calCOS(v1,v2),4)
	# print('finish calculating the sim!')

	# print('begin to  cal the word co-occur!')
	wsum = 0
	for word1 in words_set1:
		templ = []
		for word2 in words_set2:
			templ.append(round(calWordCoOccurrence(word1, word2, IIndexs),4))
		wsum += max(templ)
	
	return ALPHA*cos+(1-ALPHA)*(wsum/len(words_set1))

# def findMaxSim(sim_list):
# 	max_sim = (0,0,0)
# 	for t in sim_list:
# 		if max_sim[2] < t[2]:
# 			max_sim = t
# 	return max_sim
			

def HierarchicalClustering(question_list, IIndexs):
	
	# t1 = time.time()
	while True:
		max_sim = (0,0,0)
		print("begin to find the most similar sentence!")
		templ1 = [(k,v) for k, v in question_list.items()]
		for key, qlist in templ1:
			submax = 0
			for key2, qlist2 in question_list.items():
				if key != key2:
					sim = calSim(qlist, qlist2, IIndexs)
					if submax < sim:
						submax = sim
					if max_sim[2] < sim:
						# (classid1,classid2, similarity)
						max_sim = (key, key2, sim)
			if submax < LowerBound:
				# print(key)
				# print(submax)
				del question_list[key]
			
			# t2 = time.time()
			# print("program has cost %s s" % (t2-t1))
		print('finish finding the most similar sentence!')
		if max_sim[2] < THRESHOLD:
			# result_list.append(question_list[i])
			return question_list
		else:
			try:
				newlist = question_list[max_sim[0]]+question_list[max_sim[1]]
				del question_list[max_sim[0]]
				del question_list[max_sim[1]]
				question_list[max_sim[0]] = newlist
			except KeyError as e:
				print(max_sim)
				print(question_list.keys())
				exit()
			

def initList(questions):
	question_list = {}
	for i in range(0,len(questions)):
		question_list[i] = [questions[i],]
	return question_list


filedir = os.path.abspath("./data/IIndex_keywords.json")
jsonfile = open(filedir,"r")
IIndexs = json.load(jsonfile)

filedir = os.path.abspath("./data/questions-seg.json")
jsonfile = open(filedir,"r")
questions = json.load(jsonfile)

filedir = os.path.abspath("./data/log")
logfile = open(filedir,"w",encoding='utf8')

THRESHOLD = 0.6
LowerBound = 0.3
ALPHA = 0.5

question_list = initList(questions[:100])

print('begin to cluster!')
HierarchicalClustering(question_list,IIndexs)
filedir = os.path.abspath("./data/class_res.txt")
resfile = open(filedir,"w")
for qclass in question_list.values():
	for question in qclass:
		resfile.write(question['question']+'\r\n\r\n')
	resfile.write('---------------------------\r\n')
		
		# print(max_sim)
		# print(question_list[i])
		# print(question_list[i+1+max_index])
		# exit()