# -*- encoding:utf8 -*-

import json
import os
from operator import itemgetter, attrgetter
import math
import time

a = [1,2,3,4,5]
for i in range(0,len(a)):
	a.pop()
	print(i)




# while True:
# 	try:
# 		(n, m) = (int(x) for x in input().split())
# 		ndivisors = []
# 		for i in range(1,n+1):
# 			if n%i == 0:
# 				ndivisors.append(i)
# 		mdivisors = []
# 		for i in range(1,m+1):
# 			if m%i == 0:
# 				mdivisors.append(i)
# 		count = len([x for x in ndivisors if x in mdivisors])
# 		print(len(ndivisors)*len(mdivisors))
# 		print(count)
# 	except EOFError:
# 		break
# filedir = os.path.abspath("./data/test.txt")
# faqfile = open(filedir,"r",encoding="utf8")

# qa = []
# res = []
# line = faqfile.readline()

# while line:
# 	line.replace('\xa0',' ')
# 	if len(line.strip()) >= 1:
# 		qa.append(line)
# 	else:
# 		res.append({'question':qa[0], 'answer':''.join(qa[1::])})
# 		qa.clear()
# 	line = faqfile.readline()

# resfile = open(os.path.abspath('./data/faq_new.json'),'w',encoding='utf8')
# json.dump(res,resfile)
# print(res)
# res = []
# i = 1
# for question_json in questions_jsons:
# 	if len(question_json) >= 1:
# 		tempd = json.loads(question_json)
# 		try:
# 			tempd['answer'] = tempd['answer'].replace('\xa0',' ')
# 			l1 = tempd['answer'].split(',')
# 			del l1[0]
# 			del l1[0]
# 			if len(l1) > 1:
# 				l1.pop()
# 				l1.pop()
# 				for k in range(0,len(l1)):
# 					l1[k] = l1[k].strip()
# 				tempd['answer'] = '\n'.join(l1)
# 				tempd['question'] = tempd['question'].strip()
# 				tempd['id'] = i
# 				i += 1
# 				res.append(tempd)
# 		except KeyError as e:
# 			print(tempd)
# 			continue