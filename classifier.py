#-*- encoding:utf-8 -*-

import os
import json
import numpy as np
import time


def normalize(l1):
	return [round(x/(sum(l1)+0.0001), 4) for x in l1]

def calWordCoOccurrence(word1, word2, IIndexs):
	if word1 in IIndexs and word2 in IIndexs:
		ids1 = set(IIndexs[word1]['ids'])
		ids2 = set(IIndexs[word2]['ids'])
	else:
		return 0

	try:
		intersection = ids1 & ids2
		union = ids1 | ids2
		return len(intersection)/len(union)
	except Exception as e:
		return 0

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

	if len(words_set1) == 0 or len(words_set2) == 0:
		return 0
	v1 = generateVector(set1,words_set1|words_set2)
	v2 = generateVector(set2,words_set1|words_set2)
	cos = round(calCOS(v1,v2),4)
	# print('finish calculating the sim!')

	# print('begin to  cal the word co-occur!')
	wsum = 0
	for word1 in words_set1:
		templ = [0,]
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
			

def HierarchicalClustering(question_list, IIndexs, classes):
	
	# t1 = time.time()
	while True:
		max_sim = (0,0,0)
		t1 = time.time()
		print("begin to find the most similar sentence!")
		templ1 = [(k,v) for k, v in classes.items()]
		length = max(classes.keys())+1
		simmatrix = -np.ones((length, length))
		for key1, qidclass1 in templ1:
			submax = 0
			for key2, qidclass2 in classes.items():
				if key1 != key2:
					if simmatrix[key1][key2] == -1:
						qlist2 = []
						qlist1 = []
						for qid in qidclass1:
							qlist1.append(question_list[qid])
						for qid in qidclass2:
							qlist2.append(question_list[qid])
						sim = calSim(qlist1, qlist2, IIndexs)
						simmatrix[key1][key2] = sim
					else:
						sim = simmatrix[key1][key2]
					if submax < sim:
						submax = sim
					if max_sim[2] < sim:
						# (classid1,classid2, similarity)
						max_sim = (key1, key2, sim)
			if submax < LowerBound:
				# print(key)
				# print(submax)
				del classes[key1]
			
			# t2 = time.time()
			# print("program has cost %s s" % (t2-t1))
		t2 = time.time()
		print('finish finding the most similar sentence! cost %s seconds' % round(t2-t1,4))
		if max_sim[2] < THRESHOLD:
			# result_list.append(question_list[i])
			return classes
		else:
			try:
				newlist = classes[max_sim[0]].union(classes[max_sim[1]])
				del classes[max_sim[0]]
				del classes[max_sim[1]]
				classes[max_sim[0]] = newlist
			except KeyError as e:
				print(max_sim)
				print(classes.keys())
				exit()
			

def initList(questions):
	question_list = {}
	classes = {}
	for i in range(0,len(questions)):
		question_list[questions[i]['id']] = questions[i]
		classes[questions[i]['id']] = {questions[i]['id'],}
	return (question_list, classes)

print('open the inverted index file of answer keywords')
root = "D:/workspace/python-aqs"
filedir = os.path.abspath(root+"/data/IIndex_keywords.json")
jsonfile = open(filedir,"r")
IIndexs = json.load(jsonfile)

print('open the file of the questions segs')
filedir = os.path.abspath(root+"/data/questions-seg.json")
jsonfile = open(filedir,"r")
questions = json.load(jsonfile)

THRESHOLD = 0.56
LowerBound = 0.3
ALPHA = 0.8

t1 = time.time()
print('init the origin class')
(question_list, classes) = initList(questions[:100])

print('begin to cluster!')
classes = HierarchicalClustering(question_list, IIndexs, classes)

print('finish clustering!')
print('write the result to the file!')
filedir = os.path.abspath(root+"/data/class_res.txt")
resfile = open(filedir,"w")
for key, qclass in classes.items():
	json.dump({key:list(qclass)}, resfile)
	resfile.write('\r\n')
t2 = time.time()
print('programm over! cost %s hours' % round((t2-t1)/3600,1))
		# print(max_sim)
		# print(question_list[i])
		# print(question_list[i+1+max_index])
		# exit()