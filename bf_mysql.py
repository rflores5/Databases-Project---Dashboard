import mysql.connector
from mysql.connector import errorcode
import random

class MySqlClass:

	def __init__(self):
		self.cnx = mysql.connector.Connect(user='root',password='test_root',host='localhost',port='3306',database='academicworld',auth_plugin='mysql_native_password')
		self.cursor = self.cnx.cursor(prepared=True)
		
	def close(self):
		self.cursor.close()
		self.cnx.close()
		
	def commit(self):
		return self.cnx.commit()

	def getKeywordList(self):
		query = ("SELECT id, name FROM keyword")
		self.cursor.execute(query)
		return self.cursor.fetchall()
		
	def getFacultyList(self):
		query = ("SELECT id, name FROM faculty")
		self.cursor.execute(query)
		return self.cursor.fetchall()
	
	def getUniveristyList(self):
		query = ("SELECT id, name FROM university")
		self.cursor.execute(query)
		return self.cursor.fetchall()
	
	def findFaculty_id(self, id):
		query = ("SELECT * FROM faculty WHERE id = %s")
		self.cursor.execute(query, (id,))
		return self.cursor.fetchall()
	
	def findFaculty_name(self, name):	
		query = ("SELECT * FROM faculty WHERE name like '%" + name+ "%'")
		self.cursor.execute(query)
		return self.cursor.fetchall()
	
	def getMaxId(self):
		query = ("SELECT MAX(id) as id FROM faculty")
		self.cursor.execute(query)
		id = self.cursor.fetchone()[0]
		return id
	
	def findRandomFaculty(self):
		max_id = self.getMaxId()
		rand_id = random.randint(0, max_id)
		query = ("SELECT * FROM faculty WHERE id = %s")
		self.cursor.execute(query, (rand_id,))
		return self.cursor.fetchall()
		
	def addFaculty(self,name, position, research_interest, email, phone, photo_url, university_id):
		id_ = self.getMaxId() + 1
		print(name, position, research_interest, email, phone, photo_url, university_id)
		insert = ("INSERT INTO faculty (id, name, position, research_interest, email, phone, photo_url, university_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")
		self.cursor.execute(insert, (id_,name,position,research_interest,email,phone,photo_url,university_id))
		self.cnx.commit()
		return self.cursor.statement

if __name__ == "__main__":
	myclass = MySqlClass()


