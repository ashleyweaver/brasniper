import praw
import re
from pymongo import MongoClient
import os
from secrets import MONGO_USER, MONGO_PASS, MONGO_URL, MONGO_PORT


client = MongoClient(MONGO_URL, MONGO_PORT)
client.BraSniper.authenticate(MONGO_USER, MONGO_PASS)
db = client.BraSniper

r = praw.Reddit(user_agent='brasniper')


def findMatches(sizes):
	submissions = r.get_subreddit('braswap').get_new(limit=10)
	links = []
	for post in submissions:
		title = vars(post)['title']
		delimiters = " ", "/", ",", ".", "(", ")", "[", "]"
	 	regexPattern = '|'.join(map(re.escape, delimiters))
		words = re.split(regexPattern, title)
		#print title
		for bra in sizes:
			if bra in words:
				links.append(vars(post)['url'])
	return links

	#print [str(x) for x in submissions]

def matchAll():
	for user in db.users.find():
		matches = findMatches(user['sizes'])
		sentList = user['sent']
		for link in matches:
			if link not in user['sent']:
				sentList.append(link)
			else:
				matches.remove(link)
		print matches
		#TODO email str(matches)
		db.users.update({'_id': user['_id']}, {'$set': {'sent': sentList}})

matchAll()
#print findMatches({"30G", "34G"})

# def convert(size):
# 	'''converts EU to UK'''
# 	band = getBand(size)
# 	cup = getCup(size)

# 	if (band >= 55):
# 		band = {
# 			55: 26,
# 			60: 28,
# 			65: 30,
# 			70: 32,
# 			75: 34,
# 			80: 36,
# 			85: 38,
# 			90: 40,
# 			95: 42,
# 			100: 44,
# 			105: 46
# 		}[band]

def getBand(size):
	return int(re.match(r'\d+', size).group())

def getCup(size):
	band = int(re.match(r'\d+', size).group())
	return size[len(band):]