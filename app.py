from flask import Flask, render_template
import json
import os

app = Flask(__name__)


def load_blog_posts():
    """Load the blog_posts"""
    with open("blog_posts.json", "r") as file:
        return json.load(file)


@app.route("/")
def index():
    blog_posts = load_blog_posts()
    return render_template("index.html", posts=blog_posts)

if __name__ == "__main__":
    app.run(debug=True)
    """Wichtig! Das ist die Funktion, die den internen Server startet.
    debug=True bedeutet, dass Flask im Debug-Modus läuft 
    (automatischer Neustart bei Code-Änderungen)."""
