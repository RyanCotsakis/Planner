"""

Commands:
week
done (#)
add (event, task) [prompt when](weekday) (time) [then it prompts for message]
(weekday)
today
sort (date, priority)
edit (#)
remove (#)
tomorrow
time
next (task, event)


"""

#IMPORTS
import datetime

BAD_COMMAND = "Invalid command: "
try:
	f = open('planner.txt','r+')
	rawData = f.read().strip()
	entries = rawData.split('\n')
	print "Hello, %s!" %entries[0]
except:
	f = open('planner.txt','w+')
	print "Hello! What's your name?"
	rawData = raw_input()
	f.write(rawData)

while True:
	command = raw_input("\n>> ")

	if command == "exit":
		break

	elif "add" in command:
		if command == "add event":
			typ = "event"
		elif command == "add task":
			typ = "task"
		elif command == "add":
			typ = raw_input("'task' or 'event'?\n")
		else:
			print BAD_COMMAND + command
			typ = ""

		if typ == "event" or typ == "task":
			timeString = raw_input("When?\n")
			"next Monday"
			"Aug 23 23:59"
			"monday"
			"august 23"
			"monday 23:59"
			"today"
			"tomorrow"
			#determine datetime object from this string

			description = raw_input("What's the occasion?\n")

			#from typ, time, and description, add something
			entries.append(typ + '\t' + timeString + '\t' + description)
			f.seek(0)
			f.write('\n'.join(entries))
			f.truncate()
		elif typ != "":
			print BAD_COMMAND + "add " + typ

	else:
		print BAD_COMMAND + command

			




