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
import webbrowser

try:
	f = open('planner.txt','r+')
	rawData = f.read().strip()
	entries = rawData.split('\n')
	print "Hello, %s\n" %entries[0]
except:
	f = open('planner.txt','w+')
	print "Hello! What's your name?"
	rawData = raw_input();

while True:
	command = raw_input(">> ")


