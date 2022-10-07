import pymongo
from pymongo import MongoClient

class MongodbClass:

	def __init__(self):
		self.client = MongoClient("mongodb://127.0.0.1:27017")
		self.db = self.client['academicworld']
		self.faculty = self.db['faculty']
		self.publications = self.db['publications']

	def close(self):
		self.client.close()

	def one_faculty(self):
		return self.faculty.find_one()
		
	def one_publication(self):
		return self.publications.find_one()
		
		
	def keyword_mentions(self, keyword_):
		pipeline = [{"$unwind": "$keywords"},{"$match": {"keywords.name": keyword_}},{"$group": {"_id":"$year", "count": {"$sum":1}}},{"$sort": {"_id": -1}},{"$limit": 30}]
		result = self.publications.aggregate(pipeline)
		return list(result)
		
	def top_keywords(self, year_):
		pipeline = [{"$unwind": "$keywords"},{"$match": {"year": year_}},{"$group": {"_id":"$keywords.name", "count": {"$sum":1}}},{"$sort": {"count": -1}},{"$limit": 10}]
		result = self.publications.aggregate(pipeline)
		return list(result)
		
	def top_publications(self, year_):
		pipeline = [{"$match": {"year": year_}},{"$project": {"_id": 0, "title": 1, "numCitations": 1}},{"$sort": {"numCitations": -1}},{"$limit": 10}]
		result = self.publications.aggregate(pipeline)
		return list(result)

	def update_publication_name(self, old_title, new_title):
		query = { "title": old_title}
		newvalue = { "$set": { "title": new_title}}
		result = self.publications.update_one(query,newvalue)
		return result
		
		
if __name__ == "__main__":
	mongo = MongodbClass()
	