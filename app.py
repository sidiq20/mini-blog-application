import datetime
import os
from flask import Flask, render_template, request
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)
    client = MongoClient(os.getenv("MONGODB_URI"))
    app.db = client.microblog

    @app.route("/", methods=["GET", "POST"])
    def home():
        if request.method == "POST":
            entry_content = request.form.get("content")
            if entry_content:
                formatted_date = datetime.datetime.today().strftime("%Y-%m-%d")
                try:
                    app.db.entries.insert_one({"content": entry_content, "date": formatted_date})
                except Exception as e:
                    print("Error inserting into MongoDB:", e)
            else:
                print("Empty content cannot be inserted")

        try:
            entries_with_date = [
                (
                    entry["content"],
                    entry["date"],
                    datetime.datetime.strptime(entry.get("date", "1900-01-01"), "%Y-%m-%d").strftime("%b %d")
                    if "date" in entry else "N/A"
                )
                for entry in app.db.entries.find({})
            ]
        except Exception as e:
            print("Error fetching from MongoDB:", e)
            entries_with_date = []

        return render_template("home.html", entries=entries_with_date)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=3000)
