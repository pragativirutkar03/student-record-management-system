from flask import Flask, render_template, request, jsonify
app=Flask(__name__)
students=[
 {"roll":101,"name":"Aarav Sharma","branch":"AIML","year":"Second Year","marks":86},
 {"roll":102,"name":"Meera Patil","branch":"AIML","year":"Second Year","marks":92},
 {"roll":103,"name":"Kabir Deshmukh","branch":"CSE","year":"First Year","marks":78},
 {"roll":104,"name":"Ananya Joshi","branch":"AIML","year":"Second Year","marks":88},
]
@app.route("/")
def home(): return render_template("index.html")
@app.get("/api/students")
def get_students():
    q=request.args.get("q","").lower().strip()
    order=request.args.get("sort","roll")
    data=[s for s in students if q in str(s["roll"]).lower() or q in s["name"].lower() or q in s["branch"].lower()]
    if order=="marks": data.sort(key=lambda s:s["marks"],reverse=True)
    elif order=="name": data.sort(key=lambda s:s["name"].lower())
    else: data.sort(key=lambda s:s["roll"])
    return jsonify(data)
@app.post("/api/students")
def add_student():
    d=request.get_json(silent=True) or {}
    try:
        roll=int(d["roll"]); name=d["name"].strip(); branch=d["branch"].strip(); year=d["year"].strip(); marks=float(d["marks"])
        if not name or not branch or not year: raise ValueError("Please fill all fields.")
        if not 0<=marks<=100: raise ValueError("Marks must be between 0 and 100.")
        if any(s["roll"]==roll for s in students): raise ValueError("Roll number already exists.")
        students.append({"roll":roll,"name":name,"branch":branch,"year":year,"marks":marks})
        return jsonify(ok=True,message="Student record added successfully.")
    except (KeyError,ValueError,TypeError) as e:
        return jsonify(ok=False,error=str(e) or "Please enter valid details."),400
@app.delete("/api/students/<int:roll>")
def delete_student(roll):
    for i,s in enumerate(students):
        if s["roll"]==roll:
            students.pop(i); return jsonify(ok=True,message="Student record deleted.")
    return jsonify(ok=False,error="Student not found."),404
@app.get("/api/stats")
def stats():
    return jsonify(total=len(students),average=round(sum(s["marks"] for s in students)/len(students),1) if students else 0,
                   top=max(students,key=lambda s:s["marks"])["name"] if students else "—")
if __name__=="__main__": app.run(debug=True)
