from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.pickers import MDDatePicker
from datetime import datetime
from kivymd.uix.list import TwoLineAvatarIconListItem , ILeftBody
from kivymd.uix.selectioncontrol import MDCheckbox

#Importing the Database class and created the object
from database import Database
db = Database()


class DialogContent(MDBoxLayout):
	#The init fuction for class contructor
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.ids.date_text.text = datetime.now().strftime("%A %d %B %Y")


	#This fuction will show the date picker
	def show_date_picker(self):
		date_dialog = MDDatePicker()
		date_dialog.bind(on_save = self.on_save)
		date_dialog.open()

	#This fuction will get the date and save in a friendly form
	def on_save(self, instance, value, date_range):
		date = value.strftime("%A %d %B %Y")
		self.ids.date_text.text = str(date)


#Class for marking and deleting the list item	
class ListItemCheckbox(TwoLineAvatarIconListItem):
	"""docstring for ClassName"""
	def __init__(self, pk=None, **kwargs):
		super().__init__(**kwargs)
		self.pk = pk

	#Marking the item as complete or incomplete
	def mark(self, check, the_list_item):
		if check.active == True:
			the_list_item.text = '[s]' + the_list_item.text + '[/s]'
			db.mark_task_as_completed(the_list_item.pk)
		else:
			the_list_item.text = str(db.mark_task_as_incompleted(the_list_item.pk))

	#Deleting The List Item
	def delete_item(self, the_list_item):
		self.parent.remove_widget(the_list_item)
		db.delete_task(the_list_item.pk)

		

class LeftCheckbox(ILeftBody, MDCheckbox):
	pass
		




#aThis is a main class and function
class MainApp(MDApp):
	def build(self):
		self.theme_cls.primary_palette ="Teal"
		self.theme_cls.theme_style ="Light"
		self.title = 'Task Manager'

		self.task_list_dialog = None

	#This is the create show task fuction
	def show_task_fuction(self):
		#if not self.task_list_dialog:
		self.task_list_dialog = MDDialog(
			title = "Create Task",
			type = "custom",
			content_cls = DialogContent()

		)

		self.task_list_dialog.open()

	#Adding Tasks
	def add_task(self, task, task_date):
		created_task = db.create_task(task.text, task_date)
		self.root.ids['container'].add_widget(ListItemCheckbox(pk = created_task[0], text = '[b]' + created_task[1] + '[/b]', secondary_text = created_task[2]))
		task.text = ''



	def close_dialog(self, *args):
		self.task_list_dialog.dismiss()



	def on_start(self):
		#This is to load the saved task and add them to the MDList widget
		completed_task, incompleted_task = db.get_tasks()

		if incompleted_task != []:
			for task in incompleted_task:
				add_task = ListItemCheckbox(pk=task[0], text=task[1], secondary_text=task[2])
				self.root.ids.container.add_widget(add_task)

		if completed_task != []:
			for task in completed_task:
				add_task = ListItemCheckbox(pk=task[0], text= "[s]" + task[1] + "[/s]", secondary_text=task[2])
				add_task.ids.check.active = True
				self.root.ids.container.add_widget(add_task)




if __name__ == "__main__":
	app = MainApp()
	app.run()