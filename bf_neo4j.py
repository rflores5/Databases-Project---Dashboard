from neo4j import GraphDatabase

class Neo4jClass:

	def __init__(self):
		self.driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "password"))
		self.session = self.driver.session(database='academicworld')

	def close(self):
		self.driver.close()
		
	def print_results(self, result):
		for line in result:
			print(line)

	def query_institute(self, name):
		result = self.session.read_transaction(self._find_and_return_uni, name)
		print(result.data()['i'])
		
	def top_keywords(self, year):
		result = self.session.read_transaction(self._find_top_keywords, year)
		return result
	
	def top_professors_publications(self, year):
		result = self.session.read_transaction(self._find_top_professors_publications, year)
		return result
		
	def top_professors_citations(self, year):
		result = self.session.read_transaction(self._find_top_professors_citations, year)
		return result

	def top_university_publications(self, year):
		result = self.session.read_transaction(self._find_top_university_publications, year)
		return result
	
	def top_university_citations(self, year):
		result = self.session.read_transaction(self._find_top_university_citations, year)
		return result
		
	def faculty_publications(self, id):
		result = self.session.read_transaction(self._find_faculty_publications, id)
		return result
		
	def publications_citations(self):
		result = self.session.read_transaction(self._find_publications_citations)
		return result
		
	def update_publication_name(self, old_title, new_title):
		result = self.session.write_transaction(self._update_publication_name, old_title, new_title)
		return result
		
	@staticmethod
	def _find_and_return_uni(tx, name):
		query = ("MATCH (i:INSTITUTE) WHERE i.name = $name RETURN *")
		result = tx.run(query, name=name)
		return result.single()	
		
	@staticmethod
	def _find_top_keywords(tx, year):
		query = ("MATCH (p:PUBLICATION {year: $year})-[r:LABEL_BY]-(k:KEYWORD) RETURN k.name as keyword, COUNT(DISTINCT p.id) as count ORDER BY count desc limit 10")
		result = tx.run(query,year=year)
		return result.data()
		
	@staticmethod
	def _find_top_professors_publications(tx, year):
		query = ("MATCH (i:INSTITUTE)-[r1:AFFILIATION_WITH]-(f:FACULTY) -[r:PUBLISH]-(p:PUBLICATION {year:$year}) Return f.name as Name,i.name as University, COUNT(DISTINCT p.id) as Publications order by Publications desc limit 5")
		result = tx.run(query,year=year)
		return result.data()
		
	@staticmethod
	def _find_top_professors_citations(tx, year):
		query = ("MATCH (i:INSTITUTE)-[r1:AFFILIATION_WITH]-(f:FACULTY) -[r:PUBLISH]-(p:PUBLICATION {year:$year}) Return f.name as Name,i.name as University, Sum(p.numCitations) as Citations order by Citations desc limit 5")
		result = tx.run(query,year=year)
		return result.data()
		
	@staticmethod
	def _find_top_university_publications(tx, year):
		query = ("MATCH (i:INSTITUTE)-[r1:AFFILIATION_WITH]-(f:FACULTY) -[r:PUBLISH]-(p:PUBLICATION {year:$year}) Return i.name as Name,i.photoUrl as photoUrl, COUNT(DISTINCT p.id) as Publications order by Publications desc limit 5")
		result = tx.run(query, year=year)
		return result.data()
	
	@staticmethod
	def _find_top_university_citations(tx, year):
		query = ("MATCH (i:INSTITUTE)-[r1:AFFILIATION_WITH]-(f:FACULTY) -[r:PUBLISH]-(p:PUBLICATION {year:$year}) Return i.name as Name,i.photoUrl as photoUrl, SUM(p.numCitations) as Citations order by Citations desc limit 5")
		result = tx.run(query, year=year)
		return result.data()
		
	@staticmethod
	def _find_faculty_publications(tx, id):
		query = ("MATCH (f:FACULTY {id:$id})-[r:PUBLISH]-(p:PUBLICATION) Return p.title as title, p.year as year order by p.year desc")
		f_id = "f"+str(id)
		result = tx.run(query, id=f_id)
		return result.data()
		
	@staticmethod
	def _find_publications_citations(tx):
		query = ("MATCH (p:PUBLICATION) WITH p.year as year, MAX(p.numCitations) as cite MATCH (p2:PUBLICATION) WHERE year = p2.year and p2.numCitations = cite RETURN p2.year as year, p2.title as title, p2.numCitations as citations ORDER BY p2.year desc LIMIT 50")
		result = tx.run(query)
		return result.data()
		
	@staticmethod
	def _update_publication_name(tx, old_title, new_title):
		query = ("MATCH (p:PUBLICATION {title: $old_title}) SET p.title = $new_title RETURN p")
		result = tx.run(query, old_title=old_title, new_title=new_title)
		return result.data()
	
if __name__ == "__main__":
	greeter = Neo4jClass()
