from flask import Flask, render_template, request, session, redirect
from flask_session import Session
import requests

app = Flask(__name__)

# STATEFUL SESSION AYARLARI
app.secret_key = "book-secret-key"
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/", methods=["GET", "POST"])
def index():
    if "liked_books" not in session:
        session["liked_books"] = []

    books = []

    if request.method == "POST":
        # Kitap arama
        if "search" in request.form:
            query = request.form.get("query")
            url = f"https://openlibrary.org/search.json?q={query}"
            books = requests.get(url).json()["docs"][:6]

        # Kalp butonu (beğeni)
        elif "like" in request.form:
            title = request.form.get("title")
            if title not in session["liked_books"]:
                session["liked_books"].append(title)
            session.modified = True

    return render_template(
        "index.html",
        books=books,
        liked_books=session["liked_books"]
    )

@app.route("/clear")
def clear():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
