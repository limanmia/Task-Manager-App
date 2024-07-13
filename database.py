import sqlite3

class Database():
	def __init__(self):
		self.con = sqlite3.connect("task-database.db")
		self.cursor = self.con.cursor()
		self.create_task_table()


	#Creating task table
	def create_task_table(self):
		self.cursor.execute("CREATE TABLE IF NOT EXISTS tasks(id integer PRIMARY KEY AUTOINCREMENT, task varchar(50) NOT NULL, due_date varchar(50), completed BOOLEAN NOT NULL CHECK (completed IN (0,1)))")
		self.con.commit()

	#Creating the task
	def create_task(self, task, due_date=None):
		self.cursor.execute("INSERT INTO tasks(task, due_date, completed) VALUES(?,?,?)", (task, due_date, 0))
		self.con.commit()

		#Getting the last entered item so we can add it to the task list
		created_task = self.cursor.execute("SELECT id, task, due_date FROM tasks WHERE task = ? and completed = 0", (task,)).fetchall()
		return created_task[-1]

	#Getting the task
	def get_tasks(self):
		#Getting all tasks: compleate and incomplete
		incompleted_task = self.cursor.execute("SELECT id, task, due_date FROM tasks WHERE completed = 0").fetchall()
		completed_task = self.cursor.execute("SELECT id, task, due_date FROM tasks WHERE completed = 1").fetchall()
		return completed_task, incompleted_task

	#Updating the task
	def mark_task_as_completed(self, taskid):
		#Mark task as the completed
		self.cursor.execute("UPDATE tasks SET completed = 1 WHERE id = ?", (taskid,))
		self.con.commit()

	def mark_task_as_incompleted(self, taskid):
		#Mark task as the completed
		self.cursor.execute("UPDATE tasks SET completed = 0 WHERE id = ?", (taskid,))
		self.con.commit()

		#return the task text
		task_text = self.cursor.execute("SELECT task FROM tasks WHERE id = ?", (taskid,)).fetchall()
		return task_text[0][0]

	#Deleting the task
	def delete_task(self, taskid):
		self.cursor.execute("DELETE FROM tasks WHERE id = ?", (taskid,))
		self.con.commit()

	#Close the database connection
	def close_db_connection(self):
		self.con.close()
