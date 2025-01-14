import datetime
from flask import Flask, render_template, request
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient("mongodb+srv://sidiqolasode:1N7wJaJsOa13Hqyq@miniblog.zkfa0.mongodb.net/")
app.db = client.microblog


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        entry_content = request.form.get("content")
        if entry_content:
            formatted_date = datetime.datetime.today(). strftime("%Y-%m-%d")
            app.db.entries.insert_one({"content": entry_content, "date": formatted_date})
        else:
            print("Empty content cannot be insterted")

    entries_with_date = [
        (
            entry["content"],
            entry["date"],
            datetime.datetime.strptime(entry.get("date", "1900-01-01"), "%Y-%m-%d").strftime("%b %d")
            if "date" in entry else "N/A"
        )
        for entry in app.db.entries.find({})
    ]
    return render_template("home.html", entries=entries_with_date)

if __name__ == '__main__':
    app.run(debug=True, port=3000)
