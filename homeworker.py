from Tkinter import *
import datetime
import webbrowser


f = open("log.txt", "r+")
data = f.read().strip().split('\n\n')

for i in range(len(data)):
	data[i] += '\n'

allDays = [0,1,2,3,4,5,6]


class My_Entry:
	def __init__(self, task, text, time, link, parent):
		self.task = task
		self.completed = BooleanVar()
		self.text = text
		self.time = time
		self.link = link
		self.parent = parent
		self.entryRow = parent.newEntryRow

		#make check button if task
		if task != 0:
			self.cb = Checkbutton(variable = self.completed, command = self.check)
			if task == 2:
				self.cb.select()
			self.cb.grid(row = self.entryRow, column = 0)

		#print text
		self.lbl = Label(text = text)
		self.lbl.grid(row = self.entryRow, column = 1)

		#print time
		if not time == "None":
			self.timelbl = Label(text = time)
			self.timelbl.grid(row = self.entryRow, column = 2)

		#make openable
		if not link == "None":
			self.open = Button(text = "Open", command = lambda: self.openLink(link))
			self.open.grid(row = self.entryRow, column = 3)
			if not link in data[0]:
				data[0] = data[0].strip() + '\n' + link

		self.deleteBut = Button(text = "-", command = self.delete)
		self.deleteBut.grid(row = self.entryRow, column = 4)

	def openLink(self,link):
		webbrowser.open(link)

	def check(self):
		if self.completed.get():
			self.task = 2
			print "done!"
		else:
			self.task = 1
			print "not completed"

	def delete(self):
		if self.task != 0:
			self.cb.grid_remove()
		self.lbl.grid_remove()
		if self.time != "None":
			self.timelbl.grid_remove()
		if self.link != "None":
			self.open.grid_remove()
		self.deleteBut.grid_remove()
		self.parent.entries.remove(self)
		self.parent.newEntryRow-=1



class Day:
	def __init__(self,date):
		self.date = date
		day = date.weekday()
		self.newEntryRow = 8 * day + 2
		self.entries = []

		self.addButton = Button(text = "+", command = self.addEntry)
		self.addButton.grid(row = self.newEntryRow-1, column = 1)

		for day in data:
			if str(date) in day:
				self.data = day
				data.remove(day)
				break
		else:
			self.data = str(date) + '\n'

		ents = self.data.strip().split('\n')
		del ents[0]
		for ent in ents:
			elements = ent.split('\t')
			task = int(elements[0])
			text = elements[1]
			time = elements[2]
			link = elements[3]
			self.entries.append(My_Entry(task = task, text = text, time = time, link = link, parent = self))
			self.newEntryRow+=1

	def save(self):
		if len(self.entries) > 0:
			string = str(self.date) + '\n'
			for ent in self.entries:
				string += "%i\t%s\t%s\t%s\n" %(ent.task,ent.text,ent.time,ent.link)
			data.append(string)

	def addEntry(self):
		t = Toplevel()
		t.wm_title(self.date.strftime("%d %A"))

		self.tcbVar = BooleanVar()
		self.newTask = 0
		Checkbutton(t, text = "Task?", variable = self.tcbVar, command = self.make_task).pack()
		
		Label(t, text = "Description:").pack()
		self.newText = StringVar()
		Entry(t, textvariable = self.newText).pack()
		
		Label(t, text = "Deadline:").pack()
		self.newTime = StringVar()
		Entry(t, text = "Deadline:", textvariable = self.newTime).pack()

		Label(t, text = "Link:").pack()
		self.newLink = StringVar()
		self.linkEntry = Entry(t, textvariable = self.newLink)
		self.linkEntry.pack()

		links = data[0].split('\n')
		self.lb = Listbox(t)
		for i in range(1,len(links)):
			self.lb.insert(END, links[i])
		self.lb.bind("<<ListboxSelect>>", self.on_select)    
		self.lb.pack()

		Button(t, text = "Create Entry", command = lambda: self.commitEntry(t)).pack()

	def make_task(self):
		if self.tcbVar:
			self.newTask = 1
		else:
			self.newTask = 0

	def on_select(self, val):
		sender = val.widget
		i = sender.curselection()
		self.linkEntry.delete(0,END)
		self.linkEntry.insert(END, sender.get(i))

	def commitEntry(self,toplevel):
		if self.newText.get() == "":
			return
		if self.newTime.get() == "":
			self.newTime.set("None")
		if self.newLink.get() == "":
			self.newLink.set("None")
		entry = My_Entry(int(self.newTask), self.newText.get(), self.newTime.get(), self.newLink.get(), self)
		self.entries.append(entry)
		self.newEntryRow+=1
		toplevel.destroy()



class Homeworker(Frame):

	def __init__(self,parent):
		Frame.__init__(self,parent)
		self.parent = parent
		self.initUI()

	def initUI(self):
		self.parent.title("Ryan's Planner")
		self.date = datetime.date.today()

		#todays date at top
		header = Label(text = self.date.strftime("%a, %b %d"))
		header.config(font = ("Arial,20"))
		header.grid()

		#get days this week
		day = self.date.weekday()
		self.strvars = []
		for i in range(7):
			newDay = self.date + datetime.timedelta(days = i-day)
			dayInst = Day(newDay)
			allDays[i] = dayInst
			strvar = StringVar()
			strvar.set(newDay.strftime("%d %A"))
			self.strvars.append(strvar)
			Label(textvariable = self.strvars[i]).grid(row = 8*i+1)

		menu = Menu(self.parent, tearoff = 0)
		menu.add_command(label = "Save", command = self.save)
		menu.add_command(label = "<--", command = lambda: self.jumpWeeks(-1))
		menu.add_command(label = "-->", command = lambda: self.jumpWeeks(1))
		self.parent.config(menu = menu)

	def save(self):
		for day in allDays:
			day.save()

		data[0] = data[0].rstrip() + '\n'

		f.seek(0)
		f.write('\n'.join(data))
		f.truncate()

		#takes additions out of data
		for i in range(7):
			while len(allDays[i].entries) > 0:
				allDays[i].entries[0].delete()
			allDays[i] = Day(allDays[i].date)

	def jumpWeeks(self,num):
		for i in range(7):
			allDays[i].save()
			while len(allDays[i].entries) > 0:
				allDays[i].entries[0].delete()
			newDate = allDays[i].date + datetime.timedelta(weeks = num)
			allDays[i] = Day(newDate)
			self.strvars[i].set(newDate.strftime("%d %A"))


root = Tk()
root.geometry("500x300+100+100")
Homeworker(root)
root.mainloop()

