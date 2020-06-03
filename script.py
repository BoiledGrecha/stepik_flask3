import data
import json
import os

if os.path.isfile("teachers.json"):
  with open("teachers.json", "w")  as f:
    json.dump(data.teachers, f)
    print("Done")
else:
  print("File dont exist")