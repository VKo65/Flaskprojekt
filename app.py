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


def save_blog_posts(posts):
    """Function to save Blog-Post"""
    with open("blog_posts.json", "w") as file:
        json.dump(posts, file, indent=4)


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

        blog_posts = load_blog_posts()

        new_id = max([post["id"] for post in blog_posts], default=0) + 1

        new_post = {
            "id": new_id,
            "author": author,
            "title": title,
            "content": content
        }
        blog_posts.append(new_post)

        save_blog_posts(blog_posts)

        return redirect(url_for('index'))

    return render_template('add.html')

@app.route('/delete/<int:post_id>', methods=['POST'])
def delete(post_id):
    """Load blog_posts, delete it and save it again"""
    blog_posts = load_blog_posts()

    blog_posts = [post for post in blog_posts if post["id"] != post_id]

    save_blog_posts(blog_posts)

    return redirect(url_for('index'))


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    """Load blog_posts, search for the post id, edit new values"""
    blog_posts = load_blog_posts()

    post = next((p for p in blog_posts if p["id"] == post_id), None)

    if not post:
        return "❌ Post not found", 404

    if request.method == 'POST':
        if request.form.get("author"):
            post["author"] = request.form.get("author")
        if request.form.get("title"):
            post["title"] = request.form.get("title")
        if request.form.get("content"):
            post["content"] = request.form.get("content")

        save_blog_posts(blog_posts)
        return redirect(url_for('index'))
    return render_template('update.html', post=post)

@app.route('/like/<int:post_id>', methods=['POST'])
def like(post_id):
    """New function, to set a like button"""
    blog_posts = load_blog_posts()

    post = next((p for p in blog_posts if p["id"] == post_id), None)

    if not post:
        return "❌ Post not found", 404

    if "likes" not in post:
        post["likes"] = 0
    post["likes"] += 1

    save_blog_posts(blog_posts)

    return redirect(url_for('index'))


    return render_template('update.html', post=post)  # Formular mit alten Werten anzeigen


if __name__ == "__main__":
    app.run(debug=True)
    """Wichtig! Das ist die Funktion, die den internen Server startet.
    debug=True bedeutet, dass Flask im Debug-Modus läuft 
    (automatischer Neustart bei Code-Änderungen)."""
