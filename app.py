from flask import Flask, render_template, request
from data import goals
import json
#from flask_debugtoolbar import DebugToolbarExtension
week_days = {"mon" : "Понедельник", "tue" : "Вторник", "wed" : "Среда",
      "thu" : "Четверг", "fri" : "Пятница", "sat" :"Суббота", "sun" : "Воскресение"}
week_days_reverse = dict((v, k) for k, v in week_days.items())

app = Flask(__name__)
#app.debug = True

#app.config["SECRET_KEY"] = "super_secret_key"
#toolbar = DebugToolbarExtension(app)

@app.route("/")
def first():
	return render_template("index.html")

@app.route("/goals/<goal>/")
def goal(goal):
  return render_template("goal.html")

@app.route("/profiles/")
def profile_all():
  return "Work"

@app.route("/profiles/<id>/")
def profile(id):
    with open("teachers.json", "r") as f:
      data = json.load(f)
  #try:
    id = int(id)
    # if id isnt int will go exception
    week = data[id]["free"]
    week_remade = dict()
    for i in week:
      week_remade[week_days[i]] = []
      for key, value in week[i].items():
        if value == True:
          week_remade[week_days[i]].append(key)
    #print(week_remade)
    return render_template("profile.html", form=data[id], week = week_remade, week_reverse = week_days_reverse)
  #except:
  #  return "Wrong ID"
    
@app.route("/request/")
def request_func():
  pass

@app.route("/request_done/")
def request_done():
  pass

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
      #maybe add special error page with redirection
      return "Already booked"
  except:
    return "Wrong URL"
  return render_template("booking.html", form = data,
      date_time = week_days[day] + ", " + time, day = day, time = time)
  
@app.route("/booking_done", methods = ["POST"])
def booking_done():

  return render_template("booking_done.html")


# if __name__ == "__main__":
# 	app.run(host = "185.162.131.72", port=82)

if __name__ == "__main__":
	app.run(debug=True)