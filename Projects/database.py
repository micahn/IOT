import datetime
import json

entries = []

running = True


print("Database Engine v0.0.1")

try:
    file = open("database.txt", "r")
    entries = json.load(file)
    file.close()
except FileNotFoundError:
    print("No file found")

while running:
    choice = input("add entry? (Y/N)").upper()

    if choice == "Y":
        name = input("Application name:")
        comment = input("Comment:")
        time = str(datetime.datetime.now().strftime("%d%m%y"))
        entry = (name, comment, time)
        entries.append(entry)
    elif choice == "N":
        running = False
 
file = open("database.txt", "w")
json.dump(entries, file)

file.close()

for entry in entries:
    print("Application name: %s, Comment: %s, Timestamp: %s" % [*entry] )




