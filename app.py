from flask import Flask, render_template, request, redirect, url_for
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


# 📌 Funktion zum Speichern der Blog-Posts
def save_blog_posts(posts):
    with open("blog_posts.json", "w") as file:
        json.dump(posts, file, indent=4)

# 📌 Route für "/add"
@app.route('/add', methods=['GET', 'POST'])
def add():
    """First action is the return of the add.html.
    There is this code <form action="/add" method="post">
    This code set the methode to post, in that moment, the user pushs the
    Add_Blog_Post button.
    This function here see the /add and the methode Post.
    and starts again. Now with if reguest.methode == Post --> True
    """
    if request.method == 'POST':
        author = request.form.get("author")
        title = request.form.get("title")
        content = request.form.get("content")

        if not author or not title or not content:
            return "❌ Fehler: Alle Felder müssen ausgefüllt werden!", 400

        # Lade bestehende Blog-Posts
        blog_posts = load_blog_posts()

        # Generiere eine neue eindeutige ID
        new_id = max([post["id"] for post in blog_posts], default=0) + 1

        # Füge den neuen Post zur Liste hinzu
        new_post = {
            "id": new_id,
            "author": author,
            "title": title,
            "content": content
        }
        blog_posts.append(new_post)

        # Speichere die aktualisierte Liste
        save_blog_posts(blog_posts)

        # Weiterleitung zur Startseite
        return redirect(url_for('index'))

    return render_template('add.html')

@app.route('/delete/<int:post_id>', methods=['POST'])
def delete(post_id):
    # Blog-Posts aus JSON laden
    blog_posts = load_blog_posts()

    # Entferne den Post mit der passenden ID
    blog_posts = [post for post in blog_posts if post["id"] != post_id]

    # Aktualisierte Liste speichern
    save_blog_posts(blog_posts)

    # Zurück zur Startseite
    return redirect(url_for('index'))


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    # Blog-Posts aus JSON laden
    blog_posts = load_blog_posts()

    # Den Blog-Post mit der passenden ID finden
    post = next((p for p in blog_posts if p["id"] == post_id), None)

    if not post:
        return "❌ Post not found", 404  # Falls der Post nicht existiert

    if request.method == 'POST':
        # Neue Werte aus dem Formular holen
        post["author"] = request.form.get("author")
        post["title"] = request.form.get("title")
        post["content"] = request.form.get("content")

        # Blog-Posts aktualisieren & speichern
        save_blog_posts(blog_posts)

        return redirect(url_for('index'))  # Zurück zur Startseite

    return render_template('update.html', post=post)  # Formular mit alten Werten anzeigen


if __name__ == "__main__":
    app.run(debug=True)
    """Wichtig! Das ist die Funktion, die den internen Server startet.
    debug=True bedeutet, dass Flask im Debug-Modus läuft 
    (automatischer Neustart bei Code-Änderungen)."""
