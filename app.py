from flask import Flask, render_template, request
from data import goals
import json
from random import randint
week_days = {"mon" : "Понедельник", "tue" : "Вторник", "wed" : "Среда",
      "thu" : "Четверг", "fri" : "Пятница", "sat" :"Суббота", "sun" : "Воскресение"}
week_days_reverse = dict((v, k) for k, v in week_days.items())

app = Flask(__name__)

@app.route("/")
def first():
  with open("teachers.json", "r") as f:
    data = json.load(f)
  maximum = len(data) - 1
  id_list = []
  if maximum <= 5:
    for i in range(maximum + 1):
       id_list.append(i)
  else:
    for i in range (6):
      while True:
        tmp = randint(0, maximum)
        if tmp not in id_list:
          id_list.append(tmp)
          break
        
  return render_template("index.html", form = data, goals = goals, id_list = id_list)

def dict_value(dictionary):
  return dictionary["rating"]

@app.route("/goals/<goal>/")
def goal(goal):
  needed = []
  with open("teachers.json", "r") as f:
    data = json.load(f)
    for i in data:
      if goal in i["goals"]:
        needed.append(i)
  needed.sort(reverse=True, key=dict_value)
  return render_template("goal.html", teachers = needed, goal = goals[goal])

@app.route("/profiles/")
def profile_all():
  with open("teachers.json", "r") as f:
    data = json.load(f)
  return render_template("all_profiles.html", form = data)

@app.route("/profiles/<id>/")
def profile(id):
  with open("teachers.json", "r") as f:
    data = json.load(f)
  try:
    id = int(id)
    # if id isnt int will go exception
    week = data[id]["free"]
    week_remade = dict()
    for i in week:
      week_remade[week_days[i]] = []
      for key, value in week[i].items():
        if value == True:
          week_remade[week_days[i]].append(key)
    return render_template("profile.html", form=data[id], week = week_remade, week_reverse = week_days_reverse, goals = goals)
  except:
    return "Wrong ID"
    
@app.route("/request/")
def request_func():
  return render_template("request.html", goals = goals)

@app.route("/request_done/", methods = ["POST"])
def request_done():
  print(request.form)
  data = {"name" : request.form["name"], "time":request.form["time"],
      "phone" : request.form["phone"]}
  if request.form["goal"] in goals:
    data["goal"] = goals[request.form["goal"]]
  else:
    data["goal"] = request.form["goal"]
    
  with open("request.json", "r+") as f:
    file = json.load(f)
    file.append(data)
    f.seek(0)
    json.dump(file, f)
    
  return render_template("request_done.html", form=data)

@app.route("/booking/<id>/<day>/<time>/")
def booking(id, day, time):
  try:
    with open("teachers.json", "r") as f:
      data = json.load(f)
    id = int(id)
    week_days[day]
    time = time.replace("_", ":")
    data = data[id]
    if data["free"][day][time] == False:
      return "Already booked"
  except:
    return "Wrong URL"
  return render_template("booking.html", form = data,
      date_time = week_days[day] + ", " + time, day = day, time = time)
  
@app.route("/booking_done", methods = ["POST"])
def booking_done():
  data = { "name" : request.form["clientName"], "phone" : request.form["clientPhone"]}
  date_time = week_days[request.form["clientWeekday"]] + ", " + request.form["clientTime"]
  
  with open("teachers.json", "r+") as f:
      main_data = json.load(f)
      if main_data[int(request.form["clientTeacher"])]["free"][request.form["clientWeekday"]][request.form["clientTime"]] == True:
        main_data[int(request.form["clientTeacher"])]["free"][request.form["clientWeekday"]][request.form["clientTime"]] = False
        f.seek(0)
        json.dump(main_data, f)
      else:
        return "Alredy booked"

  with open("booking.json", "r+") as f:
    booking = json.load(f)
    booking.append({"name" : request.form["clientName"],
      "phone" : request.form["clientPhone"],
      "day" : request.form["clientWeekday"],
      "time" : request.form["clientTime"],
      "teacher_id" : request.form["clientTeacher"]})
    f.seek(0)
    json.dump(booking, f)

  return render_template("booking_done.html", form = data, time = date_time)

if __name__ == "__main__":
	app.run(debug=False)