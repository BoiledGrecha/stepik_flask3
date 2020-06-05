import json

with open("teachers.json", "r+") as f:
    file = json.load(f)
    for i in [8,9,10,11]:
      if "programming" not in file[i]["goals"]:
        file[i]["goals"].append("programming")
        
    f.seek(0)
    json.dump(file, f)